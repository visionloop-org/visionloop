from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import date

from app.client import zoho_client
from app.tax_rules import IndianTaxEngine

app = FastAPI(
    title="Vision Loop — Zoho Books Connector Service",
    description="Automated invoicing, SAC 997311 GST compliance, and bank payment reconciliation.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreateInvoiceRequest(BaseModel):
    customer_id: str
    asset_name: str
    asset_tag: str
    base_rent: float = 72000.00
    is_inter_state: bool = False
    inv_date: Optional[date] = None

class PaymentWebhookPayload(BaseModel):
    invoice_id: str
    amount: float
    reference_number: str
    payment_mode: str = "e-NACH"

@app.get("/")
def health_check():
    return {"service": "Vision Loop Zoho Connector", "status": "online"}

@app.get("/tax-calculator")
def calculate_tax(base_rent: float = 72000.00, is_inter_state: bool = False):
    return IndianTaxEngine.calculate_lease_tax(base_rent, is_inter_state)

@app.post("/invoices/generate")
async def generate_invoice(payload: CreateInvoiceRequest):
    inv = await zoho_client.create_recurring_invoice(
        customer_id=payload.customer_id,
        asset_name=payload.asset_name,
        asset_tag=payload.asset_tag,
        base_rent=payload.base_rent,
        is_inter_state=payload.is_inter_state,
        inv_date=payload.inv_date
    )
    return inv

@app.post("/webhooks/payment")
async def handle_payment_webhook(payload: PaymentWebhookPayload):
    receipt = await zoho_client.reconcile_payment(
        invoice_id=payload.invoice_id,
        amount=payload.amount,
        reference=payload.reference_number
    )
    return receipt
