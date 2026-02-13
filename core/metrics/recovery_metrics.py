"""
Jumping VPN — Recovery Metrics (Preview)

Goal:
Measure deterministic recovery behavior under transport volatility.

This module is contract-first instrumentation:
- No networking
- No crypto
- No external dependencies

It records timestamps of key events (transport death, reattach request/ack, state changes)
and produces a stable metrics summary suitable for logs/benchmarks.

Session is the anchor. Transport is volatile.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, List, Any


class EventType(str, Enum):
    # Signals
    TRANSPORT_DEAD = "TRANSPORT_DEAD"
    TRANSPORT_SWITCH = "TRANSPORT_SWITCH"

    # Control-plane
    REATTACH_REQUEST_SENT = "REATTACH_REQUEST_SENT"
    REATTACH_ACK_RECEIVED = "REATTACH_ACK_RECEIVED"
    REATTACH_REJECT_RECEIVED = "REATTACH_REJECT_RECEIVED"

    # State machine
    STATE_CHANGE = "STATE_CHANGE"

    # Limits / security / abuse
    SWITCH_RATE_LIMIT_HIT = "SWITCH_RATE_LIMIT_HIT"
    COOLDOWN_ACTIVE = "COOLDOWN_ACTIVE"
    REPLAY_REJECT = "REPLAY_REJECT"
    VERSION_MISMATCH_REJECT = "VERSION_MISMATCH_REJECT"
    TTL_EXPIRED = "TTL_EXPIRED"


@dataclass(frozen=True)
class MetricEvent:
    ts_ms: int
    event_type: str
    reason_code: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RecoveryWindow:
    """
    One recovery attempt window:
    starts when transport is declared dead, ends when session returns to ATTACHED
    (or ends in a deterministic failure).
    """
    start_ts_ms: int
    end_ts_ms: Optional[int] = None

    outcome: str = "UNKNOWN"  # e.g. RECOVERED | DEGRADED | TERMINATED | REJECTED
    reason_code: Optional[str] = None

    # Key timestamps (optional)
    reattach_request_ts_ms: Optional[int] = None
    reattach_ack_ts_ms: Optional[int] = None
    transport_switch_ts_ms: Optional[int] = None

    # Counters
    attempts: int = 0
    rejects: int = 0
    switches: int = 0
    rate_limit_hits: int = 0
    replay_rejects: int = 0
    version_mismatch_rejects: int = 0

    def duration_ms(self) -> Optional[int]:
        if self.end_ts_ms is None:
            return None
        return max(0, self.end_ts_ms - self.start_ts_ms)

    def control_plane_rtt_ms(self) -> Optional[int]:
        """
        Time from REATTACH_REQUEST_SENT to REATTACH_ACK_RECEIVED.
        """
        if self.reattach_request_ts_ms is None or self.reattach_ack_ts_ms is None:
            return None
        return max(0, self.reattach_ack_ts_ms - self.reattach_request_ts_ms)


@dataclass
class RecoveryMetricsSummary:
    """
    Stable summary intended for JSON logging / benchmark extraction.
    """
    session_id: str

    total_windows: int
    recovered_windows: int
    failed_windows: int

    # Latency stats
    recovery_durations_ms: List[int] = field(default_factory=list)
    control_plane_rtts_ms: List[int] = field(default_factory=list)

    # Counters
    total_switches: int = 0
    total_attempts: int = 0
    total_rejects: int = 0
    rate_limit_hits: int = 0
    replay_rejects: int = 0
    version_mismatch_rejects: int = 0

    # Derived (simple)
    recovery_success_rate: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "total_windows": self.total_windows,
            "recovered_windows": self.recovered_windows,
            "failed_windows": self.failed_windows,
            "recovery_success_rate": self.recovery_success_rate,
            "recovery_durations_ms": self.recovery_durations_ms,
            "control_plane_rtts_ms": self.control_plane_rtts_ms,
            "total_switches": self.total_switches,
            "total_attempts": self.total_attempts,
            "total_rejects": self.total_rejects,
            "rate_limit_hits": self.rate_limit_hits,
            "replay_rejects": self.replay_rejects,
            "version_mismatch_rejects": self.version_mismatch_rejects,
        }


class RecoveryMetricsRecorder:
    """
    Deterministic recorder that consumes events and produces metrics.

    Intended usage:
    - client agent emits: TRANSPORT_DEAD, REATTACH_REQUEST_SENT, STATE_CHANGE(RECOVERING)
    - server emits: TRANSPORT_SWITCH, REATTACH_ACK_RECEIVED, STATE_CHANGE(ATTACHED)
    - failures emit: REATTACH_REJECT_RECEIVED / TTL_EXPIRED / VERSION_MISMATCH_REJECT etc.

    This module does not enforce policy. It measures outcomes.
    """

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.events: List[MetricEvent] = []

        self.windows: List[RecoveryWindow] = []
        self._active: Optional[RecoveryWindow] = None

        # current known session state (optional)
        self._state: Optional[str] = None

    def record(
        self,
        ts_ms: int,
        event_type: EventType | str,
        reason_code: Optional[str] = None,
        **details: Any,
    ) -> None:
        et = event_type.value if isinstance(event_type, EventType) else str(event_type)
        self.events.append(MetricEvent(ts_ms=ts_ms, event_type=et, reason_code=reason_code, details=dict(details)))
        self._apply(ts_ms=ts_ms, event_type=et, reason_code=reason_code, details=details)

    def _start_window(self, ts_ms: int) -> None:
        self._active = RecoveryWindow(start_ts_ms=ts_ms)
        self.windows.append(self._active)

    def _close_window(self, ts_ms: int, outcome: str, reason_code: Optional[str] = None) -> None:
        if self._active is None:
            return
        self._active.end_ts_ms = ts_ms
        self._active.outcome = outcome
        self._active.reason_code = reason_code
        self._active = None

    def _apply(self, ts_ms: int, event_type: str, reason_code: Optional[str], details: Dict[str, Any]) -> None:
        # Window creation trigger
        if event_type == EventType.TRANSPORT_DEAD.value:
            # If a window is already active, we don't create a second window;
            # this avoids double-counting in noisy emitters.
            if self._active is None:
                self._start_window(ts_ms)
            return

        # No active window? most events are ignored for recovery metrics.
        w = self._active
        if w is None:
            # Still track state if provided
            if event_type == EventType.STATE_CHANGE.value:
                new_state = str(details.get("new_state", ""))
                if new_state:
                    self._state = new_state
            return

        # Within active window: update counters/timestamps
        if event_type == EventType.REATTACH_REQUEST_SENT.value:
            w.attempts += 1
            w.reattach_request_ts_ms = w.reattach_request_ts_ms or ts_ms
            return

        if event_type == EventType.REATTACH_ACK_RECEIVED.value:
            w.reattach_ack_ts_ms = w.reattach_ack_ts_ms or ts_ms
            return

        if event_type == EventType.TRANSPORT_SWITCH.value:
            w.switches += 1
            w.transport_switch_ts_ms = w.transport_switch_ts_ms or ts_ms
            return

        if event_type == EventType.SWITCH_RATE_LIMIT_HIT.value:
            w.rate_limit_hits += 1
            return

        if event_type == EventType.REPLAY_REJECT.value:
            w.replay_rejects += 1
            w.rejects += 1
            return

        if event_type == EventType.VERSION_MISMATCH_REJECT.value:
            w.version_mismatch_rejects += 1
            w.rejects += 1
            return

        if event_type == EventType.REATTACH_REJECT_RECEIVED.value:
            w.rejects += 1
            # Rejection does not necessarily end recovery;
            # it depends on policy, but metrics track rejects.
            return

        if event_type == EventType.TTL_EXPIRED.value:
            # TTL expiry ends deterministically.
            self._close_window(ts_ms, outcome="TERMINATED", reason_code=reason_code or "TTL_EXPIRED")
            return

        if event_type == EventType.STATE_CHANGE.value:
            old_state = str(details.get("old_state", "")) if details.get("old_state") is not None else None
            new_state = str(details.get("new_state", "")) if details.get("new_state") is not None else None
            self._state = new_state or self._state

            # Close conditions:
            # - returning to ATTACHED = recovered
            # - entering DEGRADED/TERMINATED = deterministic failure
            if new_state == "ATTACHED":
                self._close_window(ts_ms, outcome="RECOVERED", reason_code=reason_code)
                return
            if new_state == "DEGRADED":
                self._close_window(ts_ms, outcome="DEGRADED", reason_code=reason_code)
                return
            if new_state == "TERMINATED":
                self._close_window(ts_ms, outcome="TERMINATED", reason_code=reason_code)
                return

            # otherwise window remains active (RECOVERING / VOLATILE, etc.)
            return

    def summary(self) -> RecoveryMetricsSummary:
        recovered = 0
        failed = 0

        recovery_durations: List[int] = []
        control_plane_rtts: List[int] = []

        total_switches = 0
        total_attempts = 0
        total_rejects = 0
        rate_limit_hits = 0
        replay_rejects = 0
        version_mismatch_rejects = 0

        for w in self.windows:
            if w.end_ts_ms is None:
                # still active; don't count as recovered/failed yet
                continue

            if w.outcome == "RECOVERED":
                recovered += 1
            else:
                failed += 1

            d = w.duration_ms()
            if d is not None:
                recovery_durations.append(d)

            rtt = w.control_plane_rtt_ms()
            if rtt is not None:
                control_plane_rtts.append(rtt)

            total_switches += w.switches
            total_attempts += w.attempts
            total_rejects += w.rejects
            rate_limit_hits += w.rate_limit_hits
            replay_rejects += w.replay_rejects
            version_mismatch_rejects += w.version_mismatch_rejects

        total_windows = recovered + failed
        success_rate = (recovered / total_windows) if total_windows > 0 else 0.0

        return RecoveryMetricsSummary(
            session_id=self.session_id,
            total_windows=total_windows,
            recovered_windows=recovered,
            failed_windows=failed,
            recovery_durations_ms=recovery_durations,
            control_plane_rtts_ms=control_plane_rtts,
            total_switches=total_switches,
            total_attempts=total_attempts,
            total_rejects=total_rejects,
            rate_limit_hits=rate_limit_hits,
            replay_rejects=replay_rejects,
            version_mismatch_rejects=version_mismatch_rejects,
            recovery_success_rate=success_rate,
        )


def example_usage() -> Dict[str, Any]:
    """
    This function exists only to show how events map to metrics.
    It is NOT executed automatically.

    You can paste the output into docs or logs.
    """
    r = RecoveryMetricsRecorder(session_id="sess_demo_001")

    # Transport dies
    r.record(1000, EventType.TRANSPORT_DEAD, reason_code="NO_DELIVERY_WINDOW")

    # Client begins recovery
    r.record(1050, EventType.STATE_CHANGE, reason_code="TRANSPORT_DEAD", old_state="ATTACHED", new_state="RECOVERING")

    # Client sends reattach request
    r.record(1100, EventType.REATTACH_REQUEST_SENT, reason_code="REATTACH", candidate_proto="udp")

    # Server switches transport + sends ack
    r.record(1250, EventType.TRANSPORT_SWITCH, reason_code="CANDIDATE_SELECTED", new_transport_id="udp:2")
    r.record(1300, EventType.REATTACH_ACK_RECEIVED, reason_code="REATTACH_SUCCESS")

    # Session returns to attached
    r.record(1350, EventType.STATE_CHANGE, reason_code="REATTACH_SUCCESS", old_state="RECOVERING", new_state="ATTACHED")

    return r.summary().to_dict()