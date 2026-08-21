from pydantic import BaseModel

class MSMEPenaltySummary(BaseModel):
    invoice_amount: float
    due_days_allowed: int
    overdue_days: int
    rbi_bank_rate_pct: float
    statutory_multiplier: float
    effective_annual_penalty_rate_pct: float
    statutory_compound_interest_inr: float
    total_amount_payable_inr: float
    legal_statute: str

class MSMEInterestCalculator:
    """
    Computes statutory compounding interest for overdue receivables
    under Sections 15 & 16 of the MSMED Act, 2006 (3x RBI Bank Rate).
    """
    @staticmethod
    def compute_statutory_penalty(
        invoice_amount: float = 84960.00,
        overdue_days: int = 30,
        rbi_bank_rate_pct: float = 6.75
    ) -> MSMEPenaltySummary:
        statutory_multiplier = 3.0
        effective_annual_rate = rbi_bank_rate_pct * statutory_multiplier # e.g. 20.25%
        
        # Monthly compounding interest as per MSMED Act Sec 16
        monthly_rate = (effective_annual_rate / 100.0) / 12.0
        months_fraction = overdue_days / 30.0
        
        compounded_total = invoice_amount * ((1.0 + monthly_rate) ** months_fraction)
        statutory_interest = round(compounded_total - invoice_amount, 2)
        total_payable = round(invoice_amount + statutory_interest, 2)
        
        return MSMEPenaltySummary(
            invoice_amount=invoice_amount,
            due_days_allowed=45,
            overdue_days=overdue_days,
            rbi_bank_rate_pct=rbi_bank_rate_pct,
            statutory_multiplier=statutory_multiplier,
            effective_annual_penalty_rate_pct=effective_annual_rate,
            statutory_compound_interest_inr=statutory_interest,
            total_amount_payable_inr=total_payable,
            legal_statute="MSMED Act, 2006 (Sections 15 & 16)"
        )
