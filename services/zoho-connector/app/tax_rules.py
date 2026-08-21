from typing import Dict, Any

class IndianTaxEngine:
    """Handles SAC code computation and GST (CGST/SGST/IGST) calculations for commercial leasing."""
    
    @staticmethod
    def calculate_lease_tax(
        base_rent: float = 72000.00,
        is_inter_state: bool = False,
        sac_code: str = "997311"
    ) -> Dict[str, Any]:
        """
        Calculates GST for transport vehicle lease without operator (SAC 997311) at 18%.
        """
        gst_rate = 18.0
        tax_amount = round(base_rent * (gst_rate / 100.0), 2)
        
        if is_inter_state:
            cgst = 0.0
            sgst = 0.0
            igst = tax_amount
        else:
            cgst = round(tax_amount / 2.0, 2)
            sgst = round(tax_amount / 2.0, 2)
            igst = 0.0
            
        total_invoiced = round(base_rent + tax_amount, 2)
        
        return {
            "sac_code": sac_code,
            "description": "Leasing or rental services of transport vehicles without operator (Tata Intra EV)",
            "base_amount": base_rent,
            "gst_rate_pct": gst_rate,
            "cgst_rate_pct": 0.0 if is_inter_state else 9.0,
            "cgst_amount": cgst,
            "sgst_rate_pct": 0.0 if is_inter_state else 9.0,
            "sgst_amount": sgst,
            "igst_rate_pct": 18.0 if is_inter_state else 0.0,
            "igst_amount": igst,
            "total_tax_amount": tax_amount,
            "total_invoiced_amount": total_invoiced,
            "currency": "INR",
            "itc_note": "100% Full Input Tax Credit (ITC) claimable by Vision Loop on commercial EV purchase, charging & repair"
        }
