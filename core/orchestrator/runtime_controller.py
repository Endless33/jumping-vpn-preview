"""
Runtime Controller — Jumping VPN (Preview)

This module coordinates session lifecycle behavior.

It does NOT implement networking.
It orchestrates state transitions deterministically.
"""

from typing import Optional
from core.common.models import SessionState
from core.common.reason_codes import ReasonCode
from core.session.state_machine import SessionStateMachine
from core.security.rate_limiter import RateLimiter
from core.security.anti_replay import ReplayWindow
from core.metrics.recovery_metrics import RecoveryMetrics


class RuntimeController:
    """
    Coordinates session behavior under transport volatility.
    """

    def __init__(self, session_id: str, policy):
        self.session_id = session_id
        self.policy = policy

        self.state_machine = SessionStateMachine(session_id)
        self.rate_limiter = RateLimiter(policy.max_switches_per_minute)
        self.replay_window = ReplayWindow(policy.replay_window_size)
        self.metrics = RecoveryMetrics(session_id)

        self.transport_alive = True
        self.transport_death_timestamp: Optional[int] = None

    # ---------------------------------------------------------
    # Transport Signals
    # ---------------------------------------------------------

    def on_transport_dead(self, now_ms: int):
        """
        Triggered when transport is declared dead.
        """

        if not self.transport_alive:
            return  # already dead

        self.transport_alive = False
        self.transport_death_timestamp = now_ms

        self.state_machine.transition(
            SessionState.RECOVERING,
            ReasonCode.TRANSPORT_DEAD
        )

        self.metrics.mark_recovery_start(now_ms)

    def on_transport_restored(self, now_ms: int):
        """
        Triggered when reattach succeeds.
        """

        if not self.state_machine.can_transition(SessionState.ATTACHED):
            return

        self.transport_alive = True

        self.state_machine.transition(
            SessionState.ATTACHED,
            ReasonCode.REATTACH_SUCCESS
        )

        self.metrics.mark_recovery_end(now_ms)

    # ---------------------------------------------------------
    # Reattach Handling
    # ---------------------------------------------------------

    def attempt_reattach(self, nonce: int, now_ms: int) -> bool:
        """
        Attempt to reattach transport.

        Returns True if allowed, False if rejected.
        """

        # Replay protection
        if not self.replay_window.accept(nonce):
            return False

        # Rate limiting
        if not self.rate_limiter.allow(now_ms):
            return False

        # TTL check
        if self._recovery_window_expired(now_ms):
            self.state_machine.transition(
                SessionState.TERMINATED,
                ReasonCode.RECOVERY_WINDOW_EXPIRED
            )
            return False

        return True

    # ---------------------------------------------------------
    # Policy Enforcement
    # ---------------------------------------------------------

    def enforce_policy(self, now_ms: int):
        """
        Enforce recovery window expiration.
        """

        if self.state_machine.current_state == SessionState.RECOVERING:
            if self._recovery_window_expired(now_ms):
                self.state_machine.transition(
                    SessionState.TERMINATED,
                    ReasonCode.RECOVERY_WINDOW_EXPIRED
                )

    def _recovery_window_expired(self, now_ms: int) -> bool:
        if self.transport_death_timestamp is None:
            return False

        return (
            now_ms - self.transport_death_timestamp
            > self.policy.max_recovery_window_ms
        )

    # ---------------------------------------------------------
    # Observability
    # ---------------------------------------------------------

    def get_state(self):
        return self.state_machine.current_state

    def get_metrics(self):
        return self.metrics.snapshot()

    def debug_snapshot(self):
        return {
            "session_id": self.session_id,
            "state": self.state_machine.current_state.name,
            "transport_alive": self.transport_alive,
            "recovery_active": self.state_machine.current_state == SessionState.RECOVERING,
            "metrics": self.metrics.snapshot()
        }