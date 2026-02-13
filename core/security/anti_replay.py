"""
Jumping VPN — Anti-Replay / Freshness Gate (Preview)

Purpose:
Prevent control-plane replay (e.g., REATTACH_REQUEST reuse) and enforce freshness.

This is a contract-first security component:
- deterministic outcomes
- bounded memory
- explicit reason codes
- no crypto implementation here (proof-of-possession is assumed validated elsewhere)

How to use:
- For each session_id, track a monotonic nonce or strictly increasing counter.
- Accept only if:
    * nonce is greater than the highest seen OR
    * nonce is within a bounded forward window and not previously used
- Reject duplicates and stale nonces deterministically.

Session is the anchor. Transport is volatile.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Set, Tuple


class AntiReplayDecision(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT_STALE = "REJECT_STALE"
    REJECT_DUPLICATE = "REJECT_DUPLICATE"
    REJECT_WINDOW_EXCEEDED = "REJECT_WINDOW_EXCEEDED"
    REJECT_MISSING_NONCE = "REJECT_MISSING_NONCE"


class ReasonCode(str, Enum):
    NONCE_ACCEPTED = "NONCE_ACCEPTED"
    NONCE_STALE = "NONCE_STALE"
    NONCE_DUPLICATE = "NONCE_DUPLICATE"
    NONCE_WINDOW_EXCEEDED = "NONCE_WINDOW_EXCEEDED"
    NONCE_MISSING = "NONCE_MISSING"


@dataclass
class AntiReplayPolicy:
    """
    Policy knobs.

    - max_gap: how far ahead of last_seen_nonce we allow a new nonce to be,
      before rejecting as suspicious (prevents unbounded memory growth / abuse).
      Example: last_seen=100, max_gap=256 => allow up to 356.

    - track_window: size of "recently used" set we keep (bounded memory).
      This helps reject duplicates within the forward window.
    """
    max_gap: int = 256
    track_window: int = 512


@dataclass
class SessionReplayState:
    last_seen_nonce: int = -1
    # Track used nonces in a bounded window to reject duplicates.
    used_nonces: Set[int] = field(default_factory=set)

    # For deterministic pruning, keep a simple min/max view.
    min_tracked: int = 0
    max_tracked: int = 0


@dataclass(frozen=True)
class AntiReplayResult:
    decision: str
    reason_code: str
    last_seen_nonce: int
    accepted_nonce: Optional[int] = None


class AntiReplayWindow:
    """
    Per-session anti-replay window.

    Deterministic rules:
    - Missing nonce -> reject
    - Nonce <= last_seen_nonce AND already tracked -> duplicate reject
    - Nonce <= last_seen_nonce AND not tracked -> stale reject (out-of-order)
    - Nonce > last_seen_nonce:
        * If nonce - last_seen_nonce > max_gap -> window exceeded reject
        * Else accept:
            - advance last_seen_nonce
            - record nonce in used_nonces
            - prune used_nonces to bounded window
    """

    def __init__(self, policy: Optional[AntiReplayPolicy] = None):
        self.policy = policy or AntiReplayPolicy()
        self._sessions: Dict[str, SessionReplayState] = {}

    def get_state(self, session_id: str) -> SessionReplayState:
        st = self._sessions.get(session_id)
        if st is None:
            st = SessionReplayState()
            self._sessions[session_id] = st
        return st

    def validate_and_record(self, session_id: str, nonce: Optional[int]) -> AntiReplayResult:
        if nonce is None:
            st = self.get_state(session_id)
            return AntiReplayResult(
                decision=AntiReplayDecision.REJECT_MISSING_NONCE.value,
                reason_code=ReasonCode.NONCE_MISSING.value,
                last_seen_nonce=st.last_seen_nonce,
                accepted_nonce=None,
            )

        st = self.get_state(session_id)

        # Duplicate detection (within tracked window)
        if nonce in st.used_nonces:
            return AntiReplayResult(
                decision=AntiReplayDecision.REJECT_DUPLICATE.value,
                reason_code=ReasonCode.NONCE_DUPLICATE.value,
                last_seen_nonce=st.last_seen_nonce,
                accepted_nonce=None,
            )

        # Stale / out-of-order (nonce not tracked but <= last_seen)
        if nonce <= st.last_seen_nonce:
            return AntiReplayResult(
                decision=AntiReplayDecision.REJECT_STALE.value,
                reason_code=ReasonCode.NONCE_STALE.value,
                last_seen_nonce=st.last_seen_nonce,
                accepted_nonce=None,
            )

        # Forward window abuse check
        gap = nonce - st.last_seen_nonce
        if st.last_seen_nonce >= 0 and gap > self.policy.max_gap:
            return AntiReplayResult(
                decision=AntiReplayDecision.REJECT_WINDOW_EXCEEDED.value,
                reason_code=ReasonCode.NONCE_WINDOW_EXCEEDED.value,
                last_seen_nonce=st.last_seen_nonce,
                accepted_nonce=None,
            )

        # ACCEPT
        st.last_seen_nonce = nonce
        st.used_nonces.add(nonce)

        # Update min/max tracked deterministically
        if len(st.used_nonces) == 1:
            st.min_tracked = nonce
            st.max_tracked = nonce
        else:
            if nonce < st.min_tracked:
                st.min_tracked = nonce
            if nonce > st.max_tracked:
                st.max_tracked = nonce

        self._prune(st)

        return AntiReplayResult(
            decision=AntiReplayDecision.ACCEPT.value,
            reason_code=ReasonCode.NONCE_ACCEPTED.value,
            last_seen_nonce=st.last_seen_nonce,
            accepted_nonce=nonce,
        )

    def _prune(self, st: SessionReplayState) -> None:
        """
        Keep used_nonces bounded by track_window.

        Deterministic pruning rule:
        - keep only nonces in [last_seen_nonce - track_window + 1, last_seen_nonce]
        """
        if st.last_seen_nonce < 0:
            st.used_nonces.clear()
            st.min_tracked = 0
            st.max_tracked = 0
            return

        lower = st.last_seen_nonce - self.policy.track_window + 1
        if lower < 0:
            lower = 0

        # Remove anything below lower bound
        if not st.used_nonces:
            st.min_tracked = 0
            st.max_tracked = 0
            return

        to_remove = [n for n in st.used_nonces if n < lower]
        for n in to_remove:
            st.used_nonces.remove(n)

        # Recompute min/max deterministically if needed
        if st.used_nonces:
            st.min_tracked = min(st.used_nonces)
            st.max_tracked = max(st.used_nonces)
        else:
            st.min_tracked = 0
            st.max_tracked = 0

    def debug_snapshot(self, session_id: str) -> Dict[str, int]:
        st = self.get_state(session_id)
        return {
            "last_seen_nonce": st.last_seen_nonce,
            "tracked_count": len(st.used_nonces),
            "min_tracked": st.min_tracked,
            "max_tracked": st.max_tracked,
            "max_gap": self.policy.max_gap,
            "track_window": self.policy.track_window,
        }


def example_usage() -> Tuple[AntiReplayResult, AntiReplayResult, AntiReplayResult, Dict[str, int]]:
    """
    Example (not executed automatically):

    - Accept nonce 1
    - Reject duplicate nonce 1
    - Reject stale nonce 0
    """
    ar = AntiReplayWindow(AntiReplayPolicy(max_gap=8, track_window=16))

    r1 = ar.validate_and_record("sess_demo_001", 1)
    r2 = ar.validate_and_record("sess_demo_001", 1)
    r3 = ar.validate_and_record("sess_demo_001", 0)
    snap = ar.debug_snapshot("sess_demo_001")

    return r1, r2, r3, snap