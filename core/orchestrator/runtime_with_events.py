"""
Runtime Controller (Evented) — Jumping VPN (Preview)

Same orchestration logic as runtime_controller.py,
but emits non-blocking protocol events for audit/SIEM pipelines.

This is a behavioral skeleton (no sockets, no crypto).
"""

from typing import Optional

from core.common.models import SessionState
from core.common.reason_codes import ReasonCode
from core.session.state_machine import SessionStateMachine
from core.security.rate_limiter import RateLimiter
from core.security.anti_replay import ReplayWindow
from core.metrics.recovery_metrics import RecoveryMetrics
from core.observability.event_bus import EventBus


class RuntimeControllerWithEvents:
    def __init__(self, session_id: str, policy, event_bus: EventBus):
        self.session_id = session_id
        self.policy = policy
        self.bus = event_bus

        self.state_machine = SessionStateMachine(session_id)
        self.rate_limiter = RateLimiter(policy.max_switches_per_minute)
        self.replay_window = ReplayWindow(policy.replay_window_size)
        self.metrics = RecoveryMetrics(session_id)

        self.transport_alive = True
        self.transport_death_timestamp: Optional[int] = None

        # Emit initial
        self._emit("SESSION_CREATED", ReasonCode.SESSION_CREATED, {})

    # ---------------------------------------------------------
    # Transport Signals
    # ---------------------------------------------------------

    def on_transport_dead(self, now_ms: int):
        if not self.transport_alive:
            return

        self.transport_alive = False
        self.transport_death_timestamp = now_ms

        self.state_machine.transition(SessionState.RECOVERING, ReasonCode.TRANSPORT_DEAD)
        self.metrics.mark_recovery_start(now_ms)

        self._emit("TRANSPORT_DEAD", ReasonCode.TRANSPORT_DEAD, {"now_ms": now_ms})
        self._emit("STATE_CHANGE", ReasonCode.TRANSPORT_DEAD, {"to": "RECOVERING"})

    def on_transport_restored(self, now_ms: int):
        if not self.state_machine.can_transition(SessionState.ATTACHED):
            return

        self.transport_alive = True

        self.state_machine.transition(SessionState.ATTACHED, ReasonCode.REATTACH_SUCCESS)
        self.metrics.mark_recovery_end(now_ms)

        self._emit("TRANSPORT_SWITCH", ReasonCode.REATTACH_SUCCESS, {"now_ms": now_ms})
        self._emit("STATE_CHANGE", ReasonCode.REATTACH_SUCCESS, {"to": "ATTACHED"})

    # ---------------------------------------------------------
    # Reattach Handling
    # ---------------------------------------------------------

    def attempt_reattach(self, nonce: int, now_ms: int) -> bool:
        # Replay
        if not self.replay_window.accept(nonce):
            self._emit("SECURITY_REJECT", ReasonCode.REPLAY_REJECTED, {"nonce": nonce})
            return False

        # Rate limit
        if not self.rate_limiter.allow(now_ms):
            self._emit("POLICY_REJECT", ReasonCode.SWITCH_RATE_LIMIT, {"now_ms": now_ms})
            return False

        # Recovery window
        if self._recovery_window_expired(now_ms):
            self.state_machine.transition(SessionState.TERMINATED, ReasonCode.RECOVERY_WINDOW_EXPIRED)
            self._emit("STATE_CHANGE", ReasonCode.RECOVERY_WINDOW_EXPIRED, {"to": "TERMINATED"})
            return False

        self._emit("REATTACH_ALLOWED", ReasonCode.REATTACH_ALLOWED, {"nonce": nonce, "now_ms": now_ms})
        return True

    # ---------------------------------------------------------
    # Policy Enforcement
    # ---------------------------------------------------------

    def enforce_policy(self, now_ms: int):
        if self.state_machine.current_state == SessionState.RECOVERING:
            if self._recovery_window_expired(now_ms):
                self.state_machine.transition(SessionState.TERMINATED, ReasonCode.RECOVERY_WINDOW_EXPIRED)
                self._emit("STATE_CHANGE", ReasonCode.RECOVERY_WINDOW_EXPIRED, {"to": "TERMINATED"})

    def _recovery_window_expired(self, now_ms: int) -> bool:
        if self.transport_death_timestamp is None:
            return False
        return (now_ms - self.transport_death_timestamp) > self.policy.max_recovery_window_ms

    # ---------------------------------------------------------
    # Observability helpers
    # ---------------------------------------------------------

    def _emit(self, event_type: str, reason: ReasonCode, details: dict):
        self.bus.emit(
            event_type=event_type,
            session_id=self.session_id,
            state_version=self.state_machine.state_version,
            reason_code=reason.value,
            details=details,
        )

    def debug_snapshot(self):
        return {
            "session_id": self.session_id,
            "state": self.state_machine.current_state.name,
            "state_version": self.state_machine.state_version,
            "transport_alive": self.transport_alive,
            "metrics": self.metrics.snapshot(),
        }