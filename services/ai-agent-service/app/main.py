from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.agents.financial_agent import financial_agent
from app.agents.telematics_agent import telematics_agent
from app.agents.legal_agent import legal_agent
from app.agents.executive_agent import executive_agent
from app.agents.agentic_executor import agent_executor

app = FastAPI(
    title="Vision Loop — AI Multi-Agent Operations Service",
    description="Autonomous swarm of AI agents governing Indian compliance, financial collections, asset health, and executive reporting.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatExecutionRequest(BaseModel):
    prompt: str
    user_name: Optional[str] = "Proprietor"
    chat_id: Optional[str] = None

@app.get("/")
def health_check():
    return {"service": "Vision Loop AI Agent Service", "status": "active", "agentic_executor": "online"}

@app.post("/agents/chat/execute")
async def execute_chat_prompt(req: ChatExecutionRequest):
    """Executes a natural-language task sent from Telegram or web chat using Antigravity AI reasoning."""
    return await agent_executor.execute_task(prompt=req.prompt, user_name=req.user_name or "Proprietor")

@app.post("/agents/financial/run")
async def run_financial_agent():
    return await financial_agent.scan_and_collect()

@app.post("/agents/telematics/evaluate")
async def run_telematics_agent():
    return await telematics_agent.evaluate_fleet_health()

@app.post("/agents/legal/audit")
async def run_legal_agent():
    return await legal_agent.audit_compliance()

@app.get("/agents/executive/briefing")
async def get_executive_briefing():
    return await executive_agent.generate_briefing()

import sys
from pathlib import Path

# Add packages to path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir / "packages" / "visionloop-finance"))
sys.path.insert(0, str(root_dir / "packages" / "visionloop-telematics"))
sys.path.insert(0, str(root_dir / "packages" / "visionloop-legal"))
sys.path.insert(0, str(root_dir / "packages" / "visionloop-comms"))
sys.path.insert(0, str(root_dir / "packages" / "visionloop-sdk"))

from visionloop_sdk.swarm import SwarmOrchestrator

swarm_engine = SwarmOrchestrator()

class SwarmTaskRequest(BaseModel):
    goal: str
    domain: Optional[str] = "finance"
    context: Optional[Dict[str, Any]] = None

@app.get("/agents/hierarchy")
async def get_agent_hierarchy():
    """Returns the 3-tier hierarchical agent organization tree."""
    return {"hierarchy": swarm_engine.list_hierarchy()}

@app.post("/agents/swarm/cross-examine")
async def execute_swarm_task(req: SwarmTaskRequest):
    """
    Executes a high-level enterprise task through the multi-agent swarm hierarchy.
    Operational workers propose solutions, the Chief Auditor cross-examines with Q&A challenges,
    and the Chief Executive certifies the final audited action receipt.
    """
    receipt = await swarm_engine.execute_task_with_cross_examination(
        goal=req.goal,
        domain=req.domain or "finance",
        context=req.context
    )
    return receipt.model_dump()

