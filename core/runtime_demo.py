"""
Runtime Demo — Jumping VPN (Preview)

A tiny, readable simulation showing:
- transport death
- bounded recovery
- replay gating
- rate-limit gating
- deterministic return to ATTACHED

No sockets. No crypto. No real VPN.
This is a behavior demo for reviewers.
"""

from dataclasses import dataclass
from typing import Optional

from core.orchestrator.runtime_controller import RuntimeController
from core.orchestrator.transport_manager import TransportCandidate, TransportManager
from core.policy.policy_engine import PolicyEngine, QualitySample


@dataclass
class DemoPolicy:
    # recovery bounds
    max_recovery_window_ms: int = 4000

    # switch abuse protection
    max_switches_per_minute: int = 10

    # replay
    replay_window_size: int = 64


def ms(t: int) -> int:
    return t


def main():
    policy = DemoPolicy()

    # Orchestrator pieces
    controller = RuntimeController(session_id="SESSION_DEMO_01", policy=policy)
    tm = TransportManager(max_candidates=4, candidate_ttl_ms=30_000)
    pe = PolicyEngine(
        max_consecutive_drops=3,
        degrade_after_ms=1500,
        volatile_loss_pct=3.0,
        volatile_rtt_ms=200,
        volatile_jitter_ms=60,
        switch_cooldown_ms=750,
    )

    now = ms(0)

    # Candidate set (primary + backup)
    tm.upsert_candidate(
        TransportCandidate(
            transport_id="udp-primary",
            proto="udp",
            remote="198.51.100.10:51820",
            priority=10,
            observed_rtt_ms=35,
            observed_loss_pct=0.1,
            last_seen_ms=now,
        ),
        now,
    )

    tm.upsert_candidate(
        TransportCandidate(
            transport_id="udp-backup",
            proto="udp",
            remote="203.0.113.55:51820",
            priority=20,
            observed_rtt_ms=55,
            observed_loss_pct=0.3,
            last_seen_ms=now,
        ),
        now,
    )

    # Select initial active
    sel = tm.select_active(now)
    print("SELECT:", sel.reason, sel.selected.transport_id if sel.selected else None)

    print("STATE:", controller.get_state().name, controller.debug_snapshot())

    # ---------------------------------------------------------
    # Step 1: Transport quality degrades (VOLATILE)
    # ---------------------------------------------------------
    now = ms(900)
    sample = QualitySample(
        loss_pct=5.5,
        rtt_ms=260,
        jitter_ms=90,
        consecutive_drops=1,
        last_ok_ms=ms(850),
        now_ms=now,
    )

    decision = pe.evaluate(
        sample,
        last_switch_ms=tm.last_switch_ms(),
        has_candidate_transport=(tm.pick_backup(now) is not None),
    )
    print("POLICY:", decision)

    # (In a full loop, you'd transition ATTACHED->VOLATILE here via state machine.
    # For demo: we jump to death next.)

    # ---------------------------------------------------------
    # Step 2: Transport dies -> RECOVERING
    # ---------------------------------------------------------
    now = ms(1400)
    controller.on_transport_dead(now_ms=now)
    tm.clear_active()
    print("STATE:", controller.get_state().name, controller.debug_snapshot())

    # ---------------------------------------------------------
    # Step 3: Attempt reattach (bounded + anti-replay + rate limit)
    # ---------------------------------------------------------
    now = ms(1600)

    # choose a backup candidate
    backup = tm.pick_backup(now)
    print("BACKUP:", backup.transport_id if backup else None)

    # send REATTACH_REQUEST (nonce=1)
    allowed = controller.attempt_reattach(nonce=1, now_ms=now)
    print("REATTACH_ALLOWED:", allowed)

    # replay attempt should be rejected (same nonce)
    replay_allowed = controller.attempt_reattach(nonce=1, now_ms=now + 10)
    print("REPLAY_ALLOWED (should be False):", replay_allowed)

    # if allowed, select new active and mark restored
    if allowed and backup:
        tm.select_active(now)
        controller.on_transport_restored(now_ms=now)

    print("STATE:", controller.get_state().name, controller.debug_snapshot())

    # ---------------------------------------------------------
    # Step 4: Enforce bounds (should remain stable)
    # ---------------------------------------------------------
    now = ms(3000)
    controller.enforce_policy(now_ms=now)
    print("STATE:", controller.get_state().name, controller.debug_snapshot())

    print("\nDONE.")


if __name__ == "__main__":
    main()