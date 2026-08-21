import sys
from pathlib import Path

# Add packages to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "packages" / "visionloop-finance"))

from visionloop_finance import (
    IndianTaxEngine, 
    SinkingFundCalculator, 
    MSMEInterestCalculator, 
    UPIGenerator
)

def test_indian_tax_engine():
    res = IndianTaxEngine.calculate(base_rent=72000.0, is_inter_state=False)
    assert res.base_amount == 72000.0
    assert res.cgst_amount == 6480.0
    assert res.sgst_amount == 6480.0
    assert res.igst_amount == 0.0
    assert res.total_tax_amount == 12960.0
    assert res.total_invoiced_amount == 84960.0
    assert res.sac_code == "997311"

def test_sinking_fund_calculator():
    sf = SinkingFundCalculator.calculate_reserve(
        monthly_revenue=72000.0,
        allocation_pct=15.0,
        months=36
    )
    assert sf.monthly_contribution_inr == 10800.0
    assert sf.accumulated_reserve_inr == 388800.0
    assert sf.total_replacement_fund_inr > 388800.0  # Compounding yield

def test_msme_interest_calculator():
    # 45 days is statutory limit, so 0 days overdue = no interest
    msme_no_delay = MSMEInterestCalculator.compute_statutory_penalty(
        invoice_amount=84960.0,
        overdue_days=0
    )
    assert msme_no_delay.statutory_compound_interest_inr == 0.0

    # 30 days overdue past 45-day window
    msme_delay = MSMEInterestCalculator.compute_statutory_penalty(
        invoice_amount=84960.0,
        overdue_days=30
    )
    assert msme_delay.statutory_compound_interest_inr > 0.0
    assert msme_delay.effective_annual_penalty_rate_pct == 20.25

def test_upi_generator():
    uri = UPIGenerator.generate_qr_string(
        vpa="visionloop@icici",
        payee_name="Vision Loop",
        amount=84960.0,
        invoice_number="VL-INV-2026-001"
    )
    assert "upi://pay?" in uri
    assert "pa=visionloop%40icici" in uri or "pa=visionloop@icici" in uri
    assert "am=84960.00" in uri
