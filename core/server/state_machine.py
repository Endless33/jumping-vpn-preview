from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from core.common.errors import TerminateError, RejectError
from core.common.invariants import (
    assert_not_terminated,
    assert_single_active_binding,
    assert_state_version_monotonic,
    assert_transport_has_identity,
)
from core.common.models import SessionRecord, SessionState, TransportBinding
from core.common.reason_codes import ReasonCode


@dataclass(frozen=True)
class TransitionResult:
    """
    Result of a state transition. Used for audit emission and handlers.
    """
    prev_state: SessionState
    new_state: SessionState
    reason: ReasonCode
    prev_version: int
    new_version: int
    switched_transport: bool = False
    old_transport_id: Optional[str] = None
    new_transport_id: Optional[str] = None


class StateMachine:
    """
    Deterministic transition engine.
    All state changes must pass through here.
    """

    def _bump_version(self, rec: SessionRecord) -> Tuple[int, int]:
        old_v = rec.state_version
        new_v = old_v + 1
        assert_state_version_monotonic(old_v, new_v)
        rec.state_version = new_v
        return old_v, new_v

    def transition(
        self,
        rec: SessionRecord,
        new_state: SessionState,
        reason: ReasonCode,
        now_ms: int,
        new_transport: Optional[TransportBinding] = None,
    ) -> TransitionResult:
        """
        Apply a state transition with optional transport binding update.
        Transport updates are explicit and audited.
        """
        assert_not_terminated(rec)

        prev_state = rec.state
        prev_transport_id = rec.active_transport.transport_id if rec.active_transport else None

        # Basic illegal transition checks (minimal but strict)
        if prev_state == SessionState.BIRTH and new_state not in (SessionState.ATTACHED, SessionState.TERMINATED):
            raise RejectError(
                reason=ReasonCode.INVALID_STATE_TRANSITION,
                message="Illegal transition from BIRTH",
                details={"from": prev_state.value, "to": new_state.value},
            )

        if new_state == SessionState.ATTACHED:
            if new_transport is None:
                raise RejectError(
                    reason=ReasonCode.INVALID_STATE_TRANSITION,
                    message="ATTACHED requires a transport binding",
                    details={"session_id": rec.session_id},
                )
            assert_transport_has_identity(new_transport)
            rec.active_transport = new_transport

        if new_state == SessionState.RECOVERING:
            # When recovering, we may have lost transport; allow active_transport to be None
            rec.active_transport = None

        if new_state == SessionState.TERMINATED:
            rec.active_transport = None

        # Apply the state + version + timestamps
        old_v, new_v = self._bump_version(rec)
        rec.state = new_state
        rec.last_state_change_ts_ms = now_ms
        rec.last_activity_ts_ms = now_ms

        # Enforce invariants after mutation
        assert_single_active_binding(rec)

        new_transport_id = rec.active_transport.transport_id if rec.active_transport else None
        switched = (prev_transport_id != new_transport_id) and (prev_transport_id is not None or new_transport_id is not None)

        return TransitionResult(
            prev_state=prev_state,
            new_state=new_state,
            reason=reason,
            prev_version=old_v,
            new_version=new_v,
            switched_transport=switched,
            old_transport_id=prev_transport_id,
            new_transport_id=new_transport_id,
        )

    def terminate_if_ttl_expired(self, rec: SessionRecord, now_ms: int) -> Optional[TransitionResult]:
        """
        Deterministically terminate if session TTL is exceeded.
        """
        if rec.created_ts_ms and (now_ms - rec.created_ts_ms) > rec.policy.session_ttl_ms:
            # Termination is explicit. Caller should audit it.
            # We use transition() to enforce invariants.
            return self.transition(
                rec=rec,
                new_state=SessionState.TERMINATED,
                reason=ReasonCode.SESSION_TTL_EXPIRED,
                now_ms=now_ms,
            )
        return None

    def terminate_if_transport_loss_ttl_expired(self, rec: SessionRecord, now_ms: int) -> Optional[TransitionResult]:
        """
        If no active transport exists and transport loss TTL exceeded => terminate.
        """
        if rec.active_transport is None:
            delta = now_ms - rec.last_activity_ts_ms
            if delta > rec.policy.transport_loss_ttl_ms and rec.state in (SessionState.RECOVERING, SessionState.VOLATILE, SessionState.DEGRADED):
                return self.transition(
                    rec=rec,
                    new_state=SessionState.TERMINATED,
                    reason=ReasonCode.TRANSPORT_TTL_EXPIRED,
                    now_ms=now_ms,
                )
        return None