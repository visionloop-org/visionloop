from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid
import hashlib

class AgentRole(str, Enum):
    CHIEF_EXECUTIVE = "CHIEF_EXECUTIVE_ORCHESTRATOR"
    CHIEF_AUDITOR = "CHIEF_AUDITOR_VERIFIER"
    FLEET_OPERATIONS = "FLEET_OPERATIONS_AGENT"
    TREASURY_FINANCE = "TREASURY_FINANCE_AGENT"
    LEGAL_COMPLIANCE = "LEGAL_COMPLIANCE_AGENT"
    SOFTWARE_ENGINEERING = "SOFTWARE_ENGINEERING_AGENT"
    YOUTUBE_MARKETING = "YOUTUBE_MARKETING_AGENT"

class MessageType(str, Enum):
    TASK_DELEGATION = "TASK_DELEGATION"
    WORK_PROPOSAL = "WORK_PROPOSAL"
    CHALLENGE_QUESTION = "CHALLENGE_QUESTION"
    RESPONSE_CLARIFICATION = "RESPONSE_CLARIFICATION"
    AUDIT_APPROVAL = "AUDIT_APPROVAL"
    AUDIT_REJECTION = "AUDIT_REJECTION"
    EXECUTIVE_DECISION = "EXECUTIVE_DECISION"

class AgentMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: f"MSG-{uuid.uuid4().hex[:8].upper()}")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    sender: AgentRole
    recipient: AgentRole
    message_type: MessageType
    content: str
    data_payload: Dict[str, Any] = Field(default_factory=dict)
    cryptographic_hash: str = ""

    def compute_hash(self) -> str:
        raw = f"{self.message_id}:{self.sender.value}:{self.recipient.value}:{self.message_type.value}:{self.content}:{self.timestamp}"
        self.cryptographic_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return self.cryptographic_hash

class AgentVerificationResult(BaseModel):
    audit_id: str = Field(default_factory=lambda: f"AUDIT-{uuid.uuid4().hex[:8].upper()}")
    auditor: AgentRole = AgentRole.CHIEF_AUDITOR
    target_agent: AgentRole
    verified: bool
    confidence_score: float
    cross_examination_rounds: int
    dialogue_transcript: List[AgentMessage] = Field(default_factory=list)
    invariants_checked: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)
    certified_payload: Dict[str, Any] = Field(default_factory=dict)

class HumanApprovalStatus(str, Enum):
    AWAITING_PROPRIETOR_APPROVAL = "AWAITING_PROPRIETOR_APPROVAL"
    PROPRIETOR_APPROVED = "PROPRIETOR_APPROVED"
    PROPRIETOR_REJECTED = "PROPRIETOR_REJECTED"
    EXECUTED = "EXECUTED"

class SwarmExecutionReceipt(BaseModel):
    execution_id: str = Field(default_factory=lambda: f"SWARM-EXEC-{uuid.uuid4().hex[:8].upper()}")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    phase: str = "PHASE_4_PROPOSAL_PRESENTATION"
    goal: str
    gathered_data: Dict[str, Any] = Field(default_factory=dict)
    strategic_plan: List[str] = Field(default_factory=list)
    assigned_agents: List[AgentRole] = Field(default_factory=list)
    dialogue_log: List[AgentMessage] = Field(default_factory=list)
    verification: AgentVerificationResult
    executive_proposal_to_proprietor: str
    approval_status: HumanApprovalStatus = HumanApprovalStatus.AWAITING_PROPRIETOR_APPROVAL
    final_execution_receipt: Optional[Dict[str, Any]] = None
    status: str
