# VisionLoop Legal (`visionloop-legal`)
*Reusable Indian LegalTech, Contract Synthesis & KYC Verification Engine*

---

## ⚡ Features
- **Dynamic Lease Synthesizer:** Instantly merges asset specs, KYC parameters, and SAC 997311 billing schedules into standard Indian commercial agreements.
- **Indian KYC Validator:** Performs checksum verification on PAN (Format & Entity Type), GSTIN (State Codes & Check Digits), and Aadhaar hashes.
- **Compliance Auditor:** Validates MSME Udyam service classifications and statutory clauses under Sections 15/16 of the MSMED Act.

---

## 💻 Quick Usage Example

```python
from visionloop_legal import LeaseAgreementSynthesizer, KYCValidator

# 1. Validate Lessee GSTIN & PAN
is_pan_valid, pan_type = KYCValidator.validate_pan("AAACS1234F")
print("PAN Valid:", is_pan_valid, "Entity:", pan_type) # True, 'Company'

is_gstin_valid, state = KYCValidator.validate_gstin("07AAACS1234F1Z5")
print("GSTIN Valid:", is_gstin_valid, "State:", state) # True, 'Delhi'

# 2. Synthesize Lease Agreement
contract_md = LeaseAgreementSynthesizer.synthesize(
    lessor_name="Vision Loop",
    lessee_name="SwiftLogix Express Delivery Pvt Ltd",
    asset_name="Tata Intra EV Commercial Goods Carriage",
    reg_number="DL-01-EV-2026",
    base_rent=72000.0,
    deposit=144000.0
)
print("Contract Characters:", len(contract_md))
```
