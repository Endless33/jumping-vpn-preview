from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from core.common.models import (
    SessionState,
    PolicySnapshot,
    TransportBinding,
)
from core.common.reason_codes import ReasonCode


@dataclass
class ClientSession:
    """
    Client-side session context.
    Holds identity + policy + current transport binding.
    """
    session_id: str
    state: SessionState = SessionState.BIRTH
    state_version: int = 0

    policy: PolicySnapshot = field(default_factory=PolicySnapshot)

    active_transport: Optional[TransportBinding] = None

    created_ts_ms: int = 0
    last_activity_ts_ms: int = 0
    last_switch_ts_ms: int = 0

    # Anti-replay freshness counter (client-side monotonic)
    nonce: int = 0


class ClientAgent:
    """
    Client control-plane skeleton.

    Responsibilities:
    - Maintain session identity context
    - Track transport health signals
    - Initiate explicit reattach when transport is dead
    - Enforce anti-flap bounds locally
    - Produce audit-friendly events (optional)
    """

    def __init__(self, client_id: str):
        self.client_id = client_id
        self.session: Optional[ClientSession] = None

    # ---------------------------
    # Session lifecycle
    # ---------------------------

    def new_session(self, session_id: str, policy: Optional[PolicySnapshot] = None) -> ClientSession:
        now = int(time.time() * 1000)
        self.session = ClientSession(
            session_id=session_id,
            state=SessionState.BIRTH,
            state_version=0,
            policy=policy or PolicySnapshot(),
            created_ts_ms=now,
            last_activity_ts_ms=now,
            nonce=0,
        )
        return self.session

    def attach(self, transport: TransportBinding) -> None:
        s = self._require_session()

        now = int(time.time() * 1000)
        s.active_transport = transport
        s.state = SessionState.ATTACHED
        s.state_version += 1
        s.last_activity_ts_ms = now

        self._emit("STATE_CHANGE", ReasonCode.HANDSHAKE_OK, {"state": s.state.value})

    # ---------------------------
    # Health monitoring hooks
    # ---------------------------

    def on_health_sample(self, loss_pct: float, latency_ms: int, jitter_ms: int) -> None:
        """
        Called by transport monitor (not implemented here).
        If thresholds exceeded -> VOLATILE or DEGRADED.
        If transport dead -> RECOVERING.
        """
        s = self._require_session()
        now = int(time.time() * 1000)

        # No session activity without an attached transport
        if s.state != SessionState.ATTACHED:
            return

        # Volatility signal
        if (
            loss_pct >= s.policy.loss_threshold_pct
            or latency_ms >= s.policy.latency_threshold_ms
            or jitter_ms >= s.policy.jitter_threshold_ms
        ):
            s.state = SessionState.VOLATILE
            s.state_version += 1
            s.last_activity_ts_ms = now
            self._emit(
                "VOLATILITY_SIGNAL",
                ReasonCode.QUALITY_THRESHOLD_EXCEEDED,
                {"loss_pct": loss_pct, "latency_ms": latency_ms, "jitter_ms": jitter_ms},
            )

    def on_transport_dead(self) -> None:
        """
        Called when delivery is impossible within bounded window.
        This must trigger explicit RECOVERING + reattach attempt.
        """
        s = self._require_session()
        now = int(time.time() * 1000)

        s.active_transport = None
        s.state = SessionState.RECOVERING
        s.state_version += 1
        s.last_activity_ts_ms = now

        self._emit("TRANSPORT_DEAD", ReasonCode.RECOVERY_START, {"state": s.state.value})

    # ---------------------------
    # Reattach initiation
    # ---------------------------

    def build_reattach_request(self, new_transport: TransportBinding) -> Dict[str, Any]:
        """
        Produces a control-plane request payload.
        In production, proof would be MAC/signature with session keys.
        """
        s = self._require_session()

        # local cooldown
        if not self._cooldown_ok():
            return self._reject_payload(ReasonCode.POLICY_COOLDOWN_ACTIVE, "Cooldown active")

        # monotonic nonce
        s.nonce += 1

        payload = {
            "session_id": s.session_id,
            "nonce": s.nonce,
            "proof": "POP_PLACEHOLDER",
            "candidate": {
                "transport_id": new_transport.transport_id,
                "remote_ip": new_transport.remote_ip,
                "remote_port": new_transport.remote_port,
                "proto": new_transport.proto,
            },
        }

        self._emit("REATTACH_REQUEST", ReasonCode.RECOVERY_START, {"nonce": s.nonce})
        return payload

    def on_reattach_success(self, transport: TransportBinding) -> None:
        s = self._require_session()
        now = int(time.time() * 1000)

        s.active_transport = transport
        s.state = SessionState.ATTACHED
        s.state_version += 1
        s.last_activity_ts_ms = now
        s.last_switch_ts_ms = now

        self._emit("REATTACH_SUCCESS", ReasonCode.REATTACH_SUCCESS, {"state": s.state.value})

    def on_reattach_rejected(self, reason: ReasonCode) -> None:
        s = self._require_session()
        now = int(time.time() * 1000)

        # remain RECOVERING / possibly DEGRADED based on policy
        s.last_activity_ts_ms = now
        self._emit("REATTACH_REJECT", reason, {"state": s.state.value})

    # ---------------------------
    # Helpers
    # ---------------------------

    def _cooldown_ok(self) -> bool:
        s = self._require_session()
        now = int(time.time() * 1000)
        if s.last_switch_ts_ms == 0:
            return True
        return (now - s.last_switch_ts_ms) >= s.policy.switch_cooldown_ms

    def _reject_payload(self, reason: ReasonCode, message: str) -> Dict[str, Any]:
        return {"error": {"reason": reason.value, "message": message}}

    def _require_session(self) -> ClientSession:
        if self.session is None:
            raise RuntimeError("ClientAgent has no active session")
        return self.session

    def _emit(self, event_type: str, reason: ReasonCode, details: Dict[str, Any]) -> None:
        """
        Placeholder for event emission. In production this would stream to:
        - local logs
        - telemetry pipeline
        - SIEM adapter
        """
        _ = (event_type, reason, details)
        # keep intentionally side-effect free here
        return