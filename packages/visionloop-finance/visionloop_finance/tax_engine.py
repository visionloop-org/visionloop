from typing import Dict, Any
from pydantic import BaseModel

class TaxBreakdown(BaseModel):
    sac_code: str
    description: str
    base_amount: float
    gst_rate_pct: float
    cgst_rate_pct: float
    cgst_amount: float
    sgst_rate_pct: float
    sgst_amount: float
    igst_rate_pct: float
    igst_amount: float
    total_tax_amount: float
    total_invoiced_amount: float
    itc_eligibility: str

class IndianTaxEngine:
    """Calculates GST breakdowns for commercial asset rental under SAC 997311 or 9966."""
    
    @staticmethod
    def calculate(
        base_rent: float = 72000.00,
        is_inter_state: bool = False,
        sac_code: str = "997311",
        description: str = "Leasing of commercial transport asset without operator"
    ) -> TaxBreakdown:
        gst_rate = 18.0
        tax_amt = round(base_rent * (gst_rate / 100.0), 2)
        
        if is_inter_state:
            cgst = 0.0
            sgst = 0.0
            igst = tax_amt
            cgst_rate = 0.0
            sgst_rate = 0.0
            igst_rate = gst_rate
        else:
            cgst = round(tax_amt / 2.0, 2)
            sgst = round(tax_amt / 2.0, 2)
            igst = 0.0
            cgst_rate = 9.0
            sgst_rate = 9.0
            igst_rate = 0.0
            
        total = round(base_rent + tax_amt, 2)
        
        return TaxBreakdown(
            sac_code=sac_code,
            description=description,
            base_amount=base_rent,
            gst_rate_pct=gst_rate,
            cgst_rate_pct=cgst_rate,
            cgst_amount=cgst,
            sgst_rate_pct=sgst_rate,
            sgst_amount=sgst,
            igst_rate_pct=igst_rate,
            igst_amount=igst,
            total_tax_amount=tax_amt,
            total_invoiced_amount=total,
            itc_eligibility="100% Full Input Tax Credit (ITC) claimable under Sec 17(5)(a)"
        )
