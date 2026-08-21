# VisionLoop Telematics (`visionloop-telematics`)
*Reusable IoT Fleet Telematics, EV Battery Preservation & Standstill Security Engine*

---

## ⚡ Features
- **Battery Warranty SLA Scorer:** Protects OEM battery warranties by checking DC/AC charge ratios, SoC operating buffers (15%–90%), and cell temperature limits.
- **Geofence Breach Engine:** High-speed haversine distance and point-radius boundary checker.
- **Predictive Maintenance Scheduler:** Automatically raises servicing tickets at 10,000 km milestones.
- **Ethical Standstill Immobilizer Protocol:** Enforces remote cut-off *strictly* when vehicle is verified at `0.0 km/h` standstill.
- **CAN-Bus Stream Parser:** Normalizes raw OBD-II and CAN frames into structured telematics documents.

---

## 💻 Quick Usage Example

```python
from visionloop_telematics import (
    BatterySLAEngine, 
    GeofenceEngine, 
    ImmobilizerSafetyProtocol,
    StreamParser
)

# 1. Evaluate Battery Health
health = BatterySLAEngine.evaluate_telemetry(
    soc_pct=92.5,
    soh_pct=99.4,
    battery_temp_c=29.2,
    dc_fast_charge_count=14,
    ac_slow_charge_count=10
)
print("Battery Status:", health.status) # "COMPLIANT"

# 2. Check Geofence
in_bounds = GeofenceEngine.is_within_radius(
    current_lat=28.6139, current_lng=77.2090,
    center_lat=28.6139, center_lng=77.2090,
    radius_km=80.0
)
print("Within Perimeter:", in_bounds) # True

# 3. Verify Immobilizer Safety (Prevents in-motion cut-offs)
can_immobilize, reason = ImmobilizerSafetyProtocol.can_safely_immobilize(
    speed_kmh=0.0,
    ignition_on=False
)
print("Safe to Immobilize:", can_immobilize) # True
```
