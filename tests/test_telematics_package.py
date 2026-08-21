import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "packages" / "visionloop-telematics"))

from visionloop_telematics import (
    BatterySLAEngine, 
    GeofenceEngine, 
    MaintenanceScheduler, 
    ImmobilizerSafetyProtocol, 
    StreamParser
)

def test_battery_sla_engine():
    # Nominal healthy conditions
    health = BatterySLAEngine.evaluate_telemetry(soc_pct=92.5, soh_pct=99.4, battery_temp_c=28.5)
    assert health.status == "COMPLIANT"
    assert health.health_score > 90.0
    assert len(health.violations) == 0

    # Overheating SLA breach condition (>42C)
    hot = BatterySLAEngine.evaluate_telemetry(soc_pct=92.5, soh_pct=99.4, battery_temp_c=45.0)
    assert hot.status in ["WARNING", "VIOLATION"]
    assert len(hot.violations) > 0

def test_geofence_engine():
    # Inside Delhi NCR perimeter (center 28.6139, 77.2090)
    inside = GeofenceEngine.is_within_radius(current_lat=28.6139, current_lng=77.2090)
    assert inside is True

    # Far away in Mumbai
    outside = GeofenceEngine.is_within_radius(current_lat=19.0760, current_lng=72.8777)
    assert outside is False

def test_maintenance_scheduler():
    # 3,420 km - not due yet for 10,000 km service
    m1 = MaintenanceScheduler.check_milestone(current_odometer_km=3420.0, interval_km=10000.0)
    assert m1.service_required is False

    # 10,050 km - service due!
    m2 = MaintenanceScheduler.check_milestone(current_odometer_km=10050.0, interval_km=10000.0)
    assert m2.service_required is True

def test_immobilizer_safety_protocol():
    # Speed == 0.0 -> Safe to immobilize
    safe, msg = ImmobilizerSafetyProtocol.can_safely_immobilize(speed_kmh=0.0)
    assert safe is True

    # Speed > 0.0 -> Safety block (Zero in-motion power cut-off)
    unsafe, msg = ImmobilizerSafetyProtocol.can_safely_immobilize(speed_kmh=24.5)
    assert unsafe is False
