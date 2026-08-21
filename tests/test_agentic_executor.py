import pytest
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "services" / "ai-agent-service"))

from app.agents.agentic_executor import agent_executor

@pytest.mark.asyncio
async def test_agentic_executor_data_integrity():
    res = await agent_executor.execute_task("verify data integrity and invariants")
    assert res["status"] == "success"
    assert "DATA INTEGRITY" in res["reply"]
    assert "ANTIGRAVITY AI" in res["reply"]

@pytest.mark.asyncio
async def test_agentic_executor_invoice_generation():
    res = await agent_executor.execute_task("generate next month's invoice for the lessee")
    assert res["status"] == "success"
    assert "INVOICE GENERATED" in res["reply"]
    assert "SAC 997311" in res["reply"]

@pytest.mark.asyncio
async def test_agentic_executor_battery_telemetry():
    res = await agent_executor.execute_task("check battery health and temperature")
    assert res["status"] == "success"
    assert "BATTERY & FLEET TELEMETRY AUDIT" in res["reply"]
    assert "Tata Intra EV" in res["reply"]

@pytest.mark.asyncio
async def test_agentic_executor_sinking_fund():
    res = await agent_executor.execute_task("calculate sinking fund for 24 months")
    assert res["status"] == "success"
    assert "15% SINKING FUND CALCULATION" in res["reply"]
    assert "24 Months" in res["reply"]

@pytest.mark.asyncio
async def test_agentic_executor_kyc():
    res = await agent_executor.execute_task("show proprietor kyc details for Sapna Jaiswal")
    assert res["status"] == "success"
    assert "Sapna Jaiswal" in res["reply"]
    assert "BGVPJ3356G" in res["reply"]
