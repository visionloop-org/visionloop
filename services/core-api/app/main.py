from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date

from app.config import settings
from app.database import (
    connect_to_mongo, close_mongo_connection, 
    get_assets_collection, get_lessees_collection, get_leases_collection, 
    get_invoices_collection, get_agent_logs_collection, get_telemetry_collection
)
from app.api import assets, leases, invoices, telemetry, agents, compliance, graph

app = FastAPI(
    title="Vision Loop — Autonomous Core API (Unstructured MongoDB)",
    description="Backend microservice managing polymorphic asset documents, CAN-Bus streams, Zoho Books sync, and AI agent operations.",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(assets.router)
app.include_router(leases.router)
app.include_router(invoices.router)
app.include_router(telemetry.router)
app.include_router(agents.router)
app.include_router(compliance.router)
app.include_router(graph.router)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()
    
    # Auto-seed initial Tata Intra EV if collection is empty
    assets_col = get_assets_collection()
    existing = await assets_col.find_one({"asset_tag": "VL-EV-001"})
    if not existing:
        # Seed Tata Intra EV
        await assets_col.insert_one({
            "asset_tag": "VL-EV-001",
            "name": "Tata Intra EV Commercial Goods Carriage",
            "asset_type": "COMMERCIAL_EV",
            "vin": "MAT612345N2A09876",
            "registration_number": "DL-01-EV-2026",
            "specifications": {
                "battery_capacity_kwh": 26.0,
                "payload_capacity_kg": 1000,
                "range_certified_km": 140
            },
            "current_state": {
                "soc_pct": 92.5,
                "soh_pct": 99.4,
                "battery_temp_c": 29.2,
                "odometer_km": 3420.0,
                "speed_kmh": 24.5,
                "location": {"type": "Point", "coordinates": [77.2090, 28.6139]},
                "immobilizer_active": False,
                "status": "LEASED",
                "last_serviced_km": 0.0,
                "next_service_due_km": 10000.0
            },
            "financial_profile": {
                "monthly_rental_base": 72000.00,
                "sac_code": "997311",
                "gst_rate_pct": 18.00,
                "monthly_gst_amount": 12960.00,
                "total_monthly_invoiced": 84960.00
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        # Seed Lessee
        lessees_col = get_lessees_collection()
        await lessees_col.insert_one({
            "company_name": "SwiftLogix Express Delivery Pvt Ltd",
            "signatory_name": "Rajesh Sharma (Director)",
            "email": "accounts@swiftlogix.in",
            "phone": "+919876543210",
            "pan": "AAACS1234F",
            "gstin": "07AAACS1234F1Z5",
            "billing_address": "Plot 42, Okhla Industrial Area Phase-III, New Delhi, Delhi - 110020",
            "zoho_customer_id": "ZB-CUST-883921",
            "kyc": {"verified": True, "method": "DigiLocker / Aadhaar OTP"},
            "security_deposit": {"amount": 144000.00, "status": "HELD"},
            "created_at": datetime.utcnow()
        })
        
        # Seed Lease
        leases_col = get_leases_collection()
        await leases_col.insert_one({
            "lease_number": "VL-LEASE-2026-001",
            "asset_tag": "VL-EV-001",
            "lessee_pan": "AAACS1234F",
            "lessee_name": "SwiftLogix Express Delivery Pvt Ltd",
            "start_date": datetime(2026, 8, 1),
            "end_date": datetime(2028, 7, 31),
            "financials": {
                "base_rent_monthly": 72000.00,
                "sac_code": "997311",
                "gst_rate_pct": 18.00,
                "gst_amount_monthly": 12960.00,
                "total_monthly_rent": 84960.00,
                "billing_day_of_month": 1,
                "payment_due_days": 5
            },
            "contract_status": {
                "status": "ACTIVE",
                "e_signed": True,
                "contract_url": "https://sign.visionloop.in/docs/VL-LEASE-2026-001.pdf"
            },
            "created_at": datetime.utcnow()
        })
        
        # Seed Invoice
        invoices_col = get_invoices_collection()
        await invoices_col.insert_one({
            "invoice_number": "VL-INV-2026-08-001",
            "zoho_invoice_id": "ZB-INV-99201",
            "lease_number": "VL-LEASE-2026-001",
            "asset_tag": "VL-EV-001",
            "lessee_pan": "AAACS1234F",
            "lessee_name": "SwiftLogix Express Delivery Pvt Ltd",
            "invoice_date": datetime(2026, 8, 1),
            "due_date": datetime(2026, 8, 5),
            "sac_code": "997311",
            "tax_summary": {
                "taxable_value": 72000.00,
                "cgst": 6480.00,
                "sgst": 6480.00,
                "igst": 0.00,
                "total_tax": 12960.00,
                "total_payable": 84960.00
            },
            "settlement": {
                "status": "PAID",
                "payment_method": "e-NACH Auto-Debit",
                "payment_reference": "NACH-ICICI-20260805-9981",
                "paid_at": datetime(2026, 8, 5, 10, 30, 0),
                "receipt_url": "https://books.zoho.in/secure/receipts/ZB-INV-99201.pdf"
            },
            "created_at": datetime.utcnow()
        })
        
        # Seed Telemetry
        telem_col = get_telemetry_collection()
        await telem_col.insert_one({
            "asset_tag": "VL-EV-001",
            "timestamp": datetime.utcnow(),
            "location": {"type": "Point", "coordinates": [77.2090, 28.6139]},
            "speed_kmh": 24.5,
            "soc_pct": 92.5,
            "battery_temp_c": 29.2,
            "battery_voltage": 384.2,
            "odometer_km": 3420.0,
            "ignition_on": True,
            "charging_status": "DISCHARGING"
        })
        
        # Seed AI Logs
        logs_col = get_agent_logs_collection()
        await logs_col.insert_many([
            {
                "agent_name": "LEGAL_SENTINEL",
                "asset_tag": "VL-EV-001",
                "action_type": "CONTRACT_E_SIGNED",
                "severity": "INFO",
                "summary": "Commercial Lease Agreement for Tata Intra EV (DL-01-EV-2026) verified via Aadhaar OTP e-Sign by Rajesh Sharma (SwiftLogix).",
                "details": {"lease_number": "VL-LEASE-2026-001", "sac_code": "997311"},
                "created_at": datetime.utcnow()
            },
            {
                "agent_name": "FINANCIAL_SENTINEL",
                "asset_tag": "VL-EV-001",
                "action_type": "PAYMENT_RECONCILED",
                "severity": "INFO",
                "summary": "e-NACH auto-cleared: ₹84,960 (₹72,000 + 18% GST) received for Invoice VL-INV-2026-08-001. Zoho Books ledger updated.",
                "details": {"ref": "NACH-ICICI-20260805-9981", "amount": 84960.0},
                "created_at": datetime.utcnow()
            },
            {
                "agent_name": "TELEMATICS_SENTINEL",
                "asset_tag": "VL-EV-001",
                "action_type": "TELEMETRY_NOMINAL",
                "severity": "INFO",
                "summary": "CAN-Bus scan nominal: Battery SoH 99.4%, Cell delta 0.01V, Operating temperature 29.2°C.",
                "details": {"soc": 92.5, "odometer": 3420.0},
                "created_at": datetime.utcnow()
            }
        ])

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/")
def health_check():
    return {
        "service": "Vision Loop Core API",
        "database": "Unstructured Document Store (MongoDB)",
        "status": "online",
        "timestamp": datetime.utcnow().isoformat(),
        "docs_url": "/docs"
    }
