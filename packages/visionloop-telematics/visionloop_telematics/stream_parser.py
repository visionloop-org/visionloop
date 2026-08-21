from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel

class NormalizedTelemetry(BaseModel):
    asset_tag: str
    timestamp: datetime
    latitude: float
    longitude: float
    speed_kmh: float
    soc_pct: float
    battery_temp_c: float
    battery_voltage: float
    odometer_km: float
    ignition_on: bool
    charging_status: str

class StreamParser:
    """Normalizes raw GPS/OBD-II/CAN frames into clean schema."""
    
    @staticmethod
    def parse_raw_packet(raw_data: Dict[str, Any], default_tag: str = "VL-EV-001") -> NormalizedTelemetry:
        return NormalizedTelemetry(
            asset_tag=raw_data.get("asset_tag") or raw_data.get("device_id") or default_tag,
            timestamp=datetime.utcnow(),
            latitude=float(raw_data.get("lat") or raw_data.get("latitude", 28.6139)),
            longitude=float(raw_data.get("lng") or raw_data.get("longitude", 77.2090)),
            speed_kmh=float(raw_data.get("spd") or raw_data.get("speed_kmh", 0.0)),
            soc_pct=float(raw_data.get("soc") or raw_data.get("soc_pct", 100.0)),
            battery_temp_c=float(raw_data.get("temp") or raw_data.get("battery_temp_c", 28.5)),
            battery_voltage=float(raw_data.get("v") or raw_data.get("battery_voltage", 380.0)),
            odometer_km=float(raw_data.get("odo") or raw_data.get("odometer_km", 0.0)),
            ignition_on=bool(raw_data.get("ign") if "ign" in raw_data else raw_data.get("ignition_on", True)),
            charging_status=raw_data.get("chg") or raw_data.get("charging_status", "DISCHARGING")
        )
