from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class SessionState(str, Enum):
    BIRTH = "BIRTH"
    ATTACHED = "ATTACHED"
    VOLATILE = "VOLATILE"
    DEGRADED = "DEGRADED"
    RECOVERING = "RECOVERING"
    TERMINATED = "TERMINATED"


@dataclass(frozen=True)
class PolicySnapshot:
    """
    Deterministic policy bounds. Keep this small and explicit.
    These values define the behavioral contract of the session lifecycle.
    """

    # Identity lifetime bound (forces new handshake after expiry)
    session_ttl_ms: int = 60 * 60 * 1000  # 1h

    # How long a session may remain alive without an active transport
    transport_loss_ttl_ms: int = 10 * 1000  # 10s

    # Max time allowed to recover after transport death before DEGRADED/TERMINATED
    max_recovery_window_ms: int = 5 * 1000  # 5s

    # Anti-flap: max switches per rolling window
    max_switches_per_min: int = 10

    # Cooldown after a successful switch (prevents oscillation)
    switch_cooldown_ms: int = 500

    # Quality thresholds (used to gate VOLATILE/DEGRADED decisions)
    loss_threshold_pct: float = 20.0
    latency_threshold_ms: int = 300
    jitter_threshold_ms: int = 80


@dataclass(frozen=True)
class TransportBinding:
    """
    A replaceable attachment. This is NOT identity.
    """
    transport_id: str
    remote_ip: str
    remote_port: int
    proto: str = "UDP"  # UDP/TCP/QUIC (candidate)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SessionRecord:
    """
    Authoritative session state stored on server (or ownership layer).
    Must remain small, deterministic, and versioned.
    """
    session_id: str

    state: SessionState = SessionState.BIRTH
    state_version: int = 0

    # Active binding (single-active invariant)
    active_transport: Optional[TransportBinding] = None

    # Policy snapshot for this session
    policy: PolicySnapshot = field(default_factory=PolicySnapshot)

    # Bookkeeping timestamps (ms)
    created_ts_ms: int = 0
    last_state_change_ts_ms: int = 0
    last_activity_ts_ms: int = 0

    # Switch tracking (anti-flap)
    last_switch_ts_ms: int = 0
    switches_in_current_min: int = 0
    switches_window_start_ts_ms: int = 0

    # Replay / freshness tracking (control-plane)
    last_accepted_nonce: int = 0

    # Ownership (clustered deployments)
    owner_node_id: Optional[str] = None

    def to_public_dict(self) -> Dict[str, Any]:
        """Safe-ish representation for audit logs (no secrets)."""
        return {
            "session_id": self.session_id,
            "state": self.state.value,
            "state_version": self.state_version,
            "active_transport": None
            if self.active_transport is None
            else {
                "transport_id": self.active_transport.transport_id,
                "remote_ip": self.active_transport.remote_ip,
                "remote_port": self.active_transport.remote_port,
                "proto": self.active_transport.proto,
            },
            "created_ts_ms": self.created_ts_ms,
            "last_state_change_ts_ms": self.last_state_change_ts_ms,
            "last_activity_ts_ms": self.last_activity_ts_ms,
            "last_switch_ts_ms": self.last_switch_ts_ms,
            "switches_in_current_min": self.switches_in_current_min,
            "switches_window_start_ts_ms": self.switches_window_start_ts_ms,
            "owner_node_id": self.owner_node_id,
        }


@dataclass(frozen=True)
class ReattachRequest:
    """
    Control-plane request to bind a new transport to an existing session.
    In production this would carry cryptographic proof; here it's abstracted.
    """
    session_id: str
    nonce: int
    proof: str  # placeholder for PoP (MAC/signature)
    candidate: TransportBinding
    client_meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class HandshakeInit:
    """
    Initial session establishment request (abstracted).
    """
    client_id: str
    client_nonce: int
    client_meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class HandshakeResponse:
    """
    Initial session establishment response (abstracted).
    """
    session_id: str
    server_nonce: int
    policy: PolicySnapshot
    # In production: key material / negotiated parameters (NOT included here)