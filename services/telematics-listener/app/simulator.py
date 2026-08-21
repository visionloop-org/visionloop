import asyncio
import httpx
import math
import random
from typing import Dict, Any
from app.config import settings

# Waypoints simulating commercial logistics delivery route in Delhi NCR
DELHI_ROUTE_WAYPOINTS = [
    {"lat": 28.5355, "lng": 77.2660, "name": "Okhla Phase-III Hub"},
    {"lat": 28.5700, "lng": 77.2400, "name": "Lajpat Nagar Commercial Ring"},
    {"lat": 28.6139, "lng": 77.2090, "name": "Connaught Place Central Ring"},
    {"lat": 28.6353, "lng": 77.2773, "name": "Mayur Vihar Logistics Node"},
    {"lat": 28.6280, "lng": 77.3649, "name": "Noida Sector 62 Delivery Cluster"},
    {"lat": 28.4595, "lng": 77.0266, "name": "Gurugram Cyber Hub Corridor"}
]

class VehicleTelemetrySimulator:
    def __init__(self, asset_tag: str = "VL-EV-001"):
        self.asset_tag = asset_tag
        self.waypoint_index = 0
        self.current_lat = 28.5355
        self.current_lng = 77.2660
        self.soc_pct = 92.5
        self.soh_pct = 99.4
        self.odometer_km = 3420.0
        self.battery_temp_c = 29.2
        self.speed_kmh = 28.0
        self.charging_status = "DISCHARGING"
        self.is_running = True

    async def step(self) -> Dict[str, Any]:
        """Advances vehicle telemetry by one simulation step."""
        target = DELHI_ROUTE_WAYPOINTS[self.waypoint_index]
        
        # Smooth movement interpolation
        d_lat = target["lat"] - self.current_lat
        d_lng = target["lng"] - self.current_lng
        distance = math.sqrt(d_lat**2 + d_lng**2)

        if distance < 0.005:
            # Switch to next waypoint
            self.waypoint_index = (self.waypoint_index + 1) % len(DELHI_ROUTE_WAYPOINTS)
        else:
            step_size = 0.002
            self.current_lat += (d_lat / distance) * step_size
            self.current_lng += (d_lng / distance) * step_size

        # Speed and Odometer progression
        self.speed_kmh = round(random.uniform(22.0, 48.0), 1)
        self.odometer_km = round(self.odometer_km + (self.speed_kmh * (settings.SIMULATION_INTERVAL_SEC / 3600.0)), 2)

        # Battery Drainage & Charging Logic
        if self.charging_status == "DISCHARGING":
            self.soc_pct = max(5.0, round(self.soc_pct - random.uniform(0.05, 0.15), 2))
            self.battery_temp_c = round(28.0 + (self.speed_kmh / 15.0) + random.uniform(-0.5, 0.5), 1)
            if self.soc_pct <= 18.0:
                self.charging_status = "CHARGING_FAST"
        else:
            # Fast charging at 50kW DC fast charger
            self.soc_pct = min(100.0, round(self.soc_pct + 1.2, 2))
            self.battery_temp_c = 34.5
            self.speed_kmh = 0.0
            if self.soc_pct >= 95.0:
                self.charging_status = "DISCHARGING"

        telemetry_payload = {
            "asset_id": self.asset_tag,
            "latitude": round(self.current_lat, 6),
            "longitude": round(self.current_lng, 6),
            "speed_kmh": self.speed_kmh,
            "soc_pct": self.soc_pct,
            "battery_temp_c": self.battery_temp_c,
            "battery_voltage": round(370.0 + (self.soc_pct * 0.3), 1),
            "odometer_km": self.odometer_km,
            "ignition_on": self.charging_status == "DISCHARGING",
            "charging_status": self.charging_status,
            "fault_codes": None
        }

        # Transmit to Core API
        async with httpx.AsyncClient() as client:
            try:
                await client.post(f"{settings.CORE_API_URL}/telemetry/ingest", json=telemetry_payload)
            except Exception:
                pass

        return telemetry_payload

simulator = VehicleTelemetrySimulator()
