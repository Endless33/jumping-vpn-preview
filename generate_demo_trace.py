"""
Jumping VPN — Demo Trace Generator

This script generates a deterministic demo trace showing:

• session creation
• transport volatility
• transport switch
• recovery
• session continuity preservation

Output:
    DEMO_TRACE.jsonl

Usage:
    python generate_demo_trace.py
"""

import json
import time


OUTPUT_FILE = "DEMO_TRACE.jsonl"


def write_event(f, event):
    f.write(json.dumps(event) + "\n")


def generate_trace():

    session_id = "DEMO-SESSION"

    base_ts = 1700000000000

    events = [

        {
            "ts_ms": base_ts,
            "event": "SESSION_CREATED",
            "session_id": session_id,
            "state": "ATTACHED",
            "state_version": 0
        },

        {
            "ts_ms": base_ts + 200,
            "event": "PATH_SELECTED",
            "session_id": session_id,
            "active_path": "udp:A",
            "score": {
                "rtt_ms": 24,
                "jitter_ms": 3,
                "loss_pct": 0.0
            },
            "cwnd_packets": 64,
            "pacing_pps": 1200
        },

        {
            "ts_ms": base_ts + 800,
            "event": "VOLATILITY_SIGNAL",
            "session_id": session_id,
            "reason": "LOSS_SPIKE",
            "observed": {
                "loss_pct": 7.5,
                "rtt_ms": 41,
                "jitter_ms": 18
            }
        },

        {
            "ts_ms": base_ts + 810,
            "event": "STATE_CHANGE",
            "session_id": session_id,
            "from": "ATTACHED",
            "to": "VOLATILE",
            "reason": "LOSS_SPIKE",
            "state_version": 1
        },

        {
            "ts_ms": base_ts + 900,
            "event": "FLOW_CONTROL_UPDATE",
            "session_id": session_id,
            "reason": "LOSS_REACTION",
            "cwnd_packets": 36,
            "pacing_pps": 820
        },

        {
            "ts_ms": base_ts + 1100,
            "event": "TRANSPORT_SWITCH",
            "session_id": session_id,
            "from_path": "udp:A",
            "to_path": "udp:B",
            "reason": "PREFERRED_PATH_CHANGED"
        },

        {
            "ts_ms": base_ts + 1110,
            "event": "AUDIT_EVENT",
            "session_id": session_id,
            "check": "NO_DUAL_ACTIVE_BINDING",
            "result": "PASS"
        },

        {
            "ts_ms": base_ts + 1810,
            "event": "STATE_CHANGE",
            "session_id": session_id,
            "from": "RECOVERING",
            "to": "ATTACHED",
            "reason": "RECOVERY_COMPLETE",
            "state_version": 3
        }

    ]

    with open(OUTPUT_FILE, "w") as f:

        for event in events:
            write_event(f, event)

    print(f"\nDemo trace generated: {OUTPUT_FILE}")


if __name__ == "__main__":

    print("\nJumping VPN — Demo Trace Generator")
    print("----------------------------------")

    generate_trace()

    print("Done.\n")