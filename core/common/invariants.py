from __future__ import annotations

from core.common.errors import InvariantError
from core.common.reason_codes import ReasonCode
from core.common.models import Session, TransportBinding, SessionState


def assert_single_active_binding(session: Session) -> None:
    """
    Ensures a session has at most one active transport binding.
    """
    active = [t for t in session.transports if t.active]
    if len(active) > 1:
        raise InvariantError(
            reason=ReasonCode.DUAL_ACTIVE_BINDING,
            message="Multiple active transport bindings detected",
            details={"active_count": len(active)}
        )


def assert_session_not_terminated(session: Session) -> None:
    """
    Prevents illegal transitions after termination.
    """
    if session.state == SessionState.TERMINATED:
        raise InvariantError(
            reason=ReasonCode.ILLEGAL_STATE_TRANSITION,
            message="Operation attempted on terminated session"
        )


def assert_state_version_monotonic(previous_version: int, new_version: int) -> None:
    """
    Ensures state version never rolls back.
    """
    if new_version <= previous_version:
        raise InvariantError(
            reason=ReasonCode.VERSION_ROLLBACK,
            message="State version rollback detected",
            details={
                "previous_version": previous_version,
                "new_version": new_version,
            }
        )


def assert_transport_belongs_to_session(
    session: Session,
    transport: TransportBinding
) -> None:
    """
    Ensures a transport binding belongs to the session.
    """
    if transport.session_id != session.session_id:
        raise InvariantError(
            reason=ReasonCode.TRANSPORT_SESSION_MISMATCH,
            message="Transport binding does not belong to session",
            details={
                "session_id": session.session_id,
                "transport_session_id": transport.session_id,
            }
        )