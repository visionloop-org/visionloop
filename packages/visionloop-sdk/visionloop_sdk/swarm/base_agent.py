from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from visionloop_sdk.swarm.models import AgentRole, MessageType, AgentMessage

class BaseSwarmAgent(ABC):
    """
    Abstract Base Class for all Autonomous Swarm Agents.
    Supports autonomous execution, Q&A cross-examination hooks,
    and structured inter-agent message passing.
    """
    def __init__(self, role: AgentRole, name: str, description: str):
        self.role = role
        self.name = name
        self.description = description
        self.inbox: List[AgentMessage] = []
        self.outbox: List[AgentMessage] = []

    def send_message(self, recipient: AgentRole, msg_type: MessageType, content: str, payload: Optional[Dict[str, Any]] = None) -> AgentMessage:
        msg = AgentMessage(
            sender=self.role,
            recipient=recipient,
            message_type=msg_type,
            content=content,
            data_payload=payload or {}
        )
        msg.compute_hash()
        self.outbox.append(msg)
        return msg

    def receive_message(self, msg: AgentMessage):
        self.inbox.append(msg)

    @abstractmethod
    async def process_task(self, task_instruction: str, context: Optional[Dict[str, Any]] = None) -> AgentMessage:
        """Execute domain-specific work and return a proposal."""
        pass

    @abstractmethod
    async def answer_challenge(self, challenge_question: str, proposal_context: Dict[str, Any]) -> AgentMessage:
        """Answer a verification or cross-examination question asked by a peer/auditor agent."""
        pass
