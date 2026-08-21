from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime
from app.database import get_assets_collection, get_agent_logs_collection
from app.schemas import AssetCreate, AssetUpdate

router = APIRouter(prefix="/assets", tags=["Assets (Unstructured)"])

def clean_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    # Flatten common properties for dashboard backward compatibility
    if "current_state" in doc:
        cs = doc["current_state"]
        doc["current_soc_pct"] = cs.get("soc_pct", 100.0)
        doc["current_soh_pct"] = cs.get("soh_pct", 100.0)
        doc["odometer_km"] = cs.get("odometer_km", 0.0)
        doc["last_serviced_km"] = cs.get("last_serviced_km", 0.0)
        doc["next_service_due_km"] = cs.get("next_service_due_km", 10000.0)
        doc["status"] = cs.get("status", "AVAILABLE")
        doc["immobilizer_active"] = cs.get("immobilizer_active", False)
        doc["speed_kmh"] = cs.get("speed_kmh", 0.0)
        loc = cs.get("location", {})
        if loc and "coordinates" in loc:
            doc["current_lng"] = loc["coordinates"][0]
            doc["current_lat"] = loc["coordinates"][1]
    return doc

@router.get("", response_model=List[Dict[str, Any]])
async def get_all_assets():
    col = get_assets_collection()
    cursor = col.find({})
    results = []
    async for doc in cursor:
        results.append(clean_doc(doc))
    return results

@router.get("/{asset_id}", response_model=Dict[str, Any])
async def get_asset_by_id(asset_id: str):
    col = get_assets_collection()
    doc = await col.find_one({"$or": [{"asset_tag": asset_id}, {"vin": asset_id}]})
    if not doc:
        raise HTTPException(status_code=404, detail="Asset document not found")
    return clean_doc(doc)

@router.post("", response_model=Dict[str, Any])
async def create_asset(payload: AssetCreate):
    col = get_assets_collection()
    existing = await col.find_one({"asset_tag": payload.asset_tag})
    if existing:
        raise HTTPException(status_code=400, detail="Asset document with this tag already exists")
    
    doc = {
        "asset_tag": payload.asset_tag,
        "name": payload.name,
        "asset_type": payload.asset_type,
        "vin": payload.vin,
        "registration_number": payload.registration_number,
        "specifications": payload.specifications or {
            "battery_capacity_kwh": 26.0,
            "payload_capacity_kg": 1000
        },
        "current_state": {
            "soc_pct": 100.0,
            "soh_pct": 100.0,
            "odometer_km": 0.0,
            "speed_kmh": 0.0,
            "location": {"type": "Point", "coordinates": [77.2090, 28.6139]},
            "immobilizer_active": False,
            "status": "AVAILABLE",
            "last_serviced_km": 0.0,
            "next_service_due_km": 10000.0
        },
        "financial_profile": {
            "monthly_rental_base": payload.monthly_rental_base,
            "sac_code": payload.sac_code,
            "gst_rate_pct": payload.gst_rate_pct,
            "monthly_gst_amount": round(payload.monthly_rental_base * (payload.gst_rate_pct / 100.0), 2),
            "total_monthly_invoiced": round(payload.monthly_rental_base * (1 + (payload.gst_rate_pct / 100.0)), 2)
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = await col.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return clean_doc(doc)

@router.patch("/{asset_id}", response_model=Dict[str, Any])
async def update_asset(asset_id: str, payload: AssetUpdate):
    col = get_assets_collection()
    asset = await col.find_one({"$or": [{"asset_tag": asset_id}, {"vin": asset_id}]})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    update_dict = {}
    if payload.status:
        update_dict["current_state.status"] = payload.status
    if payload.immobilizer_active is not None:
        update_dict["current_state.immobilizer_active"] = payload.immobilizer_active
    if payload.current_soc_pct is not None:
        update_dict["current_state.soc_pct"] = payload.current_soc_pct
    if payload.odometer_km is not None:
        update_dict["current_state.odometer_km"] = payload.odometer_km
    if payload.current_lat is not None and payload.current_lng is not None:
        update_dict["current_state.location"] = {
            "type": "Point",
            "coordinates": [payload.current_lng, payload.current_lat]
        }
    if payload.speed_kmh is not None:
        update_dict["current_state.speed_kmh"] = payload.speed_kmh
    if payload.specifications:
        update_dict["specifications"] = payload.specifications
        
    update_dict["updated_at"] = datetime.utcnow()
    
    await col.update_one({"_id": asset["_id"]}, {"$set": update_dict})
    updated = await col.find_one({"_id": asset["_id"]})
    return clean_doc(updated)

@router.post("/{asset_id}/immobilizer/toggle")
async def toggle_immobilizer(asset_id: str):
    col = get_assets_collection()
    asset = await col.find_one({"$or": [{"asset_tag": asset_id}, {"vin": asset_id}]})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    current_state = asset.get("current_state", {})
    new_immob = not current_state.get("immobilizer_active", False)
    new_status = "IMMOBILIZED" if new_immob else "LEASED"
    
    await col.update_one(
        {"_id": asset["_id"]},
        {"$set": {
            "current_state.immobilizer_active": new_immob,
            "current_state.status": new_status,
            "updated_at": datetime.utcnow()
        }}
    )
    
    # Log Action to MongoDB
    logs_col = get_agent_logs_collection()
    await logs_col.insert_one({
        "agent_name": "SECURITY_CONTROLLER",
        "asset_tag": asset.get("asset_tag"),
        "action_type": "IMMOBILIZER_TOGGLED",
        "severity": "CRITICAL" if new_immob else "INFO",
        "summary": f"Remote ignition immobilizer {'ACTIVATED (Engine Cut-off)' if new_immob else 'DEACTIVATED'} for {asset.get('asset_tag')} ({asset.get('name')})",
        "details": {
            "previous_state": current_state.get("immobilizer_active", False),
            "new_state": new_immob,
            "status": new_status,
            "speed_kmh": current_state.get("speed_kmh", 0.0)
        },
        "created_at": datetime.utcnow()
    })
    
    return {
        "status": "success",
        "asset_tag": asset.get("asset_tag"),
        "immobilizer_active": new_immob,
        "asset_status": new_status,
        "message": f"Immobilizer relay {'engaged (motor cut-off)' if new_immob else 'disengaged (normal operation)'}"
    }
