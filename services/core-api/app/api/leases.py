from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime, date
from app.database import get_leases_collection, get_lessees_collection, get_assets_collection, get_agent_logs_collection
from app.schemas import LeaseCreate, LesseeCreate

router = APIRouter(prefix="/leases", tags=["Leases & Lessees (Unstructured)"])

def clean_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

# -----------------------------------------------------------------------------
# Lessees
# -----------------------------------------------------------------------------
@router.get("/lessees", response_model=List[Dict[str, Any]])
async def get_all_lessees():
    col = get_lessees_collection()
    cursor = col.find({})
    results = []
    async for doc in cursor:
        results.append(clean_doc(doc))
    return results

@router.post("/lessees", response_model=Dict[str, Any])
async def create_lessee(payload: LesseeCreate):
    col = get_lessees_collection()
    existing = await col.find_one({"pan": payload.pan})
    if existing:
        raise HTTPException(status_code=400, detail="Lessee with this PAN already registered")
    
    doc = {
        "company_name": payload.company_name,
        "signatory_name": payload.signatory_name,
        "email": payload.email,
        "phone": payload.phone,
        "pan": payload.pan,
        "gstin": payload.gstin,
        "billing_address": payload.billing_address,
        "zoho_customer_id": f"ZB-CUST-{abs(hash(payload.pan))%1000000}",
        "kyc": payload.kyc_data or {"verified": True, "method": "DigiLocker / Aadhaar OTP"},
        "security_deposit": {
            "amount": payload.security_deposit_amount,
            "status": "HELD"
        },
        "created_at": datetime.utcnow()
    }
    result = await col.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return clean_doc(doc)

# -----------------------------------------------------------------------------
# Leases
# -----------------------------------------------------------------------------
@router.get("", response_model=List[Dict[str, Any]])
async def get_all_leases():
    col = get_leases_collection()
    cursor = col.find({})
    results = []
    async for doc in cursor:
        results.append(clean_doc(doc))
    return results

@router.post("", response_model=Dict[str, Any])
async def create_lease(payload: LeaseCreate):
    assets_col = get_assets_collection()
    asset = await assets_col.find_one({"asset_tag": payload.asset_tag})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    lessees_col = get_lessees_collection()
    lessee = await lessees_col.find_one({"pan": payload.lessee_pan})
    if not lessee:
        raise HTTPException(status_code=404, detail="Lessee not found")
    
    base_rent = payload.base_rent_monthly
    gst_rate = float(asset.get("financial_profile", {}).get("gst_rate_pct", 18.0))
    gst_amount = round(base_rent * (gst_rate / 100.0), 2)
    total_rent = round(base_rent + gst_amount, 2)
    
    lease_num = f"VL-LEASE-{datetime.utcnow().strftime('%Y%m')}-{payload.asset_tag}"
    
    doc = {
        "lease_number": lease_num,
        "asset_tag": payload.asset_tag,
        "lessee_pan": payload.lessee_pan,
        "lessee_name": lessee.get("company_name"),
        "start_date": datetime.combine(payload.start_date, datetime.min.time()),
        "end_date": datetime.combine(payload.end_date, datetime.min.time()),
        "financials": {
            "base_rent_monthly": base_rent,
            "sac_code": "997311",
            "gst_rate_pct": gst_rate,
            "gst_amount_monthly": gst_amount,
            "total_monthly_rent": total_rent,
            "billing_day_of_month": payload.billing_day_of_month,
            "payment_due_days": payload.payment_due_days
        },
        "contract_status": {
            "status": "ACTIVE",
            "e_signed": True,
            "contract_url": f"https://sign.visionloop.in/docs/{lease_num}.pdf"
        },
        "additional_clauses": payload.additional_clauses,
        "created_at": datetime.utcnow()
    }
    
    leases_col = get_leases_collection()
    result = await leases_col.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    
    # Update asset state to LEASED
    await assets_col.update_one({"_id": asset["_id"]}, {"$set": {"current_state.status": "LEASED"}})
    
    # Log Legal Sentinel Action
    logs_col = get_agent_logs_collection()
    await logs_col.insert_one({
        "agent_name": "LEGAL_SENTINEL",
        "asset_tag": payload.asset_tag,
        "action_type": "LEASE_DOCUMENT_CREATED",
        "severity": "INFO",
        "summary": f"Commercial Lease {lease_num} drafted & e-signed for {asset.get('name')} with {lessee.get('company_name')} at ₹{total_rent:,.2f}/mo (incl. 18% GST)",
        "details": {"base_rent": base_rent, "gst_amount": gst_amount, "total_rent": total_rent},
        "created_at": datetime.utcnow()
    })
    
    return clean_doc(doc)
