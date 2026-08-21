"""
VisionLoop Telematics Module
Reusable IoT Fleet Telematics, Battery SLA & Remote Security Protocol
"""

from .battery_sla import BatterySLAEngine, BatteryHealthEvaluation
from .geofence import GeofenceEngine
from .maintenance_scheduler import MaintenanceScheduler, ServiceMilestone
from .immobilizer_protocol import ImmobilizerSafetyProtocol
from .stream_parser import StreamParser, NormalizedTelemetry

__all__ = [
    "BatterySLAEngine",
    "BatteryHealthEvaluation",
    "GeofenceEngine",
    "MaintenanceScheduler",
    "ServiceMilestone",
    "ImmobilizerSafetyProtocol",
    "StreamParser",
    "NormalizedTelemetry"
]
