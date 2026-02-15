"""
Jumping VPN — One-command demo runner

What it does:
1) Ensures DEMO_TRACE.jsonl exists (creates a deterministic one if missing)
2) Validates the trace using demo_engine/replay.py (if available)
3) Runs live_demo.py (if available)
4) Prints a clean PASS/FAIL summary

Usage:
    python run_demo.py

Files:
    DEMO_TRACE.jsonl (created if missing)
    DEMO_OUTPUT.jsonl (created by live_demo.py)
"""

import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TRACE = ROOT / "DEMO_TRACE.jsonl"


TRACE_TEMPLATE = """\
{"ts_ms":1700000000000,"event":"SESSION_CREATED","session_id":"DEMO-SESSION","state":"ATTACHED","state_version":0}
{"ts_ms":1700000000200,"event":"PATH_SELECTED","session_id":"DEMO-SESSION","active_path":"udp:A","score":{"rtt_ms":24,"jitter_ms":3,"loss_pct":0.0},"cwnd_packets":64,"pacing_pps":1200}
{"ts_ms":1700000000500,"event":"TELEMETRY_TICK","session_id":"DEMO-SESSION","rtt_ms":25,"jitter_ms":4,"loss_pct":0.0,"cwnd_packets":72,"in_flight":18,"pacing_pps":1350}

{"ts_ms":1700000000800,"event":"VOLATILITY_SIGNAL","session_id":"DEMO-SESSION","reason":"LOSS_SPIKE","observed":{"loss_pct":7.5,"rtt_ms":41,"jitter_ms":18}}
{"ts_ms":1700000000810,"event":"STATE_CHANGE","session_id":"DEMO-SESSION","from":"ATTACHED","to":"VOLATILE","reason":"LOSS_SPIKE","state_version":1}
{"ts_ms":1700000000900,"event":"FLOW_CONTROL_UPDATE","session_id":"DEMO-SESSION","reason":"LOSS_REACTION","cwnd_packets":36,"pacing_pps":820}

{"ts_ms":1700000001100,"event":"TRANSPORT_SWITCH","session_id":"DEMO-SESSION","from_path":"udp:A","to_path":"udp:B","reason":"PREFERRED_PATH_CHANGED","bounded_by_policy":{"cooldown_ok":true,"switch_rate_ok":true}}
{"ts_ms":1700000001110,"event":"AUDIT_EVENT","session_id":"DEMO-SESSION","check":"NO_DUAL_ACTIVE_BINDING","result":"PASS"}
{"ts_ms":1700000001120,"event":"AUDIT_EVENT","session_id":"DEMO-SESSION","check":"NO_IDENTITY_RESET","result":"PASS"}

{"ts_ms":1700000001800,"event":"RECOVERY_SIGNAL","session_id":"DEMO-SESSION","observed":{"loss_pct":0.4,"rtt_ms":26,"jitter_ms":4}}
{"ts_ms":1700000001810,"event":"STATE_CHANGE","session_id":"DEMO-SESSION","from":"VOLATILE","to":"RECOVERING","reason":"STABILITY_WINDOW","state_version":2}
{"ts_ms":1700000002100,"event":"STATE_CHANGE","session_id":"DEMO-SESSION","from":"RECOVERING","to":"ATTACHED","reason":"RECOVERY_COMPLETE","state_version":3}
"""


def print_header():
    print("\nJumping VPN — Demo Runner")
    print("-------------------------\n")


def ensure_trace():
    if TRACE.exists() and TRACE.stat().st_size > 0:
        print(f"[OK] Found trace: {TRACE.name}")
        return

    TRACE.write_text(TRACE_TEMPLATE, encoding="utf-8")
    print(f"[OK] Created trace: {TRACE.name}")


def run_replay_validator():
    """
    Tries:
    - python demo_engine/replay.py DEMO_TRACE.jsonl
    - python -m demo_engine.replay DEMO_TRACE.jsonl
    If not present, prints SKIP.
    """
    candidates = [
        [sys.executable, str(ROOT / "demo_engine" / "replay.py"), str(TRACE)],
        [sys.executable, "-m", "demo_engine.replay", str(TRACE)],
    ]

    print("\n[STEP] Validate trace (demo_engine/replay.py)")
    for cmd in candidates:
        try:
            # Only run if the target script exists when using path-based call
            if cmd[1].endswith("replay.py") and not Path(cmd[1]).exists():
                continue

            r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
            out = (r.stdout or "") + (("\n" + r.stderr) if r.stderr else "")
            out = out.strip()

            if r.returncode == 0:
                print("[PASS] Trace validation succeeded.")
                if out:
                    print(out)
                return True
            else:
                print("[FAIL] Trace validation failed.")
                if out:
                    print(out)
                return False
        except Exception as ex:
            # try next candidate
            last_ex = ex
            continue

    print("[SKIP] replay validator not found. (Add demo_engine/replay.py to enable validation.)")
    return None


def run_live_demo():
    """
    Runs live_demo.py if it exists.
    """
    live = ROOT / "live_demo.py"
    print("\n[STEP] Live demo (live_demo.py)")
    if not live.exists():
        print("[SKIP] live_demo.py not found.")
        return None

    r = subprocess.run([sys.executable, str(live)], cwd=str(ROOT))
    if r.returncode == 0:
        print("[PASS] Live demo finished.")
        return True
    print("[FAIL] Live demo failed.")
    return False


def main():
    print_header()
    ensure_trace()

    v = run_replay_validator()
    l = run_live_demo()

    print("\nSummary")
    print("-------")
    if v is False or l is False:
        print("[FAIL] Demo did not complete cleanly.")
        sys.exit(1)

    if v is None and l is None:
        print("[OK] Trace exists, but validator and live demo are missing.")
        print("     Add demo_engine/replay.py and live_demo.py for full one-command demo.")
        sys.exit(0)

    print("[OK] Demo completed.")
    if v is None:
        print("     (Validator skipped)")
    if l is None:
        print("     (Live demo skipped)")
    sys.exit(0)


if __name__ == "__main__":
    main()