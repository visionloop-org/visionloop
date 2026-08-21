import httpx
from datetime import datetime, date
from typing import Dict, Any, Optional
from .tax_engine import IndianTaxEngine

class StandaloneZohoBooksClient:
    """
    Reusable Zoho Books API Client for B2B recurring invoicing, 
    contact management, and payment reconciliation.
    """
    def __init__(
        self,
        client_id: str = "",
        client_secret: str = "",
        refresh_token: str = "",
        org_id: str = "",
        api_domain: str = "https://books.zoho.in/api/v3",
        accounts_domain: str = "https://accounts.zoho.in"
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.org_id = org_id
        self.api_domain = api_domain
        self.accounts_domain = accounts_domain

    def create_invoice_payload(
        self,
        customer_id: str,
        item_name: str,
        asset_tag: str,
        base_rent: float = 72000.00,
        is_inter_state: bool = False,
        sac_code: str = "997311",
        inv_date: Optional[date] = None
    ) -> Dict[str, Any]:
        tax = IndianTaxEngine.calculate(base_rent, is_inter_state, sac_code, item_name)
        date_str = (inv_date or date.today()).strftime("%Y-%m-%d")
        inv_num = f"VL-INV-{datetime.utcnow().strftime('%Y%m')}-{abs(hash(asset_tag))%1000:03d}"
        
        return {
            "invoice_number": inv_num,
            "customer_id": customer_id,
            "date": date_str,
            "due_date": date_str,
            "sac_code": sac_code,
            "line_items": [
                {
                    "name": f"{item_name} ({asset_tag})",
                    "rate": base_rent,
                    "quantity": 1,
                    "hsn_or_sac": sac_code,
                    "tax_percentage": tax.gst_rate_pct
                }
            ],
            "tax_summary": tax.model_dump(),
            "total_amount": tax.total_invoiced_amount,
            "status": "sent"
        }
