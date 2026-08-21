from pydantic import BaseModel

class SinkingFundSummary(BaseModel):
    monthly_revenue_base: float
    allocation_pct: float
    monthly_contribution_inr: float
    months_elapsed: int
    accumulated_reserve_inr: float
    estimated_interest_earned_inr: float
    total_replacement_fund_inr: float
    target_replacement_cost_inr: float
    funding_progress_pct: float

class SinkingFundCalculator:
    """Computes treasury sinking fund accumulations for asset replacement cycles."""
    
    @staticmethod
    def calculate_reserve(
        monthly_revenue: float = 72000.00,
        allocation_pct: float = 15.0,
        months: int = 12,
        annual_yield_pct: float = 6.8,
        target_asset_cost: float = 1200000.00
    ) -> SinkingFundSummary:
        monthly_contribution = round(monthly_revenue * (allocation_pct / 100.0), 2)
        total_principal = monthly_contribution * months
        
        # Approximate compound interest for monthly SIP
        monthly_rate = (annual_yield_pct / 100.0) / 12.0
        future_value = 0.0
        for m in range(months):
            future_value = (future_value + monthly_contribution) * (1.0 + monthly_rate)
            
        interest_earned = round(future_value - total_principal, 2)
        total_fund = round(future_value, 2)
        progress = round((total_fund / target_asset_cost) * 100.0, 1) if target_asset_cost > 0 else 100.0
        
        return SinkingFundSummary(
            monthly_revenue_base=monthly_revenue,
            allocation_pct=allocation_pct,
            monthly_contribution_inr=monthly_contribution,
            months_elapsed=months,
            accumulated_reserve_inr=round(total_principal, 2),
            estimated_interest_earned_inr=interest_earned,
            total_replacement_fund_inr=total_fund,
            target_replacement_cost_inr=target_asset_cost,
            funding_progress_pct=progress
        )
