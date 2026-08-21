import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Numeric, Boolean, Date, DateTime, Text, Integer, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Asset(Base):
    __tablename__ = "assets"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    asset_tag = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    asset_type = Column(String(50), default="COMMERCIAL_EV")
    vin = Column(String(50), unique=True, nullable=True)
    registration_number = Column(String(30), unique=True, nullable=True)
    battery_capacity_kwh = Column(Numeric(5, 2), default=26.0)
    current_soc_pct = Column(Numeric(5, 2), default=100.0)
    current_soh_pct = Column(Numeric(5, 2), default=100.0)
    odometer_km = Column(Numeric(10, 2), default=0.0)
    last_serviced_km = Column(Numeric(10, 2), default=0.0)
    next_service_due_km = Column(Numeric(10, 2), default=10000.0)
    monthly_rental_base = Column(Numeric(12, 2), default=72000.00)
    sac_code = Column(String(20), default="997311")
    gst_rate_pct = Column(Numeric(5, 2), default=18.00)
    status = Column(String(30), default="AVAILABLE") # AVAILABLE, LEASED, MAINTENANCE, IMMOBILIZED
    immobilizer_active = Column(Boolean, default=False)
    current_lat = Column(Numeric(10, 6), default=28.6139)
    current_lng = Column(Numeric(10, 6), default=77.2090)
    speed_kmh = Column(Numeric(5, 2), default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    leases = relationship("Lease", back_populates="asset", cascade="all, delete-orphan")
    telemetry_records = relationship("TelemetryRecord", back_populates="asset", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="asset")

class Lessee(Base):
    __tablename__ = "lessees"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_name = Column(String(150), nullable=False)
    signatory_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    pan = Column(String(20), nullable=False)
    gstin = Column(String(20), nullable=True)
    billing_address = Column(Text, nullable=False)
    zoho_customer_id = Column(String(50), nullable=True)
    kyc_verified = Column(Boolean, default=False)
    security_deposit_amount = Column(Numeric(12, 2), default=144000.00)
    created_at = Column(DateTime, default=datetime.utcnow)

    leases = relationship("Lease", back_populates="lessee")
    invoices = relationship("Invoice", back_populates="lessee")

class Lease(Base):
    __tablename__ = "leases"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    lease_number = Column(String(50), unique=True, nullable=False)
    asset_id = Column(String(36), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    lessee_id = Column(String(36), ForeignKey("lessees.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    base_rent_monthly = Column(Numeric(12, 2), default=72000.00)
    gst_amount_monthly = Column(Numeric(12, 2), default=12960.00)
    total_monthly_rent = Column(Numeric(12, 2), default=84960.00)
    billing_day_of_month = Column(Integer, default=1)
    payment_due_days = Column(Integer, default=5)
    status = Column(String(30), default="ACTIVE") # DRAFT, ACTIVE, EXPIRED, TERMINATED
    contract_signed = Column(Boolean, default=False)
    e_sign_doc_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    asset = relationship("Asset", back_populates="leases")
    lessee = relationship("Lessee", back_populates="leases")
    invoices = relationship("Invoice", back_populates="lease")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    invoice_number = Column(String(50), unique=True, nullable=False)
    zoho_invoice_id = Column(String(50), unique=True, nullable=True)
    lease_id = Column(String(36), ForeignKey("leases.id", ondelete="SET NULL"), nullable=True)
    asset_id = Column(String(36), ForeignKey("assets.id", ondelete="SET NULL"), nullable=True)
    lessee_id = Column(String(36), ForeignKey("lessees.id", ondelete="SET NULL"), nullable=True)
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    sac_code = Column(String(20), default="997311")
    base_amount = Column(Numeric(12, 2), default=72000.00)
    cgst_amount = Column(Numeric(12, 2), default=6480.00)
    sgst_amount = Column(Numeric(12, 2), default=6480.00)
    igst_amount = Column(Numeric(12, 2), default=0.00)
    total_amount = Column(Numeric(12, 2), default=84960.00)
    status = Column(String(30), default="PENDING") # DRAFT, PENDING, PAID, OVERDUE, ESCALATED
    payment_method = Column(String(50), nullable=True)
    payment_reference = Column(String(100), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    pdf_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    lease = relationship("Lease", back_populates="invoices")
    asset = relationship("Asset", back_populates="invoices")
    lessee = relationship("Lessee", back_populates="invoices")

class TelemetryRecord(Base):
    __tablename__ = "telemetry_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    asset_id = Column(String(36), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    latitude = Column(Numeric(10, 6), nullable=False)
    longitude = Column(Numeric(10, 6), nullable=False)
    speed_kmh = Column(Numeric(5, 2), default=0.0)
    soc_pct = Column(Numeric(5, 2), nullable=False)
    battery_temp_c = Column(Numeric(5, 2), default=28.5)
    battery_voltage = Column(Numeric(6, 2), default=380.0)
    odometer_km = Column(Numeric(10, 2), nullable=False)
    fault_codes = Column(Text, nullable=True)
    ignition_on = Column(Boolean, default=True)
    charging_status = Column(String(20), default="DISCHARGING")

    asset = relationship("Asset", back_populates="telemetry_records")

class AgentActionLog(Base):
    __tablename__ = "agent_action_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    agent_name = Column(String(50), nullable=False)
    asset_id = Column(String(36), ForeignKey("assets.id", ondelete="SET NULL"), nullable=True)
    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="SET NULL"), nullable=True)
    action_type = Column(String(50), nullable=False)
    severity = Column(String(20), default="INFO")
    summary = Column(Text, nullable=False)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
