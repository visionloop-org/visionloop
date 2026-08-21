import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "packages" / "visionloop-finance"))
sys.path.insert(0, str(root_dir / "packages" / "visionloop-telematics"))
sys.path.insert(0, str(root_dir / "packages" / "visionloop-legal"))
sys.path.insert(0, str(root_dir / "packages" / "visionloop-comms"))
sys.path.insert(0, str(root_dir / "packages" / "visionloop-sdk"))

import pytest
import pytest_asyncio
from visionloop_sdk import VisionLoopSDK
from visionloop_sdk.swarm import (
    SwarmOrchestrator,
    ChiefExecutiveSwarmAgent,
    ChiefAuditorVerificationAgent,
    FleetOperationsAgent,
    TreasuryFinanceAgent,
    LegalComplianceAgent,
    SoftwareEngineeringAgent,
    YouTubeMarketingAgent,
    AgentRole,
    MessageType,
    HumanApprovalStatus
)

@pytest.mark.asyncio
async def test_swarm_hierarchy_structure():
    orchestrator = SwarmOrchestrator()
    hierarchy = orchestrator.list_hierarchy()
    assert len(hierarchy) == 3
    assert hierarchy[0]["role"] == AgentRole.CHIEF_EXECUTIVE.value
    assert hierarchy[1]["role"] == AgentRole.CHIEF_AUDITOR.value
    assert len(hierarchy[2]["agents"]) == 5

@pytest.mark.asyncio
async def test_treasury_5_phase_workflow_and_human_approval():
    orchestrator = SwarmOrchestrator()
    
    # Phase 1 -> 4: Gather, Plan, Grill/Verify, Present Proposal
    proposal_receipt = await orchestrator.execute_task_with_cross_examination(
        goal="Generate monthly lease invoice for Tata Intra EV and allocate sinking fund",
        domain="finance",
        context={"base_amount": 72000.00, "sac_code": "997311"}
    )
    assert proposal_receipt.phase == "PHASE_4_PROPOSAL_PRESENTATION"
    assert proposal_receipt.approval_status == HumanApprovalStatus.AWAITING_PROPRIETOR_APPROVAL
    assert proposal_receipt.verification.verified is True
    assert proposal_receipt.verification.confidence_score == 1.0
    assert proposal_receipt.verification.cross_examination_rounds == 2
    assert "PROPOSAL PRESENTED TO SOLE PROPRIETOR" in proposal_receipt.executive_proposal_to_proprietor
    assert len(proposal_receipt.strategic_plan) == 6
    assert len(proposal_receipt.gathered_data) > 0

    # Phase 5: Execute upon explicit proprietor approval
    executed_receipt = await orchestrator.execute_approved_task(proposal_receipt, proprietor_approval=True)
    assert executed_receipt.phase == "PHASE_5_EXECUTED"
    assert executed_receipt.approval_status == HumanApprovalStatus.EXECUTED
    assert executed_receipt.status == "EXECUTED_AND_SEALED"
    assert executed_receipt.final_execution_receipt["execution_status"] == "SUCCESSFUL_MUTATION"

@pytest.mark.asyncio
async def test_fleet_cross_examination_and_safety_lockout():
    auditor = ChiefAuditorVerificationAgent()
    fleet_agent = FleetOperationsAgent()

    # Case A: Vehicle in Standstill (Safe)
    proposal_safe = await fleet_agent.process_task("Evaluate vehicle telemetry", {"speed_kmh": 0.0, "dc_fast_charge_ratio": 0.30, "battery_temp_c": 32.0})
    audit_safe = await auditor.cross_examine_and_verify(fleet_agent, proposal_safe)
    assert audit_safe.verified is True
    assert any("Standstill Invariant" in inv for inv in audit_safe.invariants_checked)

    # Case B: Vehicle in Motion (Immobilizer Lockout Triggered)
    proposal_motion = await fleet_agent.process_task("Actuate remote immobilizer", {"speed_kmh": 45.0, "dc_fast_charge_ratio": 0.30, "battery_temp_c": 32.0})
    audit_motion = await auditor.cross_examine_and_verify(fleet_agent, proposal_motion)
    assert audit_motion.verified is False
    assert any("violat" in r.lower() or "lockout" in r.lower() for r in audit_motion.reasons)

@pytest.mark.asyncio
async def test_legal_and_privacy_cross_examination():
    orchestrator = SwarmOrchestrator()
    receipt = await orchestrator.execute_task_with_cross_examination(
        goal="Audit statutory MSME 45-day payment clauses and DPDP Act privacy governance",
        domain="legal"
    )
    assert receipt.phase == "PHASE_4_PROPOSAL_PRESENTATION"
    assert receipt.approval_status == HumanApprovalStatus.AWAITING_PROPRIETOR_APPROVAL
    assert receipt.verification.verified is True
    assert any("MSMED Act" in inv for inv in receipt.verification.invariants_checked)
    assert any("DPDP Act" in inv for inv in receipt.verification.invariants_checked)

@pytest.mark.asyncio
async def test_sdk_swarm_integration():
    sdk = VisionLoopSDK()
    assert hasattr(sdk, "swarm")
    assert hasattr(sdk, "orchestrator")
    receipt = await sdk.orchestrator.execute_task_with_cross_examination(
        goal="Run full YouTube creator monetization and tax export audit",
        domain="youtube"
    )
    assert receipt.phase == "PHASE_4_PROPOSAL_PRESENTATION"
    assert receipt.approval_status == HumanApprovalStatus.AWAITING_PROPRIETOR_APPROVAL
    assert receipt.verification.verified is True

