from __future__ import annotations

from core.common.errors import InvariantError
from core.common.reason_codes import ReasonCode
from core.common.models import SessionRecord, SessionState, TransportBinding


def assert_not_terminated(rec: SessionRecord) -> None:
    if rec.state == SessionState.TERMINATED:
        raise InvariantError(
            reason=ReasonCode.INVALID_STATE_TRANSITION,
            message="Operation attempted on a TERMINATED session",
            details={"session_id": rec.session_id},
        )


def assert_state_version_monotonic(old_version: int, new_version: int) -> None:
    if new_version <= old_version:
        raise InvariantError(
            reason=ReasonCode.INVARIANT_VIOLATION,
            message="State version rollback detected",
            details={"old_version": old_version, "new_version": new_version},
        )


def assert_single_active_binding(rec: SessionRecord) -> None:
    """
    In this model, 'single-active' is represented by exactly one field:
    rec.active_transport. So we enforce consistency rules around it.
    """
    # If ATTACHED, we MUST have an active transport
    if rec.state == SessionState.ATTACHED and rec.active_transport is None:
        raise InvariantError(
            reason=ReasonCode.INVARIANT_VIOLATION,
            message="ATTACHED session has no active transport",
            details={"session_id": rec.session_id},
        )

    # If TERMINATED, we MUST NOT have an active transport
    if rec.state == SessionState.TERMINATED and rec.active_transport is not None:
        raise InvariantError(
            reason=ReasonCode.INVARIANT_VIOLATION,
            message="TERMINATED session still has active transport bound",
            details={"session_id": rec.session_id},
        )


def assert_transport_has_identity(binding: TransportBinding) -> None:
    """
    TransportBinding must be well-formed (no empty identifiers).
    """
    if not binding.transport_id or not binding.remote_ip or not binding.proto:
        raise InvariantError(
            reason=ReasonCode.INVARIANT_VIOLATION,
            message="Malformed transport binding",
            details={
                "transport_id": binding.transport_id,
                "remote_ip": binding.remote_ip,
                "proto": binding.proto,
            },
        )