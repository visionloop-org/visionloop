# VisionLoop Finance (`visionloop-finance`)
*Reusable Indian Financial, Tax, Zoho Books & Treasury Automation Engine*

---

## ⚡ Features
- **Zoho Books Automation:** Auto-generate recurring GST invoices, contacts, and payment receipts.
- **Indian Tax Engine:** Calculates SAC 997311 / 9966 GST breakdowns (18% CGST/SGST/IGST) and Input Tax Credit (ITC) eligibility.
- **15% Treasury Sinking Fund:** Computes liquid capital reserves needed to replace assets or battery packs at month 36.
- **MSMED Act Calculator:** Computes statutory compound interest (at 3x RBI Bank Rate) for invoices overdue beyond 45 days.
- **Dynamic UPI QR Generator:** Generates NPCI-compliant `upi://pay` strings and instant checkout links.

---

## 💻 Quick Usage Example

```python
from visionloop_finance import IndianTaxEngine, SinkingFundCalculator, MSMEInterestCalculator, UPIGenerator

# 1. Calculate SAC 997311 GST Breakdown
tax = IndianTaxEngine.calculate(base_rent=72000.0, is_inter_state=False)
print("Total Invoiced Amount:", tax.total_invoiced_amount) # 84960.0

# 2. Compute 15% Sinking Fund for 12 months
sinking = SinkingFundCalculator.calculate_reserve(monthly_revenue=72000.0, months=12)
print("Accumulated Capital:", sinking.accumulated_reserve_inr) # 129600.0

# 3. Dynamic UPI Payment String
upi = UPIGenerator.generate_qr_string(
    vpa="visionloop@icici",
    payee_name="Vision Loop",
    amount=84960.0,
    invoice_number="VL-INV-2026-08-001"
)
print("UPI String:", upi)
```
