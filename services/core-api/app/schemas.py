from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# Asset Schemas (Unstructured / Polymorphic)
# -----------------------------------------------------------------------------
class AssetCreate(BaseModel):
    asset_tag: str
    name: str
    asset_type: str = "COMMERCIAL_EV"
    vin: Optional[str] = None
    registration_number: Optional[str] = None
    specifications: Optional[Dict[str, Any]] = Field(default_factory=dict)
    financial_profile: Optional[Dict[str, Any]] = Field(default_factory=dict)
    monthly_rental_base: float = 72000.00
    sac_code: str = "997311"
    gst_rate_pct: float = 18.00

class AssetUpdate(BaseModel):
    status: Optional[str] = None
    immobilizer_active: Optional[bool] = None
    current_soc_pct: Optional[float] = None
    current_soh_pct: Optional[float] = None
    odometer_km: Optional[float] = None
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    speed_kmh: Optional[float] = None
    specifications: Optional[Dict[str, Any]] = None
    current_state: Optional[Dict[str, Any]] = None

# -----------------------------------------------------------------------------
# Lessee Schemas
# -----------------------------------------------------------------------------
class LesseeCreate(BaseModel):
    company_name: str
    signatory_name: str
    email: str
    phone: str
    pan: str
    gstin: Optional[str] = None
    billing_address: str
    security_deposit_amount: float = 144000.00
    kyc_data: Optional[Dict[str, Any]] = Field(default_factory=dict)

# -----------------------------------------------------------------------------
# Lease Schemas
# -----------------------------------------------------------------------------
class LeaseCreate(BaseModel):
    asset_tag: str
    lessee_pan: str
    lessee_name: Optional[str] = None
    start_date: date
    end_date: date
    base_rent_monthly: float = 72000.00
    billing_day_of_month: int = 1
    payment_due_days: int = 5
    additional_clauses: Optional[Dict[str, Any]] = Field(default_factory=dict)

# -----------------------------------------------------------------------------
# Invoice Schemas
# -----------------------------------------------------------------------------
class InvoiceCreate(BaseModel):
    lease_number: Optional[str] = None
    asset_tag: Optional[str] = "VL-EV-001"
    lessee_pan: Optional[str] = "AAACS1234F"
    lessee_name: Optional[str] = "SwiftLogix Express Delivery Pvt Ltd"
    invoice_date: Optional[date] = None
    due_date: Optional[date] = None
    base_amount: float = 72000.00
    sac_code: str = "997311"

class InvoicePaymentUpdate(BaseModel):
    payment_method: str = "e-NACH Auto-Debit"
    payment_reference: str
    paid_at: Optional[datetime] = None

# -----------------------------------------------------------------------------
# Telemetry Schemas (Unstructured CAN-Bus & Sensor Payloads)
# -----------------------------------------------------------------------------
class TelemetryCreate(BaseModel):
    asset_id: Optional[str] = None
    asset_tag: Optional[str] = "VL-EV-001"
    latitude: float
    longitude: float
    speed_kmh: float = 0.0
    soc_pct: float
    battery_temp_c: float = 28.5
    battery_voltage: float = 380.0
    odometer_km: float
    fault_codes: Optional[str] = None
    ignition_on: bool = True
    charging_status: str = "DISCHARGING"
    cell_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    raw_can_frames: Optional[List[Dict[str, Any]]] = None

# -----------------------------------------------------------------------------
# Agent Action Logs (Unstructured AI Memory & Decision Graphs)
# -----------------------------------------------------------------------------
class AgentActionCreate(BaseModel):
    agent_name: str
    asset_tag: Optional[str] = None
    invoice_number: Optional[str] = None
    action_type: str
    severity: str = "INFO"
    summary: str
    details: Optional[Dict[str, Any]] = None
