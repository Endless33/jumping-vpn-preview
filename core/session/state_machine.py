from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from core.common.models import SessionRecord, SessionState, TransportBinding
from core.common.reason_codes import ReasonCode
from core.common.errors import RejectError
from core.common.invariants import (
    assert_not_terminated,
    assert_single_active_binding,
    assert_state_version_monotonic,
    assert_transport_has_identity,
)


@dataclass(frozen=True)
class SessionTransition:
    prev_state: SessionState
    new_state: SessionState
    reason: ReasonCode
    prev_version: int
    new_version: int
    transport_switched: bool


class SessionStateMachine:
    """
    Pure deterministic session state machine.
    No networking.
    No storage.
    No logging side effects.
    """

    def _bump_version(self, rec: SessionRecord) -> Tuple[int, int]:
        old_v = rec.state_version
        new_v = old_v + 1
        assert_state_version_monotonic(old_v, new_v)
        rec.state_version = new_v
        return old_v, new_v

    def attach(
        self,
        rec: SessionRecord,
        transport: TransportBinding,
        now_ms: int,
    ) -> SessionTransition:
        assert_not_terminated(rec)
        assert_transport_has_identity(transport)

        prev_state = rec.state
        prev_transport = rec.active_transport

        old_v, new_v = self._bump_version(rec)

        rec.state = SessionState.ATTACHED
        rec.active_transport = transport
        rec.last_activity_ts_ms = now_ms
        rec.last_state_change_ts_ms = now_ms

        assert_single_active_binding(rec)

        switched = (
            prev_transport is None
            or prev_transport.transport_id != transport.transport_id
        )

        return SessionTransition(
            prev_state=prev_state,
            new_state=SessionState.ATTACHED,
            reason=ReasonCode.TRANSPORT_SWITCH if switched else ReasonCode.NONE,
            prev_version=old_v,
            new_version=new_v,
            transport_switched=switched,
        )

    def enter_recovering(
        self,
        rec: SessionRecord,
        now_ms: int,
        reason: ReasonCode,
    ) -> SessionTransition:
        assert_not_terminated(rec)

        prev_state = rec.state

        old_v, new_v = self._bump_version(rec)

        rec.state = SessionState.RECOVERING
        rec.active_transport = None
        rec.last_state_change_ts_ms = now_ms

        assert_single_active_binding(rec)

        return SessionTransition(
            prev_state=prev_state,
            new_state=SessionState.RECOVERING,
            reason=reason,
            prev_version=old_v,
            new_version=new_v,
            transport_switched=False,
        )

    def degrade(
        self,
        rec: SessionRecord,
        now_ms: int,
        reason: ReasonCode,
    ) -> SessionTransition:
        assert_not_terminated(rec)

        prev_state = rec.state

        old_v, new_v = self._bump_version(rec)

        rec.state = SessionState.DEGRADED
        rec.last_state_change_ts_ms = now_ms

        assert_single_active_binding(rec)

        return SessionTransition(
            prev_state=prev_state,
            new_state=SessionState.DEGRADED,
            reason=reason,
            prev_version=old_v,
            new_version=new_v,
            transport_switched=False,
        )

    def terminate(
        self,
        rec: SessionRecord,
        now_ms: int,
        reason: ReasonCode,
    ) -> SessionTransition:
        assert_not_terminated(rec)

        prev_state = rec.state

        old_v, new_v = self._bump_version(rec)

        rec.state = SessionState.TERMINATED
        rec.active_transport = None
        rec.last_state_change_ts_ms = now_ms

        assert_single_active_binding(rec)

        return SessionTransition(
            prev_state=prev_state,
            new_state=SessionState.TERMINATED,
            reason=reason,
            prev_version=old_v,
            new_version=new_v,
            transport_switched=False,
        )