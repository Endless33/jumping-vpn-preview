"""
Transport Manager — Jumping VPN (Preview)

Manages transport candidates and deterministic selection.

This module does NOT open sockets.
It models:
- candidate discovery
- active transport selection
- competition resolution
- retirement of old transports

Only one ACTIVE transport is allowed.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class TransportCandidate:
    """
    Abstract transport candidate descriptor.
    No networking details beyond identity and metadata.
    """
    transport_id: str
    proto: str                 # "udp" | "tcp" | "quic" | etc.
    remote: str                # "ip:port" or abstract endpoint
    priority: int              # lower is better (deterministic ordering)
    observed_rtt_ms: int
    observed_loss_pct: float
    last_seen_ms: int


@dataclass(frozen=True)
class SelectionResult:
    selected: Optional[TransportCandidate]
    reason: str
    candidates_considered: int


class TransportManager:
    """
    Holds candidate set and deterministically selects an active transport.

    Determinism rule:
    Sort by (priority, observed_loss_pct, observed_rtt_ms, transport_id)
    """

    def __init__(self, *, max_candidates: int = 8, candidate_ttl_ms: int = 15_000):
        self.max_candidates = max_candidates
        self.candidate_ttl_ms = candidate_ttl_ms

        self._candidates: Dict[str, TransportCandidate] = {}
        self._active_id: Optional[str] = None
        self._last_switch_ms: Optional[int] = None

    # ---------------------------------------------------------
    # Candidate Management
    # ---------------------------------------------------------

    def upsert_candidate(self, cand: TransportCandidate, now_ms: int) -> None:
        """
        Add or update a candidate. Enforces bounded candidate set.
        """
        self._candidates[cand.transport_id] = cand
        self._evict_stale(now_ms)
        self._evict_overflow(now_ms)

    def remove_candidate(self, transport_id: str) -> None:
        self._candidates.pop(transport_id, None)
        if self._active_id == transport_id:
            self._active_id = None

    def has_candidates(self) -> bool:
        return len(self._candidates) > 0

    def list_candidates(self) -> List[TransportCandidate]:
        return list(self._candidates.values())

    # ---------------------------------------------------------
    # Active Selection
    # ---------------------------------------------------------

    def active_transport(self) -> Optional[TransportCandidate]:
        if self._active_id is None:
            return None
        return self._candidates.get(self._active_id)

    def last_switch_ms(self) -> Optional[int]:
        return self._last_switch_ms

    def clear_active(self) -> None:
        """
        Used when transport is declared dead.
        """
        self._active_id = None

    def select_active(self, now_ms: int) -> SelectionResult:
        """
        Deterministically select best candidate and set as active.
        """
        self._evict_stale(now_ms)
        if not self._candidates:
            return SelectionResult(selected=None, reason="NO_CANDIDATES", candidates_considered=0)

        ranked = self._ranked_candidates()
        selected = ranked[0]

        prev = self._active_id
        self._active_id = selected.transport_id

        if prev != self._active_id:
            self._last_switch_ms = now_ms
            reason = "ACTIVE_SELECTED_SWITCH"
        else:
            reason = "ACTIVE_SELECTED_NO_CHANGE"

        return SelectionResult(
            selected=selected,
            reason=reason,
            candidates_considered=len(ranked),
        )

    def pick_backup(self, now_ms: int) -> Optional[TransportCandidate]:
        """
        Return the next-best candidate (backup), without activating it.
        """
        self._evict_stale(now_ms)
        ranked = self._ranked_candidates()
        if not ranked:
            return None
        if self._active_id is None:
            return ranked[0]
        for c in ranked:
            if c.transport_id != self._active_id:
                return c
        return None

    # ---------------------------------------------------------
    # Deterministic Ranking
    # ---------------------------------------------------------

    def _ranked_candidates(self) -> List[TransportCandidate]:
        return sorted(
            self._candidates.values(),
            key=lambda c: (
                c.priority,
                c.observed_loss_pct,
                c.observed_rtt_ms,
                c.transport_id,
            ),
        )

    # ---------------------------------------------------------
    # Bounds / Eviction
    # ---------------------------------------------------------

    def _evict_stale(self, now_ms: int) -> None:
        stale_ids = [
            tid for tid, c in self._candidates.items()
            if (now_ms - c.last_seen_ms) > self.candidate_ttl_ms
        ]
        for tid in stale_ids:
            self.remove_candidate(tid)

    def _evict_overflow(self, now_ms: int) -> None:
        """
        Keep only best N candidates deterministically.
        """
        if len(self._candidates) <= self.max_candidates:
            return
        ranked = self._ranked_candidates()
        keep = set(c.transport_id for c in ranked[: self.max_candidates])
        for tid in list(self._candidates.keys()):
            if tid not in keep:
                self.remove_candidate(tid)