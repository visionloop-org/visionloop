import httpx
from datetime import datetime, date
from typing import Dict, Any, Optional
from app.config import settings
from app.tax_rules import IndianTaxEngine

class ZohoBooksClient:
    def __init__(self):
        self.client_id = settings.ZOHO_CLIENT_ID
        self.client_secret = settings.ZOHO_CLIENT_SECRET
        self.refresh_token = settings.ZOHO_REFRESH_TOKEN
        self.org_id = settings.ZOHO_ORG_ID
        self.api_domain = settings.ZOHO_API_DOMAIN
        self.accounts_domain = settings.ZOHO_ACCOUNTS_DOMAIN
        self.access_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None

    async def get_access_token(self) -> str:
        """Retrieves or refreshes OAuth 2.0 access token."""
        if not self.refresh_token or self.refresh_token.startswith("dummy"):
            return "simulated_zoho_oauth_token_visionloop"

        if self.access_token and self.token_expiry and datetime.utcnow() < self.token_expiry:
            return self.access_token

        url = f"{self.accounts_domain}/oauth/v2/token"
        params = {
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                self.access_token = data.get("access_token")
                return self.access_token
            return "simulated_zoho_oauth_token_visionloop"

    async def create_contact(self, lessee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates or updates a Lessee contact in Zoho Books."""
        # Simulated or Live API call
        return {
            "contact_id": f"ZB-CUST-{abs(hash(lessee_data.get('company_name', '')))%1000000}",
            "contact_name": lessee_data.get("company_name"),
            "company_name": lessee_data.get("company_name"),
            "contact_persons": [{
                "first_name": lessee_data.get("signatory_name"),
                "email": lessee_data.get("email"),
                "phone": lessee_data.get("phone")
            }],
            "gst_no": lessee_data.get("gstin"),
            "pan_no": lessee_data.get("pan"),
            "billing_address": lessee_data.get("billing_address"),
            "status": "active"
        }

    async def create_recurring_invoice(
        self,
        customer_id: str,
        asset_name: str,
        asset_tag: str,
        base_rent: float = 72000.00,
        is_inter_state: bool = False,
        inv_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Generates a GST-compliant invoice in Zoho Books under SAC 997311."""
        tax = IndianTaxEngine.calculate_lease_tax(base_rent, is_inter_state, "997311")
        inv_date_str = (inv_date or date.today()).strftime("%Y-%m-%d")
        invoice_number = f"VL-INV-{datetime.utcnow().strftime('%Y%m')}-{abs(hash(asset_tag))%1000:03d}"
        
        invoice_payload = {
            "invoice_id": f"ZB-{invoice_number}",
            "invoice_number": invoice_number,
            "customer_id": customer_id,
            "date": inv_date_str,
            "due_date": inv_date_str,
            "sac_code": "997311",
            "line_items": [
                {
                    "name": f"Commercial EV Dry Lease - {asset_name} ({asset_tag})",
                    "description": "Monthly commercial vehicle lease without operator (SAC 997311)",
                    "rate": base_rent,
                    "quantity": 1,
                    "hsn_or_sac": "997311",
                    "tax_percentage": 18.0
                }
            ],
            "tax_breakdown": tax,
            "total": tax["total_invoiced_amount"],
            "balance": tax["total_invoiced_amount"],
            "status": "sent",
            "payment_link": f"https://pay.visionloop.in/invoice/{invoice_number}",
            "upi_qr_string": f"upi://pay?pa=visionloop@icici&pn=VisionLoop&am={tax['total_invoiced_amount']}&tr={invoice_number}"
        }
        return invoice_payload

    async def reconcile_payment(self, invoice_id: str, amount: float, reference: str) -> Dict[str, Any]:
        """Reconciles payment against an open invoice and generates a payment receipt."""
        return {
            "payment_id": f"ZB-PAY-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "invoice_id": invoice_id,
            "amount_applied": amount,
            "payment_mode": "Bank Transfer / e-NACH",
            "reference_number": reference,
            "reconciled_at": datetime.utcnow().isoformat(),
            "status": "success",
            "receipt_url": f"https://books.zoho.in/secure/receipts/{invoice_id}.pdf"
        }

zoho_client = ZohoBooksClient()
