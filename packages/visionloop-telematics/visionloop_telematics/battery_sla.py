from typing import Optional, List
from pydantic import BaseModel

class BatteryHealthEvaluation(BaseModel):
    soc_pct: float
    soh_pct: float
    battery_temp_c: float
    dc_fast_charge_ratio_pct: float
    health_score: float
    status: str # COMPLIANT, WARNING, VIOLATION
    violations: List[str]
    recommendation: str

class BatterySLAEngine:
    """Evaluates EV battery operational compliance with OEM warranty clauses."""
    
    @staticmethod
    def evaluate_telemetry(
        soc_pct: float,
        soh_pct: float,
        battery_temp_c: float,
        dc_fast_charge_count: int = 10,
        ac_slow_charge_count: int = 5,
        max_dc_ratio: float = 70.0,
        max_temp_c: float = 42.0
    ) -> BatteryHealthEvaluation:
        violations = []
        
        # 1. Charge Ratio Check
        total_charges = dc_fast_charge_count + ac_slow_charge_count
        dc_ratio = round((dc_fast_charge_count / total_charges * 100.0), 1) if total_charges > 0 else 50.0
        if dc_ratio > max_dc_ratio:
            violations.append(f"DC Fast Charging Ratio ({dc_ratio}%) exceeds OEM threshold ({max_dc_ratio}%)")
            
        # 2. Temperature Threshold
        if battery_temp_c > max_temp_c:
            violations.append(f"Operating temperature ({battery_temp_c}°C) exceeds maximum limit ({max_temp_c}°C)")
            
        # 3. Deep Discharge
        if soc_pct < 10.0:
            violations.append(f"Deep discharge detected (SoC: {soc_pct}%). Habitual deep discharge degrades cell chemistry.")
            
        # Compute Health Score (0 - 100)
        penalty = len(violations) * 15.0
        health_score = max(0.0, round(soh_pct - penalty, 1))
        
        status = "COMPLIANT" if not violations else ("WARNING" if len(violations) == 1 else "VIOLATION")
        recommendation = "Operation optimal." if not violations else "Conduct overnight AC slow charge for cell balancing and avoid extreme fast-charging cycles."
        
        return BatteryHealthEvaluation(
            soc_pct=soc_pct,
            soh_pct=soh_pct,
            battery_temp_c=battery_temp_c,
            dc_fast_charge_ratio_pct=dc_ratio,
            health_score=health_score,
            status=status,
            violations=violations,
            recommendation=recommendation
        )
