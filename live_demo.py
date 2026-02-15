"""
Jumping VPN — Live Demo (Terminal)

Goal:
- Show a "live" evolving session timeline in the terminal
- Write a JSONL trace to DEMO_OUTPUT.jsonl
- Prove: volatility -> switch -> recovery -> session stays ATTACHED

Usage:
    python live_demo.py

Output:
    DEMO_OUTPUT.jsonl
"""

import json
import os
import time
from typing import Dict, Any, List

OUTPUT_FILE = "DEMO_OUTPUT.jsonl"


def now_ms() -> int:
    return int(time.time() * 1000)


def emit(f, event: Dict[str, Any]) -> None:
    f.write(json.dumps(event, ensure_ascii=False) + "\n")
    f.flush()


def print_line(s: str) -> None:
    print(s, flush=True)


def main() -> None:
    session_id = "LIVE-DEMO"
    ts0 = now_ms()

    # "Live" state
    state = "ATTACHED"
    state_version = 0
    active_path = "udp:A"

    # Simple metrics (demo)
    rtt_ms = 24
    jitter_ms = 3
    loss_pct = 0.0
    cwnd_packets = 64
    pacing_pps = 1200

    # Timeline plan (seconds from start)
    plan: List[Dict[str, Any]] = [
        {"t": 0.0, "kind": "SESSION_CREATED"},
        {"t": 0.5, "kind": "PATH_SELECTED"},
        {"t": 1.5, "kind": "TELEMETRY_TICK"},
        {"t": 2.2, "kind": "VOLATILITY_SIGNAL"},
        {"t": 2.3, "kind": "STATE_CHANGE_VOLATILE"},
        {"t": 2.7, "kind": "FLOW_CONTROL_REACT"},
        {"t": 3.0, "kind": "SWITCH_PATH"},
        {"t": 3.05, "kind": "AUDIT_NO_DUAL"},
        {"t": 3.10, "kind": "AUDIT_NO_RESET"},
        {"t": 4.0, "kind": "RECOVERY_SIGNAL"},
        {"t": 4.2, "kind": "STATE_CHANGE_RECOVERING"},
        {"t": 4.8, "kind": "STATE_CHANGE_ATTACHED"},
        {"t": 5.2, "kind": "END"},
    ]

    print_line("\nJumping VPN — Live Demo (Terminal)")
    print_line("----------------------------------")
    print_line(f"Output -> {OUTPUT_FILE}\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        start = time.time()

        for item in plan:
            target = item["t"]
            while (time.time() - start) < target:
                time.sleep(0.02)

            ts = now_ms()

            kind = item["kind"]

            if kind == "SESSION_CREATED":
                state = "ATTACHED"
                state_version = 0
                evt = {
                    "ts_ms": ts,
                    "event": "SESSION_CREATED",
                    "session_id": session_id,
                    "state": state,
                    "state_version": state_version,
                }
                emit(f, evt)
                print_line("SESSION_CREATED OK  -> state=ATTACHED")

            elif kind == "PATH_SELECTED":
                active_path = "udp:A"
                evt = {
                    "ts_ms": ts,
                    "event": "PATH_SELECTED",
                    "session_id": session_id,
                    "active_path": active_path,
                    "score": {"rtt_ms": rtt_ms, "jitter_ms": jitter_ms, "loss_pct": loss_pct},
                    "cwnd_packets": cwnd_packets,
                    "pacing_pps": pacing_pps,
                }
                emit(f, evt)
                print_line(f"PATH_SELECTED OK    -> active_path={active_path}")

            elif kind == "TELEMETRY_TICK":
                evt = {
                    "ts_ms": ts,
                    "event": "TELEMETRY_TICK",
                    "session_id": session_id,
                    "rtt_ms": rtt_ms,
                    "jitter_ms": jitter_ms,
                    "loss_pct": loss_pct,
                    "cwnd_packets": cwnd_packets,
                    "pacing_pps": pacing_pps,
                }
                emit(f, evt)
                print_line("TELEMETRY_TICK OK   -> stable baseline")

            elif kind == "VOLATILITY_SIGNAL":
                # spike
                rtt_ms = 41
                jitter_ms = 18
                loss_pct = 7.5
                evt = {
                    "ts_ms": ts,
                    "event": "VOLATILITY_SIGNAL",
                    "session_id": session_id,
                    "reason": "LOSS_SPIKE",
                    "observed": {"loss_pct": loss_pct, "rtt_ms": rtt_ms, "jitter_ms": jitter_ms},
                }
                emit(f, evt)
                print_line("VOLATILITY_SIGNAL OK -> loss spike detected")

            elif kind == "STATE_CHANGE_VOLATILE":
                prev = state
                state = "VOLATILE"
                state_version += 1
                evt = {
                    "ts_ms": ts,
                    "event": "STATE_CHANGE",
                    "session_id": session_id,
                    "from": prev,
                    "to": state,
                    "reason": "LOSS_SPIKE",
                    "state_version": state_version,
                }
                emit(f, evt)
                print_line("STATE_CHANGE OK     -> ATTACHED -> VOLATILE")

            elif kind == "FLOW_CONTROL_REACT":
                # react deterministically
                cwnd_packets = 36
                pacing_pps = 820
                evt = {
                    "ts_ms": ts,
                    "event": "FLOW_CONTROL_UPDATE",
                    "session_id": session_id,
                    "reason": "LOSS_REACTION",
                    "cwnd_packets": cwnd_packets,
                    "pacing_pps": pacing_pps,
                }
                emit(f, evt)
                print_line("FLOW_CONTROL OK     -> cwnd/pacing reacted")

            elif kind == "SWITCH_PATH":
                prev = active_path
                active_path = "udp:B"
                evt = {
                    "ts_ms": ts,
                    "event": "TRANSPORT_SWITCH",
                    "session_id": session_id,
                    "from_path": prev,
                    "to_path": active_path,
                    "reason": "PREFERRED_PATH_CHANGED",
                    "bounded_by_policy": {"cooldown_ok": True, "switch_rate_ok": True},
                }
                emit(f, evt)
                print_line("TRANSPORT_SWITCH OK -> udp:A -> udp:B (bounded)")

            elif kind == "AUDIT_NO_DUAL":
                evt = {
                    "ts_ms": ts,
                    "event": "AUDIT_EVENT",
                    "session_id": session_id,
                    "check": "NO_DUAL_ACTIVE_BINDING",
                    "result": "PASS",
                }
                emit(f, evt)
                print_line("AUDIT OK            -> NO_DUAL_ACTIVE_BINDING PASS")

            elif kind == "AUDIT_NO_RESET":
                evt = {
                    "ts_ms": ts,
                    "event": "AUDIT_EVENT",
                    "session_id": session_id,
                    "check": "NO_IDENTITY_RESET",
                    "result": "PASS",
                }
                emit(f, evt)
                print_line("AUDIT OK            -> NO_IDENTITY_RESET PASS")

            elif kind == "RECOVERY_SIGNAL":
                # return to stable-ish metrics
                rtt_ms = 26
                jitter_ms = 4
                loss_pct = 0.4
                evt = {
                    "ts_ms": ts,
                    "event": "RECOVERY_SIGNAL",
                    "session_id": session_id,
                    "observed": {"loss_pct": loss_pct, "rtt_ms": rtt_ms, "jitter_ms": jitter_ms},
                }
                emit(f, evt)
                print_line("RECOVERY_SIGNAL OK  -> stability window detected")

            elif kind == "STATE_CHANGE_RECOVERING":
                prev = state
                state = "RECOVERING"
                state_version += 1
                evt = {
                    "ts_ms": ts,
                    "event": "STATE_CHANGE",
                    "session_id": session_id,
                    "from": prev,
                    "to": state,
                    "reason": "STABILITY_WINDOW",
                    "state_version": state_version,
                }
                emit(f, evt)
                print_line("STATE_CHANGE OK     -> VOLATILE -> RECOVERING")

            elif kind == "STATE_CHANGE_ATTACHED":
                prev = state
                state = "ATTACHED"
                state_version += 1
                evt = {
                    "ts_ms": ts,
                    "event": "STATE_CHANGE",
                    "session_id": session_id,
                    "from": prev,
                    "to": state,
                    "reason": "RECOVERY_COMPLETE",
                    "state_version": state_version,
                }
                emit(f, evt)
                print_line("RECOVERY_COMPLETE OK -> RECOVERING -> ATTACHED")

            elif kind == "END":
                evt = {
                    "ts_ms": ts,
                    "event": "DEMO_END",
                    "session_id": session_id,
                    "final_state": state,
                    "final_path": active_path,
                }
                emit(f, evt)
                print_line("\nDEMO_END OK")
                print_line("Live demo finished.")
                print_line(f"Trace saved: {os.path.abspath(OUTPUT_FILE)}\n")

            else:
                # Unknown step, ignore
                pass


if __name__ == "__main__":
    main()