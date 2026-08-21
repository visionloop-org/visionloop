# VisionLoop Comms (`visionloop-comms`)
*Reusable Omnichannel AI Messaging & WhatsApp Collections Engine*

---

## ⚡ Features
- **Dynamic Collection Copy:** Generates context-aware billing notices across escalation stages (`FRIENDLY_DUE`, `DUE_DATE`, `OVERDUE_NOTICE`, `ESCALATION_LEVEL2`).
- **Dynamic UPI Payment Links:** Injects instant NPCI UPI deep-links and QR strings into WhatsApp payload structures.
- **WhatsApp Cloud API Dispatcher:** Standardized payload format for Meta WhatsApp Business Cloud API.

---

## 💻 Quick Usage Example

```python
from visionloop_comms import CollectionReminderEngine, WhatsAppDispatcher

# 1. Generate Contextual WhatsApp Reminder
msg = CollectionReminderEngine.generate_message(
    lessee_name="SwiftLogix Express Delivery",
    invoice_number="VL-INV-2026-08-001",
    amount=84960.0,
    due_date="05 Aug, 2026",
    stage="DUE_DATE",
    upi_link="upi://pay?pa=visionloop@icici&am=84960.00"
)
print("Message:", msg)
```
