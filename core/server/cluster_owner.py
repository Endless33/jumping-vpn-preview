"""
Cluster Ownership — Jumping VPN (Preview)

Defines an authoritative ownership model for sessions in clustered deployments.

Goal:
- Exactly one owner per session
- Reject on ambiguity
- Prevent dual-active binding

This is a behavioral skeleton, not a full consensus algorithm.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class OwnershipRecord:
    session_id: str
    owner_node_id: str
    owner_epoch: int          # monotonic, bumps on ownership transfer
    state_version: int        # monotonic, bumps on state mutation


@dataclass(frozen=True)
class OwnershipResult:
    ok: bool
    reason: str
    record: Optional[OwnershipRecord] = None


class ClusterOwner:
    """
    In-memory ownership registry (preview).
    In production, this would be backed by:
    - sticky routing OR
    - atomic shared store (CAS/transactions)
    """

    def __init__(self, node_id: str):
        self.node_id = node_id
        self._table: dict[str, OwnershipRecord] = {}

    def get(self, session_id: str) -> Optional[OwnershipRecord]:
        return self._table.get(session_id)

    def create_owner(self, session_id: str) -> OwnershipResult:
        """
        Create initial ownership for a new session on this node.
        """
        if session_id in self._table:
            return OwnershipResult(False, "OWNERSHIP_ALREADY_EXISTS", self._table[session_id])

        rec = OwnershipRecord(
            session_id=session_id,
            owner_node_id=self.node_id,
            owner_epoch=0,
            state_version=0,
        )
        self._table[session_id] = rec
        return OwnershipResult(True, "OWNERSHIP_CREATED", rec)

    def assert_is_owner(self, session_id: str) -> OwnershipResult:
        """
        Validate that this node is the authoritative owner.
        """
        rec = self._table.get(session_id)
        if rec is None:
            return OwnershipResult(False, "OWNERSHIP_NOT_FOUND", None)

        if rec.owner_node_id != self.node_id:
            return OwnershipResult(False, "OWNERSHIP_CONFLICT", rec)

        return OwnershipResult(True, "OWNERSHIP_OK", rec)

    def transfer_owner(self, session_id: str, new_owner_node_id: str) -> OwnershipResult:
        """
        Explicit ownership transfer (controlled).
        """
        rec = self._table.get(session_id)
        if rec is None:
            return OwnershipResult(False, "OWNERSHIP_NOT_FOUND", None)

        # Only current owner can transfer
        if rec.owner_node_id != self.node_id:
            return OwnershipResult(False, "OWNERSHIP_TRANSFER_DENIED_NOT_OWNER", rec)

        if new_owner_node_id == rec.owner_node_id:
            return OwnershipResult(True, "OWNERSHIP_NO_CHANGE", rec)

        rec.owner_node_id = new_owner_node_id
        rec.owner_epoch += 1  # bump epoch to invalidate stale assumptions
        return OwnershipResult(True, "OWNERSHIP_TRANSFERRED", rec)

    def bump_state_version(self, session_id: str) -> OwnershipResult:
        """
        Owner-only version increment. Used to model CAS-like mutation.
        """
        res = self.assert_is_owner(session_id)
        if not res.ok or res.record is None:
            return res

        res.record.state_version += 1
        return OwnershipResult(True, "STATE_VERSION_BUMPED", res.record)