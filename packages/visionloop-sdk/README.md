# VisionLoop Master SDK (`visionloop-sdk`)
*Unified Automation SDK for Asset Rental, FinTech, Fleet IoT & Legal Operations*

---

## ⚡ Overview
`visionloop-sdk` is the top-level orchestration library providing a unified interface across all proprietary Vision Loop IP engines:
* 💰 **Finance & Tax Engine:** Zoho Books, SAC 997311 GST, Sinking Fund Treasury, MSMED Act 45-day interest.
* 🚗 **Telematics & Battery Engine:** CAN-Bus stream parsing, battery warranty SLA scoring, 2dsphere geofencing, standstill immobilization.
* ⚖️ **Legal & KYC Engine:** Commercial lease synthesis, Indian PAN/GSTIN validation, DPDP Act compliance.
* 📱 **Comms & Messaging Engine:** Automated conversational WhatsApp collection dispatch.

---

## 💻 Quick Start Example

```python
from visionloop_sdk import VisionLoopSDK

# Initialize SDK
vl = VisionLoopSDK()

# 1. Finance: Compute SAC 997311 GST breakdown
tax = vl.finance.tax.calculate(base_rent=72000.0)
print(f"Total Invoiced: ₹{tax.total_invoiced_amount} (GST: ₹{tax.total_tax_amount})")

# 2. Legal: Validate Lessee GSTIN
is_valid, state = vl.legal.kyc.validate_gstin("07AAACS1234F1Z5")
print(f"GSTIN Valid: {is_valid} ({state})")

# 3. Telematics: Check Battery Warranty SLA
health = vl.telematics.battery.evaluate_telemetry(
    soc_pct=92.5,
    soh_pct=99.4,
    battery_temp_c=29.2
)
print(f"Battery Status: {health.status}")

# 4. Comms: Generate WhatsApp UPI Reminder
msg = vl.comms.reminders.generate_message(
    lessee_name="SwiftLogix Express Delivery",
    invoice_number="VL-INV-2026-08-001",
    amount=84960.0,
    due_date="05 Aug, 2026",
    upi_link="upi://pay?pa=visionloop@icici&am=84960.00"
)
print(msg)
```
