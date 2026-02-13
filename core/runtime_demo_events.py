"""
Runtime Demo (Event Stream) — Jumping VPN (Preview)

Demonstrates:
- session creation
- transport death
- bounded reattach
- replay rejection
- switch + return to ATTACHED
- JSONL audit stream output (non-blocking)

No sockets. No crypto. Behavior-only.
"""

from dataclasses import dataclass

from core.orchestrator.transport_manager import TransportCandidate, TransportManager
from core.observability.event_bus import EventBus, stdout_sink, jsonl_file_sink
from core.orchestrator.runtime_with_events import RuntimeControllerWithEvents


@dataclass
class DemoPolicy:
    max_recovery_window_ms: int = 4000
    max_switches_per_minute: int = 10
    replay_window_size: int = 64


def ms(t: int) -> int:
    return t


def main():
    # Event bus + sinks
    bus = EventBus()
    bus.add_sink(stdout_sink)
    bus.add_sink(jsonl_file_sink("out/runtime_audit.jsonl"))

    # Ensure out/ exists (on many setups it will already exist)
    # If not, create it manually in GitHub UI: out/ (folder)

    policy = DemoPolicy()

    # Orchestrator pieces
    rt = RuntimeControllerWithEvents(session_id="SESSION_EVT_01", policy=policy, event_bus=bus)
    tm = TransportManager(max_candidates=4, candidate_ttl_ms=30_000)

    now = ms(0)

    # Candidates (primary + backup)
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

    sel = tm.select_active(now)
    bus.emit(
        event_type="TRANSPORT_SELECTED",
        session_id="SESSION_EVT_01",
        state_version=0,
        reason_code="ACTIVE_SELECTED",
        details={"active": sel.selected.transport_id if sel.selected else None},
    )

    # Step: transport dies
    now = ms(1200)
    rt.on_transport_dead(now_ms=now)
    tm.clear_active()

    # Step: bounded reattach
    now = ms(1500)
    backup = tm.pick_backup(now)
    allowed = rt.attempt_reattach(nonce=1, now_ms=now)

    # Replay should be rejected
    _ = rt.attempt_reattach(nonce=1, now_ms=now + 10)

    if allowed and backup:
        tm.select_active(now)
        rt.on_transport_restored(now_ms=now)

    # enforce policy later (should remain ATTACHED)
    now = ms(3000)
    rt.enforce_policy(now_ms=now)

    bus.emit(
        event_type="SNAPSHOT",
        session_id="SESSION_EVT_01",
        state_version=rt.state_machine.state_version,
        reason_code="FINAL",
        details=rt.debug_snapshot(),
    )


if __name__ == "__main__":
    main()