
import json
import time
from dataclasses import asdict
from pathlib import Path

from policy.schemas import RoutingDecision

LOG_PATH = Path("audit_log.jsonl")


def log_decision(session_id: str, decision: RoutingDecision) -> None:
    """Append-only log of every routing decision made, for later review."""
    entry = {
        "timestamp": time.time(),
        "session_id": session_id,
        "decision": asdict(decision),
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")
