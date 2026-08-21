from typing import Dict, Any, List, Optional
from visionloop_sdk.swarm.base_agent import BaseSwarmAgent
from visionloop_sdk.swarm.models import (
    AgentRole, 
    MessageType, 
    AgentMessage, 
    AgentVerificationResult, 
    SwarmExecutionReceipt
)
from visionloop_sdk.swarm.operational_agents import (
    FleetOperationsAgent,
    TreasuryFinanceAgent,
    LegalComplianceAgent,
    SoftwareEngineeringAgent,
    YouTubeMarketingAgent
)
from visionloop_sdk.swarm.verification_agent import ChiefAuditorVerificationAgent

class ChiefExecutiveSwarmAgent(BaseSwarmAgent):
    """
    Chief Executive Agent (Top Tier):
    Orchestrates the entire multi-agent swarm hierarchy.
    Decomposes instructions, delegates tasks to operational agents, commands the Chief Auditor
    to cross-examine proposals, and issues final certified executive decisions.
    """
    def __init__(self):
        super().__init__(
            role=AgentRole.CHIEF_EXECUTIVE,
            name="Garuda Executive Swarm Coordinator",
            description="Chief executive orchestrator governing the Vision Loop multi-agent autonomous enterprise."
        )
        self.auditor = ChiefAuditorVerificationAgent()
        self.fleet_agent = FleetOperationsAgent()
        self.treasury_agent = TreasuryFinanceAgent()
        self.legal_agent = LegalComplianceAgent()
        self.software_agent = SoftwareEngineeringAgent()
        self.youtube_agent = YouTubeMarketingAgent()

    def get_operational_agent_for_domain(self, domain: str) -> BaseSwarmAgent:
        d_lower = domain.lower()
        if any(w in d_lower for w in ["fleet", "telematics", "ev", "tata", "battery", "speed", "immobilizer"]):
            return self.fleet_agent
        if any(w in d_lower for w in ["finance", "treasury", "tax", "gst", "invoice", "sinking", "sac", "rent"]):
            return self.treasury_agent
        if any(w in d_lower for w in ["legal", "compliance", "msme", "noc", "privacy", "dpdp", "contract"]):
            return self.legal_agent
        if any(w in d_lower for w in ["software", "sdk", "test", "ci/cd", "code", "api"]):
            return self.software_agent
        if any(w in d_lower for w in ["youtube", "media", "video", "marketing", "adsense", "creator"]):
            return self.youtube_agent
        return self.treasury_agent

    async def process_task(self, task_instruction: str, context: Optional[Dict[str, Any]] = None) -> AgentMessage:
        return self.send_message(
            recipient=AgentRole.CHIEF_AUDITOR,
            msg_type=MessageType.TASK_DELEGATION,
            content=f"Executive goal initialized: {task_instruction}",
            payload=context or {}
        )

    async def execute_hierarchical_workflow(self, goal: str, domain: str, context: Optional[Dict[str, Any]] = None) -> SwarmExecutionReceipt:
        """
        Executes the full 3-tier hierarchical multi-agent workflow:
        1. Executive delegates goal to the specialized Operational Agent.
        2. Operational Agent creates a work proposal.
        3. Chief Auditor intercepts proposal and performs rigorous Q&A cross-examination.
        4. Operational Agent answers challenges with verified data.
        5. Chief Auditor certifies verification or issues rejection.
        6. Executive Agent synthesizes the certified outcome.
        """
        ctx = context or {}
        assigned_agent = self.get_operational_agent_for_domain(domain)
        all_dialogue: List[AgentMessage] = []

        # Step 1: Executive delegates task
        delegation_msg = self.send_message(
            recipient=assigned_agent.role,
            msg_type=MessageType.TASK_DELEGATION,
            content=f"Execute operational task for goal: '{goal}'",
            payload=ctx
        )
        all_dialogue.append(delegation_msg)

        # Step 2: Operational agent formulates proposal
        proposal_msg = await assigned_agent.process_task(goal, ctx)
        all_dialogue.append(proposal_msg)

        # Step 3: Chief Auditor executes Q&A cross-examination
        audit_result = await self.auditor.cross_examine_and_verify(assigned_agent, proposal_msg)
        all_dialogue.extend(audit_result.dialogue_transcript)

        # Step 4: Executive Decision
        status = "EXECUTED_AND_CERTIFIED" if audit_result.verified else "REJECTED_AUDIT_FAILURE"
        summary = (
            f"Executive Action Receipt for Goal: '{goal}'. "
            f"Assigned Worker: {assigned_agent.name} ({assigned_agent.role.value}). "
            f"Auditor: {self.auditor.name}. "
            f"Cross-Examination Rounds: {audit_result.cross_examination_rounds}. "
            f"Invariants Validated: {len(audit_result.invariants_checked)}/ {len(audit_result.invariants_checked)}. "
            f"Verdict: {'APPROVED ✓' if audit_result.verified else 'REJECTED ✗'}. "
            f"Confidence: {audit_result.confidence_score * 100:.1f}%."
        )

        exec_decision_msg = self.send_message(
            recipient=assigned_agent.role,
            msg_type=MessageType.EXECUTIVE_DECISION,
            content=summary,
            payload={"verified": audit_result.verified, "certified_payload": audit_result.certified_payload}
        )
        all_dialogue.append(exec_decision_msg)

        return SwarmExecutionReceipt(
            goal=goal,
            assigned_agents=[self.role, assigned_agent.role, self.auditor.role],
            dialogue_log=all_dialogue,
            verification=audit_result,
            final_executive_summary=summary,
            status=status
        )

    async def answer_challenge(self, challenge_question: str, proposal_context: Dict[str, Any]) -> AgentMessage:
        return self.send_message(
            recipient=AgentRole.CHIEF_AUDITOR,
            msg_type=MessageType.RESPONSE_CLARIFICATION,
            content="Executive directives are governed by immutable business guidelines and zero-corruption invariants.",
            payload=proposal_context
        )
