"""
Jumping VPN — Demo Runner

This script validates the deterministic demo trace and proves
session continuity under transport volatility.

Usage:

    python run_demo.py

Output:

    SESSION_CREATED OK
    VOLATILITY_SIGNAL OK
    TRANSPORT_SWITCH OK
    STATE_CHANGE OK
    RECOVERY_COMPLETE OK

    Trace validated successfully.
"""

import os
import sys

TRACE_FILE = "DEMO_TRACE.jsonl"


def main():
    print("\nJumping VPN — Demo Runner")
    print("-------------------------")

    if not os.path.exists(TRACE_FILE):
        print(f"ERROR: {TRACE_FILE} not found in repository root.")
        print("Make sure DEMO_TRACE.jsonl exists.")
        sys.exit(1)

    try:
        from demo_engine.replay import validate_trace
    except ImportError:
        print("ERROR: demo_engine.replay module not found.")
        print("Make sure demo_engine/replay.py exists.")
        sys.exit(1)

    print(f"Loading trace: {TRACE_FILE}\n")

    ok = validate_trace(TRACE_FILE)

    print()

    if ok:
        print("Trace validated successfully.")
        print("Session continuity preserved.")
    else:
        print("Trace validation failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()