"""
Policy Engine — Jumping VPN (Preview)

Deterministic policy evaluation for transport volatility.

This module decides:
- when quality is considered VOLATILE
- when transport is considered DEAD
- when switching is allowed
- when degradation/termination should occur

No heuristics, no randomness.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class QualitySample:
    """
    Transport quality signal snapshot.
    Values are unit-annotated and expected to be precomputed by adapters.
    """
    loss_pct: float          # 0..100
    rtt_ms: int              # >=0
    jitter_ms: int           # >=0
    consecutive_drops: int   # >=0
    last_ok_ms: int          # timestamp of last confirmed delivery
    now_ms: int              # current timestamp


@dataclass(frozen=True)
class PolicyDecision:
    """
    Deterministic decision output.
    """
    is_volatile: bool
    is_dead: bool
    should_switch: bool
    reason: str


class PolicyEngine:
    """
    Evaluates policy thresholds and returns deterministic decisions.
    """

    def __init__(
        self,
        *,
        max_consecutive_drops: int = 3,
        degrade_after_ms: int = 1500,
        volatile_loss_pct: float = 5.0,
        volatile_rtt_ms: int = 250,
        volatile_jitter_ms: int = 80,
        switch_cooldown_ms: int = 750,
    ):
        self.max_consecutive_drops = max_consecutive_drops
        self.degrade_after_ms = degrade_after_ms

        self.volatile_loss_pct = volatile_loss_pct
        self.volatile_rtt_ms = volatile_rtt_ms
        self.volatile_jitter_ms = volatile_jitter_ms

        self.switch_cooldown_ms = switch_cooldown_ms

    # ---------------------------------------------------------
    # Deterministic Evaluation
    # ---------------------------------------------------------

    def evaluate(
        self,
        sample: QualitySample,
        *,
        last_switch_ms: Optional[int],
        has_candidate_transport: bool
    ) -> PolicyDecision:
        """
        Deterministically evaluate volatility/death/switch eligibility.

        - is_dead: hard failure signal
        - is_volatile: soft failure signal
        - should_switch: only if candidate exists and cooldown allows
        """

        # Hard failure: too many consecutive drops OR no successful delivery for too long
        time_since_ok = max(0, sample.now_ms - sample.last_ok_ms)

        is_dead = (
            sample.consecutive_drops >= self.max_consecutive_drops
            or time_since_ok >= self.degrade_after_ms
        )

        # Soft failure: quality violations (loss/latency/jitter)
        is_volatile = (
            sample.loss_pct >= self.volatile_loss_pct
            or sample.rtt_ms >= self.volatile_rtt_ms
            or sample.jitter_ms >= self.volatile_jitter_ms
        )

        # Switch gating (deterministic cooldown)
        cooldown_ok = True
        if last_switch_ms is not None:
            cooldown_ok = (sample.now_ms - last_switch_ms) >= self.switch_cooldown_ms

        should_switch = bool(has_candidate_transport and cooldown_ok and (is_dead or is_volatile))

        # Reason codes (human-readable; map to ReasonCode enums elsewhere if needed)
        if is_dead and should_switch:
            reason = "TRANSPORT_DEAD_SWITCH_ALLOWED"
        elif is_dead and not should_switch:
            reason = "TRANSPORT_DEAD_NO_SWITCH_AVAILABLE"
        elif is_volatile and should_switch:
            reason = "QUALITY_VOLATILE_SWITCH_ALLOWED"
        elif is_volatile and not should_switch:
            reason = "QUALITY_VOLATILE_SWITCH_COOLDOWN_OR_NO_CANDIDATE"
        else:
            reason = "QUALITY_OK"

        return PolicyDecision(
            is_volatile=is_volatile,
            is_dead=is_dead,
            should_switch=should_switch,
            reason=reason
        )