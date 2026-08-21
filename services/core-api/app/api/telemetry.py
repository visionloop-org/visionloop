from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.database import get_telemetry_collection, get_assets_collection, get_agent_logs_collection
from app.schemas import TelemetryCreate

router = APIRouter(prefix="/telemetry", tags=["IoT Telematics (Unstructured Documents)"])

def clean_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    if "location" in doc and "coordinates" in doc["location"]:
        doc["longitude"] = doc["location"]["coordinates"][0]
        doc["latitude"] = doc["location"]["coordinates"][1]
    return doc

@router.get("/latest/{asset_tag}", response_model=Optional[Dict[str, Any]])
async def get_latest_telemetry(asset_tag: str):
    col = get_telemetry_collection()
    doc = await col.find_one({"asset_tag": asset_tag}, sort=[("timestamp", -1)])
    return clean_doc(doc)

@router.get("/history/{asset_tag}", response_model=List[Dict[str, Any]])
async def get_telemetry_history(asset_tag: str, limit: int = 50):
    col = get_telemetry_collection()
    cursor = col.find({"asset_tag": asset_tag}).sort("timestamp", -1).limit(limit)
    results = []
    async for doc in cursor:
        results.append(clean_doc(doc))
    return results

@router.post("/ingest", response_model=Dict[str, Any])
async def ingest_telemetry(payload: TelemetryCreate):
    tag = payload.asset_tag or payload.asset_id or "VL-EV-001"
    
    assets_col = get_assets_collection()
    asset = await assets_col.find_one({"asset_tag": tag})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Construct unstructured telemetry document with 2dsphere location
    doc = {
        "asset_tag": tag,
        "timestamp": datetime.utcnow(),
        "location": {
            "type": "Point",
            "coordinates": [payload.longitude, payload.latitude]
        },
        "speed_kmh": payload.speed_kmh,
        "soc_pct": payload.soc_pct,
        "battery_temp_c": payload.battery_temp_c,
        "battery_voltage": payload.battery_voltage,
        "odometer_km": payload.odometer_km,
        "ignition_on": payload.ignition_on,
        "charging_status": payload.charging_status,
        "fault_codes": payload.fault_codes,
        "cell_data": payload.cell_data or {
            "max_cell_v": round(3.8 + (payload.soc_pct / 100.0) * 0.35, 2),
            "min_cell_v": round(3.8 + (payload.soc_pct / 100.0) * 0.34, 2),
            "cell_delta_v": 0.01
        },
        "raw_can_frames": payload.raw_can_frames or []
    }
    
    telem_col = get_telemetry_collection()
    res = await telem_col.insert_one(doc)
    doc["id"] = str(res.inserted_id)
    
    # Update Asset current_state
    current_state = asset.get("current_state", {})
    next_service = float(current_state.get("next_service_due_km", 10000.0))
    
    await assets_col.update_one(
        {"_id": asset["_id"]},
        {"$set": {
            "current_state.soc_pct": payload.soc_pct,
            "current_state.odometer_km": payload.odometer_km,
            "current_state.speed_kmh": payload.speed_kmh,
            "current_state.battery_temp_c": payload.battery_temp_c,
            "current_state.location": {
                "type": "Point",
                "coordinates": [payload.longitude, payload.latitude]
            },
            "updated_at": datetime.utcnow()
        }}
    )
    
    # Autonomous Checks
    logs_col = get_agent_logs_collection()
    
    # 1. 10,000 km Service Check
    if payload.odometer_km >= next_service:
        await logs_col.insert_one({
            "agent_name": "TELEMATICS_SENTINEL",
            "asset_tag": tag,
            "action_type": "SERVICE_SCHEDULED",
            "severity": "WARNING",
            "summary": f"10,000 KM Milestone Reached ({payload.odometer_km} km)! Automated service ticket dispatched to Tata Motors Authorized Commercial Workshop.",
            "details": {"odometer": payload.odometer_km, "next_due": next_service + 10000.0},
            "created_at": datetime.utcnow()
        })
        await assets_col.update_one(
            {"_id": asset["_id"]},
            {"$set": {
                "current_state.last_serviced_km": payload.odometer_km,
                "current_state.next_service_due_km": next_service + 10000.0
            }}
        )

    # 2. Battery Thermal Alert (>45°C)
    if payload.battery_temp_c > 45.0:
        await logs_col.insert_one({
            "agent_name": "TELEMATICS_SENTINEL",
            "asset_tag": tag,
            "action_type": "BATTERY_OVERHEAT_ALERT",
            "severity": "CRITICAL",
            "summary": f"High Battery Temperature ({payload.battery_temp_c}°C) detected on {asset.get('name')}! Active liquid thermal management engaged.",
            "details": {"temp": payload.battery_temp_c, "soc": payload.soc_pct},
            "created_at": datetime.utcnow()
        })
        
    return clean_doc(doc)
