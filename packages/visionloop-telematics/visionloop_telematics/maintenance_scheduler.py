from pydantic import BaseModel

class ServiceMilestone(BaseModel):
    current_odometer_km: float
    last_serviced_km: float
    next_due_km: float
    km_until_service: float
    service_required: bool
    service_type: str

class MaintenanceScheduler:
    """Calculates periodic OEM servicing intervals (10,000 km for commercial EVs)."""
    
    @staticmethod
    def check_milestone(
        current_odometer_km: float,
        last_serviced_km: float = 0.0,
        interval_km: float = 10000.0
    ) -> ServiceMilestone:
        next_due = last_serviced_km + interval_km
        remaining = round(next_due - current_odometer_km, 2)
        required = current_odometer_km >= next_due or remaining <= 500.0 # Advance warning within 500km
        
        service_type = "OEM 10,000 KM Major Inspection & Coolant Check" if required else "Nominal Operating Interval"
        
        return ServiceMilestone(
            current_odometer_km=current_odometer_km,
            last_serviced_km=last_serviced_km,
            next_due_km=next_due,
            km_until_service=remaining,
            service_required=required,
            service_type=service_type
        )
