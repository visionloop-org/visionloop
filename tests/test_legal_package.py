import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "packages" / "visionloop-legal"))

from visionloop_legal import (
    KYCValidator, 
    LeaseAgreementSynthesizer, 
    StatutoryComplianceAuditor
)

def test_kyc_validator():
    # Valid Company PAN
    valid_pan, entity = KYCValidator.validate_pan("AAACS1234F")
    assert valid_pan is True
    assert entity == "Company"

    # Invalid PAN format
    invalid_pan, _ = KYCValidator.validate_pan("12345ABCDE")
    assert invalid_pan is False

    # Valid Delhi GSTIN
    valid_gstin, state = KYCValidator.validate_gstin("07AAACS1234F1Z5")
    assert valid_gstin is True
    assert state == "Delhi"

def test_lease_agreement_synthesizer():
    contract = LeaseAgreementSynthesizer.synthesize(
        lessor_name="Vision Loop",
        lessee_name="SwiftLogix Express Delivery Pvt Ltd",
        asset_name="Tata Intra EV",
        reg_number="DL-01-EV-2026",
        base_rent=72000.0,
        deposit=144000.0,
        lease_months=24
    )
    assert "COMMERCIAL ASSET LEASE AGREEMENT" in contract
    assert "₹72,000.00" in contract
    assert "₹84,960.00" in contract
    assert "DL-01-EV-2026" in contract

def test_statutory_compliance_auditor():
    audit = StatutoryComplianceAuditor.audit_enterprise(
        has_udyam=True,
        nic_code="77101",
        has_gstin=True,
        sac_code="997311",
        has_bank_current_ac=True
    )
    assert audit["is_fully_compliant"] is True
    assert audit["msmed_45_day_clause_active"] is True
    assert audit["itc_full_claimable"] is True
