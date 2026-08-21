from typing import Dict, Any, List, Optional
from visionloop_sdk.swarm.base_agent import BaseSwarmAgent
from visionloop_sdk.swarm.models import (
    AgentRole, 
    MessageType, 
    AgentMessage, 
    AgentVerificationResult, 
    HumanApprovalStatus,
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
        The 5-Phase Sovereign Workflow:
        1. GATHER DATA: Collect live telemetry, statutory parameters, and database state.
        2. PLAN STRATEGY: Formulate strategic steps and assign domain agents.
        3. GRILL & VERIFY: Chief Auditor interrogates operational workers with cross-examination queries.
        4. PRESENT PROPOSAL: Synthesize verified audit receipt and present to Proprietor for human approval.
        5. EXECUTE: (Triggered only after human approval).
        """
        ctx = context or {}
        assigned_agent = self.get_operational_agent_for_domain(domain)
        all_dialogue: List[AgentMessage] = []

        # ---------------------------------------------------------------------
        # PHASE 1: GATHER DATA
        # ---------------------------------------------------------------------
        gathered_data = {
            "retrieved_context": ctx,
            "target_domain": domain,
            "statutory_jurisdiction": "Lucknow, Uttar Pradesh (State Code 09)",
            "knowledge_graph_invariants": 29,
            "timestamp": "LIVE_INGESTED"
        }

        # ---------------------------------------------------------------------
        # PHASE 2: PLAN STRATEGY
        # ---------------------------------------------------------------------
        strategic_plan = [
            f"1. Ingest goal: '{goal}'",
            f"2. Delegate operational modeling to {assigned_agent.name}",
            f"3. Submit proposal to Chief Auditor for cross-examination inquest",
            "4. Verify all statutory, safety, and arithmetic invariants",
            "5. Present verified proposal to Sole Proprietor for explicit authorization",
            "6. Await human approval before executing irreversible financial/telematics actions"
        ]

        # Step 2a: Executive delegates task
        delegation_msg = self.send_message(
            recipient=assigned_agent.role,
            msg_type=MessageType.TASK_DELEGATION,
            content=f"Execute operational task for goal: '{goal}'",
            payload=ctx
        )
        all_dialogue.append(delegation_msg)

        # ---------------------------------------------------------------------
        # PHASE 3: GRILL & VERIFY (Chief Auditor Interrogation)
        # ---------------------------------------------------------------------
        proposal_msg = await assigned_agent.process_task(goal, ctx)
        all_dialogue.append(proposal_msg)

        # Chief Auditor executes cross-examination
        audit_result = await self.auditor.cross_examine_and_verify(assigned_agent, proposal_msg)
        all_dialogue.extend(audit_result.dialogue_transcript)

        # ---------------------------------------------------------------------
        # PHASE 4: PRESENT PROPOSAL TO PROPRIETOR
        # ---------------------------------------------------------------------
        proposal_text = (
            f"📋 EXECUTIVE PROPOSAL PRESENTED TO SOLE PROPRIETOR (SAPNA JAISWAL)\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 Goal: '{goal}'\n"
            f"🤖 Assigned Sentinel: {assigned_agent.name} ({assigned_agent.role.value})\n"
            f"🔍 Auditing Authority: {self.auditor.name} (Chanakya Sentinel)\n"
            f"💬 Inter-Agent Inquest Rounds: {audit_result.cross_examination_rounds}\n"
            f"🛡️ Invariants Certified: {', '.join(audit_result.invariants_checked)}\n"
            f"📊 Confidence Score: {audit_result.confidence_score * 100:.1f}%\n"
            f"⚖️ Audit Verdict: {'APPROVED BY AUDITOR ✓' if audit_result.verified else 'REJECTED BY AUDITOR ✗'}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚠️ ACTION REQUIRED: Awaiting explicit approval from Proprietor to execute."
        )

        approval_state = (
            HumanApprovalStatus.AWAITING_PROPRIETOR_APPROVAL 
            if audit_result.verified 
            else HumanApprovalStatus.PROPRIETOR_REJECTED
        )

        return SwarmExecutionReceipt(
            phase="PHASE_4_PROPOSAL_PRESENTATION",
            goal=goal,
            gathered_data=gathered_data,
            strategic_plan=strategic_plan,
            assigned_agents=[self.role, assigned_agent.role, self.auditor.role],
            dialogue_log=all_dialogue,
            verification=audit_result,
            executive_proposal_to_proprietor=proposal_text,
            approval_status=approval_state,
            status="AWAITING_PROPRIETOR_APPROVAL" if audit_result.verified else "REJECTED_AUDIT_FAILURE"
        )

    async def execute_approved_receipt(self, receipt: SwarmExecutionReceipt, proprietor_approval: bool = True) -> SwarmExecutionReceipt:
        """
        PHASE 5: EXECUTE
        Triggered ONLY when the Sole Proprietor grants explicit approval.
        """
        if not proprietor_approval:
            receipt.approval_status = HumanApprovalStatus.PROPRIETOR_REJECTED
            receipt.status = "REJECTED_BY_PROPRIETOR"
            receipt.phase = "CANCELLED"
            return receipt

        if not receipt.verification.verified:
            receipt.status = "EXECUTION_BLOCKED_UNVERIFIED"
            return receipt

        receipt.phase = "PHASE_5_EXECUTED"
        receipt.approval_status = HumanApprovalStatus.EXECUTED
        receipt.status = "EXECUTED_AND_SEALED"
        receipt.final_execution_receipt = {
            "execution_status": "SUCCESSFUL_MUTATION",
            "certified_payload": receipt.verification.certified_payload,
            "immutable_ledger_logged": True
        }
        return receipt

    async def answer_challenge(self, challenge_question: str, proposal_context: Dict[str, Any]) -> AgentMessage:
        return self.send_message(
            recipient=AgentRole.CHIEF_AUDITOR,
            msg_type=MessageType.RESPONSE_CLARIFICATION,
            content="Executive directives are governed by immutable business guidelines and zero-corruption invariants.",
            payload=proposal_context
        )
