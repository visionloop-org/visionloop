from typing import Dict, Any, List, Optional
from visionloop_sdk.swarm.models import (
    AgentRole, 
    MessageType, 
    AgentMessage, 
    AgentVerificationResult, 
    SwarmExecutionReceipt
)
from visionloop_sdk.swarm.executive_agent import ChiefExecutiveSwarmAgent
from visionloop_sdk.swarm.verification_agent import ChiefAuditorVerificationAgent
from visionloop_sdk.swarm.operational_agents import (
    FleetOperationsAgent,
    TreasuryFinanceAgent,
    LegalComplianceAgent,
    SoftwareEngineeringAgent,
    YouTubeMarketingAgent
)

class SwarmOrchestrator:
    """
    High-level entry point for the Vision Loop Hierarchical Multi-Agent Swarm.
    Provides execution, inter-agent dialogue simulation, and verification audit receipts.
    """
    def __init__(self):
        self.executive = ChiefExecutiveSwarmAgent()

    def list_hierarchy(self) -> List[Dict[str, Any]]:
        return [
            {
                "tier": "Tier 1: Strategic Governance",
                "role": AgentRole.CHIEF_EXECUTIVE.value,
                "name": self.executive.name,
                "description": self.executive.description,
                "authority": "Master Swarm Coordinator, Task Decomposition, Executive Decisions"
            },
            {
                "tier": "Tier 2: Supervisory Verification & Audit",
                "role": AgentRole.CHIEF_AUDITOR.value,
                "name": self.executive.auditor.name,
                "description": self.executive.auditor.description,
                "authority": "Independent Inquest, Q&A Cross-Examination, Invariant Verification"
            },
            {
                "tier": "Tier 3: Operational Domain Sentinels",
                "agents": [
                    {
                        "role": AgentRole.FLEET_OPERATIONS.value,
                        "name": self.executive.fleet_agent.name,
                        "description": self.executive.fleet_agent.description
                    },
                    {
                        "role": AgentRole.TREASURY_FINANCE.value,
                        "name": self.executive.treasury_agent.name,
                        "description": self.executive.treasury_agent.description
                    },
                    {
                        "role": AgentRole.LEGAL_COMPLIANCE.value,
                        "name": self.executive.legal_agent.name,
                        "description": self.executive.legal_agent.description
                    },
                    {
                        "role": AgentRole.SOFTWARE_ENGINEERING.value,
                        "name": self.executive.software_agent.name,
                        "description": self.executive.software_agent.description
                    },
                    {
                        "role": AgentRole.YOUTUBE_MARKETING.value,
                        "name": self.executive.youtube_agent.name,
                        "description": self.executive.youtube_agent.description
                    }
                ]
            }
        ]

    async def execute_task_with_cross_examination(self, goal: str, domain: str = "finance", context: Optional[Dict[str, Any]] = None) -> SwarmExecutionReceipt:
        """Runs Phase 1 (Gather) -> Phase 2 (Plan) -> Phase 3 (Grill & Verify) -> Phase 4 (Present Proposal to Proprietor)."""
        return await self.executive.execute_hierarchical_workflow(goal=goal, domain=domain, context=context)

    async def execute_approved_task(self, receipt: SwarmExecutionReceipt, proprietor_approval: bool = True) -> SwarmExecutionReceipt:
        """Runs Phase 5 (Execute upon explicit proprietor approval)."""
        return await self.executive.execute_approved_receipt(receipt=receipt, proprietor_approval=proprietor_approval)
