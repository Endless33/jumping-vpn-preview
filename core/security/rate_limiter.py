"""
Jumping VPN — Control-Plane Rate Limiter (Preview)

Purpose:
Prevent control-plane abuse (reattach floods, switching amplification)
with deterministic, bounded behavior.

This module is:
- dependency-free
- deterministic
- bounded memory
- per-session and global limiting (optional)

It is designed for control-plane operations such as:
- REATTACH_REQUEST
- HANDSHAKE_INIT
- TRANSPORT_SWITCH attempts

Security principle:
Control-plane must not become an amplification vector.

Session is the anchor. Transport is volatile.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Tuple


class RateLimitDecision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class ReasonCode(str, Enum):
    RATE_LIMIT_OK = "RATE_LIMIT_OK"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    BURST_EXCEEDED = "BURST_EXCEEDED"


@dataclass
class RateLimitPolicy:
    """
    Token bucket parameters.

    - refill_per_sec: steady state allowed rate
    - burst: maximum bucket size (short burst capacity)

    Example:
    refill_per_sec=2, burst=5
    => allow up to 5 immediate operations, then ~2 per second sustained.
    """
    refill_per_sec: float = 2.0
    burst: float = 5.0


@dataclass
class TokenBucket:
    tokens: float
    last_ts_ms: int


@dataclass(frozen=True)
class RateLimitResult:
    decision: str
    reason_code: str
    remaining_tokens: float
    retry_after_ms: int = 0


class RateLimiter:
    """
    Deterministic token-bucket rate limiter.

    Use cases:
    - per-session limit: session_id -> bucket
    - global limit: use key="__GLOBAL__"

    Memory is bounded by the number of active keys.
    Expiration/cleanup can be implemented by caller if needed.
    """

    def __init__(self, policy: Optional[RateLimitPolicy] = None):
        self.policy = policy or RateLimitPolicy()
        self._buckets: Dict[str, TokenBucket] = {}

    def check(self, key: str, now_ms: int, cost: float = 1.0) -> RateLimitResult:
        """
        Check and consume tokens for given key.

        - cost: how many tokens an operation costs (default 1)
        """
        b = self._buckets.get(key)
        if b is None:
            # Initialize full bucket
            b = TokenBucket(tokens=self.policy.burst, last_ts_ms=now_ms)
            self._buckets[key] = b

        # Refill
        self._refill(b, now_ms)

        # Burst exceeded if cost > burst (misconfiguration / attacker attempt)
        if cost > self.policy.burst:
            return RateLimitResult(
                decision=RateLimitDecision.DENY.value,
                reason_code=ReasonCode.BURST_EXCEEDED.value,
                remaining_tokens=b.tokens,
                retry_after_ms=0,
            )

        if b.tokens >= cost:
            b.tokens -= cost
            return RateLimitResult(
                decision=RateLimitDecision.ALLOW.value,
                reason_code=ReasonCode.RATE_LIMIT_OK.value,
                remaining_tokens=b.tokens,
                retry_after_ms=0,
            )

        # Deny: calculate deterministic retry_after
        # tokens needed = cost - tokens
        need = cost - b.tokens
        # time to refill need tokens
        # refill_per_sec tokens/sec => refill_per_ms = refill_per_sec / 1000
        refill_per_ms = self.policy.refill_per_sec / 1000.0
        if refill_per_ms <= 0:
            retry_ms = 1000  # defensive default
        else:
            retry_ms = int((need / refill_per_ms) + 0.999)  # ceil

        return RateLimitResult(
            decision=RateLimitDecision.DENY.value,
            reason_code=ReasonCode.RATE_LIMIT_EXCEEDED.value,
            remaining_tokens=b.tokens,
            retry_after_ms=max(0, retry_ms),
        )

    def _refill(self, b: TokenBucket, now_ms: int) -> None:
        if now_ms <= b.last_ts_ms:
            # deterministic: no negative time
            return

        elapsed_ms = now_ms - b.last_ts_ms
        add = (elapsed_ms / 1000.0) * self.policy.refill_per_sec

        b.tokens = min(self.policy.burst, b.tokens + add)
        b.last_ts_ms = now_ms

    def debug_snapshot(self, key: str, now_ms: int) -> Dict[str, float]:
        b = self._buckets.get(key)
        if b is None:
            return {
                "tokens": self.policy.burst,
                "burst": self.policy.burst,
                "refill_per_sec": self.policy.refill_per_sec,
            }

        # simulate refill without mutating state for debug
        elapsed_ms = max(0, now_ms - b.last_ts_ms)
        add = (elapsed_ms / 1000.0) * self.policy.refill_per_sec
        tokens = min(self.policy.burst, b.tokens + add)

        return {
            "tokens": float(tokens),
            "burst": float(self.policy.burst),
            "refill_per_sec": float(self.policy.refill_per_sec),
        }


def example_usage() -> Tuple[RateLimitResult, RateLimitResult, RateLimitResult]:
    """
    Example (not executed automatically):

    - Allow burst
    - Deny after burst
    - Show retry_after_ms
    """
    rl = RateLimiter(RateLimitPolicy(refill_per_sec=1.0, burst=2.0))
    now = 1000

    r1 = rl.check("sess_demo_001", now)        # allow (2->1)
    r2 = rl.check("sess_demo_001", now + 1)    # allow (1->0)
    r3 = rl.check("sess_demo_001", now + 2)    # deny (0 tokens)

    return r1, r2, r3