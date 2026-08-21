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

@app.post("/agents/swarm/execute-all")
async def execute_all_agents():
    fin = await financial_agent.scan_and_collect()
    tel = await telematics_agent.evaluate_fleet_health()
    leg = await legal_agent.audit_compliance()
    exe = await executive_agent.generate_briefing()
    return {
        "status": "success",
        "message": "All autonomous agents executed cycle successfully",
        "results": {
            "financial": fin,
            "telematics": tel,
            "legal": leg,
            "executive": exe
        }
    }
