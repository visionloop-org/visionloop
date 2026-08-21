import pytest
from pathlib import Path
from visionloop_finance.operations_logger import operations_logger, AutonomousOperationsLogger

def test_operations_logger_event_creation(tmp_path):
    temp_log_file = tmp_path / "test_events.json"
    logger = AutonomousOperationsLogger(log_path=str(temp_log_file))
    
    event = logger.log_event(
        event_type="TEST_SWEEP_EVENT",
        category="TREASURY",
        description="Test 15% sinking fund sweep",
        data={"amount_inr": 10800.00, "status": "CONFIRMED"}
    )
    
    assert event["event_type"] == "TEST_SWEEP_EVENT"
    assert event["category"] == "TREASURY"
    assert "sha256_signature" in event
    assert len(event["sha256_signature"]) == 64
    
    recent = logger.get_recent_events(limit=5)
    assert len(recent) == 1
    assert recent[0]["description"] == "Test 15% sinking fund sweep"
