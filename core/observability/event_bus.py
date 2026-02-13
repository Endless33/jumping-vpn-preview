"""
Event Bus — Jumping VPN (Preview)

Minimal non-blocking observability layer.

Purpose:
- emit deterministic protocol events (state changes, switches, security rejects)
- allow multiple sinks (stdout, jsonl, SIEM adapter)
- never block correctness

Rule:
Telemetry failure must not affect session behavior.
"""

from dataclasses import dataclass, asdict
from typing import Callable, Dict, List, Optional, Any
import time
import json


@dataclass(frozen=True)
class ProtocolEvent:
    ts_ms: int
    event_type: str
    session_id: str
    state_version: int
    reason_code: str
    details: Dict[str, Any]


class EventSinkError(Exception):
    pass


class EventBus:
    """
    Simple fan-out event bus. Sinks are best-effort.
    """

    def __init__(self):
        self._sinks: List[Callable[[ProtocolEvent], None]] = []

    def add_sink(self, sink: Callable[[ProtocolEvent], None]) -> None:
        self._sinks.append(sink)

    def emit(
        self,
        *,
        event_type: str,
        session_id: str,
        state_version: int,
        reason_code: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        ev = ProtocolEvent(
            ts_ms=int(time.time() * 1000),
            event_type=event_type,
            session_id=session_id,
            state_version=state_version,
            reason_code=reason_code,
            details=details or {},
        )

        # Non-blocking best effort fan-out
        for sink in list(self._sinks):
            try:
                sink(ev)
            except Exception:
                # Telemetry must never break protocol correctness.
                # Intentionally swallow sink errors.
                continue


# ----------------------------
# Reference sinks
# ----------------------------

def stdout_sink(ev: ProtocolEvent) -> None:
    print(f"[{ev.ts_ms}] {ev.event_type} session={ev.session_id} v={ev.state_version} reason={ev.reason_code} {ev.details}")


def jsonl_file_sink(path: str) -> Callable[[ProtocolEvent], None]:
    """
    Returns a sink that appends JSON lines to a file.
    """
    def _sink(ev: ProtocolEvent) -> None:
        line = json.dumps(asdict(ev), ensure_ascii=False)
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    return _sink