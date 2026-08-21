import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

class AutonomousOperationsLogger:
    """
    Cryptographic Operational Event Logger for Self-Sustaining Autonomous Enterprises.
    Logs financial sweeps, telematics checks, statutory compliance ticks, and
    multi-agent swarm operations with verifiable SHA-256 signatures.
    """
    
    def __init__(self, log_path: Optional[str] = None):
        if log_path:
            self.log_file = Path(log_path)
        else:
            self.log_file = Path("d:/VisionLoop/data/operations/live_operational_events.json")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    def log_event(
        self,
        event_type: str,
        category: str,
        description: str,
        data: Dict[str, Any],
        actor: str = "AI_SWARM_SENTINEL"
    ) -> Dict[str, Any]:
        """Logs an operational business event with cryptographic hashing."""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Base event object
        event = {
            "timestamp": timestamp,
            "event_type": event_type,
            "category": category,
            "actor": actor,
            "description": description,
            "payload": data
        }
        
        # Compute event SHA-256 signature
        serialized = json.dumps(event, sort_keys=True)
        signature = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        event["sha256_signature"] = signature
        
        # Append to live log
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                logs: List[Dict[str, Any]] = json.load(f)
        except Exception:
            logs = []
            
        logs.append(event)
        
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)
            
        return event

    def get_recent_events(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieves the most recent operational events."""
        if not self.log_file.exists():
            return []
        with open(self.log_file, "r", encoding="utf-8") as f:
            logs: List[Dict[str, Any]] = json.load(f)
        return logs[-limit:]

operations_logger = AutonomousOperationsLogger()
