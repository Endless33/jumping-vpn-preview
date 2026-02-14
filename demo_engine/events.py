from dataclasses import dataclass
from typing import Dict, Any
import json

@dataclass
class Event:
    ts_ms: int
    event: str
    session_id: str
    data: Dict[str, Any]

    def to_jsonl(self) -> str:
        return json.dumps({
            "ts_ms": self.ts_ms,
            "event": self.event,
            "session_id": self.session_id,
            **self.data
        })