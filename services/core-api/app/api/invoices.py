from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta
from app.database import get_invoices_collection, get_leases_collection, get_agent_logs_collection
from app.schemas import InvoiceCreate, InvoicePaymentUpdate

router = APIRouter(prefix="/invoices", tags=["Invoices (Zoho & SAC 997311)"])

def clean_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    # Flatten fields for dashboard compatibility
    if "tax_summary" in doc:
        ts = doc["tax_summary"]
        doc["base_amount"] = ts.get("taxable_value", 72000.00)
        doc["cgst_amount"] = ts.get("cgst", 6480.00)
        doc["sgst_amount"] = ts.get("sgst", 6480.00)
        doc["igst_amount"] = ts.get("igst", 0.00)
        doc["total_amount"] = ts.get("total_payable", 84960.00)
    if "settlement" in doc:
        st = doc["settlement"]
        doc["status"] = st.get("status", "PENDING")
        doc["payment_method"] = st.get("payment_method")
        doc["payment_reference"] = st.get("payment_reference")
        doc["paid_at"] = st.get("paid_at")
    if isinstance(doc.get("invoice_date"), datetime):
        doc["invoice_date"] = doc["invoice_date"].strftime("%Y-%m-%d")
    if isinstance(doc.get("due_date"), datetime):
        doc["due_date"] = doc["due_date"].strftime("%Y-%m-%d")
    return doc

@router.get("", response_model=List[Dict[str, Any]])
async def get_all_invoices(status: Optional[str] = None):
    col = get_invoices_collection()
    query = {}
    if status:
        query["settlement.status"] = status.upper()
    cursor = col.find(query).sort("created_at", -1)
    results = []
    async for doc in cursor:
        results.append(clean_doc(doc))
    return results

@router.get("/{invoice_id}", response_model=Dict[str, Any])
async def get_invoice_by_id(invoice_id: str):
    col = get_invoices_collection()
    doc = await col.find_one({"$or": [{"invoice_number": invoice_id}, {"zoho_invoice_id": invoice_id}]})
    if not doc:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return clean_doc(doc)

@router.post("/generate", response_model=Dict[str, Any])
async def generate_monthly_invoice(payload: InvoiceCreate):
    inv_date = payload.invoice_date or date.today()
    due_date = payload.due_date or (inv_date + timedelta(days=5))
    
    base_amt = payload.base_amount
    cgst = round(base_amt * 0.09, 2)
    sgst = round(base_amt * 0.09, 2)
    total_amt = round(base_amt + cgst + sgst, 2)
    
    inv_num = f"VL-INV-{inv_date.strftime('%Y%m')}-{inv_date.strftime('%d%H%M')}"
    
    doc = {
        "invoice_number": inv_num,
        "zoho_invoice_id": f"ZB-{inv_num}",
        "lease_number": payload.lease_number or "VL-LEASE-2026-001",
        "asset_tag": payload.asset_tag or "VL-EV-001",
        "lessee_pan": payload.lessee_pan or "AAACS1234F",
        "lessee_name": payload.lessee_name or "SwiftLogix Express Delivery Pvt Ltd",
        "invoice_date": datetime.combine(inv_date, datetime.min.time()),
        "due_date": datetime.combine(due_date, datetime.min.time()),
        "sac_code": payload.sac_code,
        "line_items": [
            {
                "description": f"Commercial EV Dry Lease (SAC {payload.sac_code}) - Tata Intra EV",
                "sac_code": payload.sac_code,
                "base_amount": base_amt,
                "cgst_amount": cgst,
                "sgst_amount": sgst,
                "total_amount": total_amt
            }
        ],
        "tax_summary": {
            "taxable_value": base_amt,
            "cgst": cgst,
            "sgst": sgst,
            "igst": 0.00,
            "total_tax": round(cgst + sgst, 2),
            "total_payable": total_amt
        },
        "settlement": {
            "status": "PENDING",
            "payment_method": None,
            "payment_reference": None,
            "paid_at": None,
            "payment_link": f"https://pay.visionloop.in/invoice/{inv_num}",
            "upi_qr": f"upi://pay?pa=visionloop@icici&pn=VisionLoop&am={total_amt}&tr={inv_num}"
        },
        "created_at": datetime.utcnow()
    }
    
    col = get_invoices_collection()
    result = await col.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    
    # Log Financial Sentinel Action
    logs_col = get_agent_logs_collection()
    await logs_col.insert_one({
        "agent_name": "FINANCIAL_SENTINEL",
        "asset_tag": payload.asset_tag,
        "invoice_number": inv_num,
        "action_type": "INVOICE_GENERATED",
        "severity": "INFO",
        "summary": f"Automated recurring invoice {inv_num} generated for {doc['lessee_name']} (SAC {payload.sac_code}): Base ₹{base_amt:,.2f} + 18% GST (₹{cgst+sgst:,.2f}) = ₹{total_amt:,.2f}",
        "details": {"invoice_number": inv_num, "base_amount": base_amt, "total_payable": total_amt},
        "created_at": datetime.utcnow()
    })
    
    return clean_doc(doc)

@router.post("/{invoice_id}/pay", response_model=Dict[str, Any])
async def record_payment(invoice_id: str, payload: InvoicePaymentUpdate):
    col = get_invoices_collection()
    inv = await col.find_one({"$or": [{"invoice_number": invoice_id}, {"zoho_invoice_id": invoice_id}]})
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    paid_time = payload.paid_at or datetime.utcnow()
    
    await col.update_one(
        {"_id": inv["_id"]},
        {"$set": {
            "settlement.status": "PAID",
            "settlement.payment_method": payload.payment_method,
            "settlement.payment_reference": payload.payment_reference,
            "settlement.paid_at": paid_time,
            "updated_at": datetime.utcnow()
        }}
    )
    
    # Log Action
    logs_col = get_agent_logs_collection()
    total_paid = inv.get("tax_summary", {}).get("total_payable", 84960.00)
    await logs_col.insert_one({
        "agent_name": "FINANCIAL_SENTINEL",
        "asset_tag": inv.get("asset_tag"),
        "invoice_number": inv.get("invoice_number"),
        "action_type": "PAYMENT_RECONCILED",
        "severity": "INFO",
        "summary": f"Bank feed auto-reconciled: ₹{total_paid:,.2f} received for {inv.get('invoice_number')} via {payload.payment_method} (Ref: {payload.payment_reference}). Zoho Books ledger cleared.",
        "details": {"ref": payload.payment_reference, "amount": total_paid, "paid_at": paid_time.isoformat()},
        "created_at": datetime.utcnow()
    })
    
    updated = await col.find_one({"_id": inv["_id"]})
    return clean_doc(updated)
