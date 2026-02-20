# jumping_vpn/session_manager.py
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import secrets
import time


class SessionState(str, Enum):
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    DETACHED = "DETACHED"


@dataclass
class Session:
    session_id: str
    state: SessionState = SessionState.NEW
    created_at: float = field(default_factory=time.time)
    last_event_at: float = field(default_factory=time.time)

    # A simple continuity token (placeholder for cryptographic identity)
    continuity_key: str = field(default_factory=lambda: secrets.token_hex(16))

    # Current attached transport (string label), e.g. "tcp://127.0.0.1:9000"
    transport_label: Optional[str] = None

    # Deterministic event trace
    trace: List[Dict[str, Any]] = field(default_factory=list)

    def log(self, event: str, **data: Any) -> None:
        now = time.time()
        self.last_event_at = now
        entry = {"t": now, "event": event, **data}
        self.trace.append(entry)


class SessionManager:
    """
    Minimal session manager for Early Alpha:
    - Creates session identity independent of transport
    - Attaches/detaches transports without changing identity
    - Emits deterministic trace events
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, Session] = {}

    def create_session(self) -> Session:
        sid = f"jv-{secrets.token_hex(8)}"
        s = Session(session_id=sid)
        s.log("SESSION_CREATED", session_id=s.session_id, continuity_key=s.continuity_key)
        self._sessions[sid] = s
        return s

    def get(self, session_id: str) -> Session:
        return self._sessions[session_id]

    def attach_transport(self, session: Session, transport_label: str, attachment_id: str) -> None:
        # Identity continuity check placeholder:
        # In a real protocol, you'd validate that attachment is authorized
        # (challenge/response bound to continuity_key).
        session.transport_label = transport_label
        session.state = SessionState.ACTIVE
        session.log(
            "TRANSPORT_ATTACHED",
            transport=transport_label,
            attachment_id=attachment_id,
            session_id=session.session_id,
        )

    def mark_degraded(self, session: Session, reason: str) -> None:
        session.state = SessionState.DEGRADED
        session.log("TRANSPORT_DEGRADED", reason=reason, transport=session.transport_label)

    def detach_transport(self, session: Session, reason: str) -> None:
        old = session.transport_label
        session.transport_label = None
        session.state = SessionState.DETACHED
        session.log("TRANSPORT_DETACHED", reason=reason, previous_transport=old)

    def continuity_verified(self, session: Session, expected_key: str) -> bool:
        ok = session.continuity_key == expected_key
        session.log("CONTINUITY_VERIFIED", ok=ok)
        return ok