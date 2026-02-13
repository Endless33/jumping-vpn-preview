from __future__ import annotations

from typing import Dict, Optional
from threading import RLock

from core.common.models import SessionRecord
from core.common.reason_codes import ReasonCode
from core.common.errors import RejectError
from core.common.invariants import assert_not_terminated


class SessionStore:
    """
    Authoritative in-memory session ownership store.

    Production notes:
    - In clustered deployments this layer must be replaced
      by a distributed store with atomic CAS semantics.
    - This implementation models single-node authoritative ownership.
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, SessionRecord] = {}
        self._lock = RLock()

    # ----------------------------
    # Basic CRUD
    # ----------------------------

    def get(self, session_id: str) -> Optional[SessionRecord]:
        with self._lock:
            return self._sessions.get(session_id)

    def create(self, record: SessionRecord) -> None:
        with self._lock:
            if record.session_id in self._sessions:
                raise RejectError(
                    reason=ReasonCode.INVALID_STATE_TRANSITION,
                    message="Session already exists",
                )
            self._sessions[record.session_id] = record

    def delete(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)

    # ----------------------------
    # Ownership / CAS semantics
    # ----------------------------

    def cas_update(
        self,
        session_id: str,
        expected_version: int,
        new_record: SessionRecord,
    ) -> None:
        """
        Compare-and-swap style update.

        Only applies update if state_version matches expected_version.
        Prevents rollback and concurrent mutation ambiguity.
        """
        with self._lock:
            current = self._sessions.get(session_id)
            if current is None:
                raise RejectError(
                    reason=ReasonCode.SESSION_NOT_FOUND,
                    message="Session not found",
                )

            if current.state_version != expected_version:
                raise RejectError(
                    reason=ReasonCode.INVALID_STATE_TRANSITION,
                    message="Version mismatch (CAS failed)",
                    details={
                        "expected": expected_version,
                        "actual": current.state_version,
                    },
                )

            self._sessions[session_id] = new_record

    # ----------------------------
    # Transport binding
    # ----------------------------

    def bind_transport(
        self,
        session_id: str,
        transport,
    ) -> None:
        """
        Bind transport to session.
        Must be called only after validation at higher layer.
        """
        with self._lock:
            rec = self._sessions.get(session_id)
            if rec is None:
                raise RejectError(
                    reason=ReasonCode.SESSION_NOT_FOUND,
                    message="Cannot bind transport: session not found",
                )

            assert_not_terminated(rec)

            rec.active_transport = transport

    def unbind_transport(
        self,
        session_id: str,
    ) -> None:
        with self._lock:
            rec = self._sessions.get(session_id)
            if rec is None:
                raise RejectError(
                    reason=ReasonCode.SESSION_NOT_FOUND,
                    message="Cannot unbind: session not found",
                )

            rec.active_transport = None

    # ----------------------------
    # TTL enforcement
    # ----------------------------

    def enforce_ttl(
        self,
        session_id: str,
        now_ms: int,
    ) -> Optional[ReasonCode]:
        """
        Enforce:
        - session TTL
        - transport-loss TTL

        Returns:
            None if still valid
            ReasonCode if termination required
        """
        with self._lock:
            rec = self._sessions.get(session_id)
            if rec is None:
                return None

            # Session lifetime TTL
            if now_ms - rec.created_ts_ms > rec.session_ttl_ms:
                return ReasonCode.SESSION_TTL_EXPIRED

            # Transport-loss TTL
            if (
                rec.active_transport is None
                and now_ms - rec.last_state_change_ts_ms
                > rec.transport_loss_ttl_ms
            ):
                return ReasonCode.TRANSPORT_TTL_EXPIRED

            return None

    # ----------------------------
    # Debug / Introspection
    # ----------------------------

    def list_sessions(self) -> Dict[str, SessionRecord]:
        with self._lock:
            return dict(self._sessions)