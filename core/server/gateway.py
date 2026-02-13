from __future__ import annotations

import time
from typing import Optional

from core.common.models import (
    SessionRecord,
    SessionState,
    TransportBinding,
)
from core.common.reason_codes import ReasonCode
from core.common.errors import RejectError
from core.session.state_machine import StateMachine
from core.server.session_store import SessionStore


class Gateway:
    """
    Control-plane orchestration layer.

    Responsibilities:
    - Validate reattach
    - Enforce deterministic transitions
    - Bind / unbind transport
    - Enforce TTL
    - Prevent ambiguous ownership
    """

    def __init__(self, store: SessionStore):
        self.store = store

    # --------------------------------------------------
    # Session Establishment
    # --------------------------------------------------

    def create_session(
        self,
        session_id: str,
        session_ttl_ms: int,
        transport_loss_ttl_ms: int,
    ) -> SessionRecord:
        now = int(time.time() * 1000)

        record = SessionRecord(
            session_id=session_id,
            state=SessionState.BIRTH,
            state_version=0,
            created_ts_ms=now,
            last_state_change_ts_ms=now,
            session_ttl_ms=session_ttl_ms,
            transport_loss_ttl_ms=transport_loss_ttl_ms,
            active_transport=None,
        )

        self.store.create(record)

        # move to ATTACHED happens after transport bind
        return record

    # --------------------------------------------------
    # Transport Bind (Initial or Reattach)
    # --------------------------------------------------

    def bind_transport(
        self,
        session_id: str,
        transport: TransportBinding,
    ) -> SessionRecord:

        record = self._require_session(session_id)

        # TTL enforcement before bind
        self._enforce_ttl_or_raise(record)

        new_record = StateMachine.attach_transport(record)

        # CAS update to avoid race
        self.store.cas_update(
            session_id=session_id,
            expected_version=record.state_version,
            new_record=new_record,
        )

        self.store.bind_transport(session_id, transport)

        return new_record

    # --------------------------------------------------
    # Explicit Transport Death
    # --------------------------------------------------

    def transport_dead(self, session_id: str) -> SessionRecord:
        record = self._require_session(session_id)

        new_record = StateMachine.transport_dead(record)

        self.store.cas_update(
            session_id=session_id,
            expected_version=record.state_version,
            new_record=new_record,
        )

        self.store.unbind_transport(session_id)

        return new_record

    # --------------------------------------------------
    # Reattach Request (Validated externally)
    # --------------------------------------------------

    def reattach(
        self,
        session_id: str,
        transport: TransportBinding,
    ) -> SessionRecord:

        record = self._require_session(session_id)

        # TTL check before allowing reattach
        self._enforce_ttl_or_raise(record)

        new_record = StateMachine.reattach(record)

        self.store.cas_update(
            session_id=session_id,
            expected_version=record.state_version,
            new_record=new_record,
        )

        self.store.bind_transport(session_id, transport)

        return new_record

    # --------------------------------------------------
    # TTL Enforcement
    # --------------------------------------------------

    def enforce_ttl(self, session_id: str) -> Optional[ReasonCode]:
        record = self._require_session(session_id)

        now = int(time.time() * 1000)
        reason = self.store.enforce_ttl(session_id, now)

        if reason:
            terminated = StateMachine.terminate(record, reason)

            self.store.cas_update(
                session_id=session_id,
                expected_version=record.state_version,
                new_record=terminated,
            )

            self.store.unbind_transport(session_id)

        return reason

    # --------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------

    def _require_session(self, session_id: str) -> SessionRecord:
        record = self.store.get(session_id)
        if record is None:
            raise RejectError(
                reason=ReasonCode.SESSION_NOT_FOUND,
                message="Session not found",
            )
        return record

    def _enforce_ttl_or_raise(self, record: SessionRecord) -> None:
        now = int(time.time() * 1000)
        reason = self.store.enforce_ttl(record.session_id, now)
        if reason:
            raise RejectError(
                reason=reason,
                message="TTL expired, operation denied",
            )