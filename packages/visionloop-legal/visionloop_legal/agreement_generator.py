from datetime import datetime, timezone

class LeaseAgreementSynthesizer:
    """Synthesizes structured commercial asset lease agreements for Indian operations."""
    
    @staticmethod
    def synthesize(
        lessor_name: str = "Vision Loop",
        lessor_signatory: str = "Sapna Jaiswal (Sole Proprietor)",
        lessee_name: str = "SwiftLogix Express Delivery Pvt Ltd",
        lessee_signatory: str = "Rajesh Sharma (Director)",
        lessee_pan: str = "AAACS1234F",
        lessee_gstin: str = "07AAACS1234F1Z5",
        asset_name: str = "Tata Intra EV Commercial Goods Carriage",
        reg_number: str = "DL-01-EV-2026",
        vin: str = "MAT612345N2A09876",
        base_rent: float = 72000.00,
        gst_rate_pct: float = 18.0,
        deposit: float = 144000.00,
        lease_months: int = 24
    ) -> str:
        gst_amt = round(base_rent * (gst_rate_pct / 100.0), 2)
        total_rent = round(base_rent + gst_amt, 2)
        effective_date = datetime.now(timezone.utc).strftime("%d %B, %Y")
        
        return f"""# COMMERCIAL ASSET LEASE AGREEMENT (SAC 997311)
**Date:** {effective_date}

### PARTIES:
1. **LESSOR:** {lessor_name} (Proprietorship), represented by {lessor_signatory}.
2. **LESSEE:** {lessee_name}, PAN: {lessee_pan}, GSTIN: {lessee_gstin}, represented by {lessee_signatory}.

---

### COMMERCIAL TERMS:
* **Asset:** {asset_name} (Registration: {reg_number}, VIN: {vin})
* **Lease Duration:** {lease_months} Months
* **Base Monthly Rent:** ₹{base_rent:,.2f}
* **GST @ {gst_rate_pct}% (SAC 997311):** ₹{gst_amt:,.2f}
* **Total Monthly Invoiced:** ₹{total_rent:,.2f}
* **Refundable Escrow Security Deposit:** ₹{deposit:,.2f}

---

### STATUTORY & OPERATING CLAUSES:
1. **MSMED Act Protection:** In accordance with Sections 15 and 16 of the MSMED Act, 2006, monthly invoices must be settled within 45 days. Overdue balances attract 3x RBI bank rate compounding interest.
2. **Battery Warranty SLA:** The Lessee shall observe a maximum 70% DC fast charging ratio and avoid deep discharge below 10% SoC.
3. **Standstill Immobilizer Consent:** Remote engine cut-off is strictly enforced only when vehicle is stationary at 0.0 km/h in case of default.
"""
