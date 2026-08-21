import urllib.parse
from typing import Optional

class UPIGenerator:
    """Generates NPCI-compliant dynamic UPI payment URIs and QR payload strings."""
    
    @staticmethod
    def generate_qr_string(
        vpa: str = "visionloop@icici",
        payee_name: str = "Vision Loop",
        amount: float = 84960.00,
        invoice_number: str = "VL-INV-2026-08-001",
        note: Optional[str] = None
    ) -> str:
        transaction_note = note or f"Lease Rent Inv {invoice_number}"
        
        params = {
            "pa": vpa,
            "pn": payee_name,
            "am": f"{amount:.2f}",
            "cu": "INR",
            "tr": invoice_number,
            "tn": transaction_note
        }
        
        query_string = urllib.parse.urlencode(params)
        return f"upi://pay?{query_string}"
    
    @staticmethod
    def generate_payment_link(
        domain: str = "https://pay.visionloop.in",
        invoice_number: str = "VL-INV-2026-08-001"
    ) -> str:
        return f"{domain}/invoice/{invoice_number}"
