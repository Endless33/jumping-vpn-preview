"""
Versioning Guard — Jumping VPN (Preview)

Provides monotonic state_version enforcement.

Core rule:
- All state mutations must be versioned.
- Stale updates must be rejected.
- Rollback is forbidden.

This module is used by server session stores and control-plane handlers.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class VersionCheckResult:
    ok: bool
    reason: str


class VersionGuard:
    """
    Enforces monotonic, CAS-like state version semantics.
    """

    @staticmethod
    def require_exact(current_version: int, incoming_version: int) -> VersionCheckResult:
        """
        Accept only if incoming_version equals current_version.
        """
        if incoming_version < 0:
            return VersionCheckResult(False, "VERSION_INVALID_NEGATIVE")

        if incoming_version != current_version:
            if incoming_version < current_version:
                return VersionCheckResult(False, "VERSION_STALE_REJECTED")
            return VersionCheckResult(False, "VERSION_FUTURE_REJECTED")

        return VersionCheckResult(True, "VERSION_MATCH")

    @staticmethod
    def next_version(current_version: int) -> int:
        """
        Compute next monotonic version.
        """
        if current_version < 0:
            raise ValueError("state_version cannot be negative")
        return current_version + 1