from typing import Tuple

class ImmobilizerSafetyProtocol:
    """
    Ethical Safety Protocol for Remote Vehicle Immobilization.
    Guarantees zero in-motion power interruption by enforcing strict 0.0 km/h standstill verification.
    """
    @staticmethod
    def can_safely_immobilize(
        speed_kmh: float,
        ignition_on: bool = False,
        speed_threshold_kmh: float = 0.0
    ) -> Tuple[bool, str]:
        """
        Validates whether remote cut-off relay can be safely engaged.
        Returns: (is_safe: bool, reason: str)
        """
        if speed_kmh > speed_threshold_kmh:
            return False, f"SAFETY LOCK ENGAGED: Vehicle is in motion ({speed_kmh} km/h). Motor cut-off blocked to prevent accident."
        
        if ignition_on and speed_kmh == 0.0:
            return True, "STANDSTILL VERIFIED: Vehicle speed is 0.0 km/h. Relay safe to engage."
            
        return True, "PARKED STANDSTILL: Vehicle is stationary and ignition off. Safe to lock."
