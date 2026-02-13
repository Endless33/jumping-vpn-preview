from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from core.common.reason_codes import ReasonCode


@dataclass(frozen=True)
class ProtocolError(Exception):
    """
    Base protocol error used for deterministic failure handling.
    Always carries a ReasonCode.
    """
    reason: ReasonCode
    message: str
    details: Optional[Dict[str, Any]] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "reason": self.reason.value,
            "message": self.message,
            "details": self.details or {},
        }


class RejectError(ProtocolError):
    """
    Deterministic rejection (no state mutation).
    Example: replay detected, auth fail, policy deny.
    """


class TerminateError(ProtocolError):
    """
    Deterministic termination (explicit state transition required).
    Example: TTL expired, invariant violation.
    """


class InvariantError(TerminateError):
    """
    Raised when a hard invariant is violated.
    These are correctness failures and must fail closed.
    """