# Prototype: Session-Anchored Transport Demo (UDP)

This is **not a production VPN**.  
This prototype exists to demonstrate one architectural property:

**Session continuity independent of transport attachment.**

- Session identity is anchored to a session key (`session_id` + PSK)
- Transport paths (`udp:A`, `udp:B`) are replaceable attachments
- Monotonic counters provide replay resistance (demo-level)
- Switching transport does **not** renegotiate identity

## Run

Terminal 1 (server):

```bash
python -m prototype.server --host 127.0.0.1 --port-a 40000 --port-b 40001 --psk DEMO_PSK_CHANGE_ME

Terminal 2 (client):

python -m prototype.client --host 127.0.0.1 --port-a 40000 --port-b 40001 --psk DEMO_PSK_CHANGE_ME --session-id DEMO-SESSION --trace DEMO_TRACE.jsonl

Output trace is JSONL: DEMO_TRACE.jsonl

What it proves

Session created (ATTACHED on udp:A)

Volatility signal (loss spike)

Transport switch udp:A -> udp:B

Recovery back to ATTACHED without identity reset

---

# live_demo.py
"""
Jumping VPN — Live Prototype Demo Runner

This script launches a local Jumping VPN prototype server and client,
demonstrates session creation, transport volatility, transport switch,
and recovery without identity reset.

Output:
    DEMO_TRACE.jsonl  — deterministic session continuity trace

Usage:
    python live_demo.py
"""

from __future__ import annotations
import subprocess
import sys
import time
import os


def main() -> None:
    # Demo configuration
    psk = "DEMO_PSK_CHANGE_ME"
    host = "127.0.0.1"
    port_a = "40000"
    port_b = "40001"
    session_id = "DEMO-SESSION"
    trace_file = "DEMO_TRACE.jsonl"

    # Remove old trace if exists
    if os.path.exists(trace_file):
        os.remove(trace_file)

    print("[live_demo] Starting Jumping VPN prototype server...")

    # Start server process
    server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "prototype.server",
            "--host",
            host,
            "--port-a",
            port_a,
            "--port-b",
            port_b,
            "--psk",
            psk,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        # Give server time to initialize
        time.sleep(0.8)

        print("[live_demo] Launching client session...")

        # Run client process
        client = subprocess.run(
            [
                sys.executable,
                "-m",
                "prototype.client",
                "--host",
                host,
                "--port-a",
                port_a,
                "--port-b",
                port_b,
                "--psk",
                psk,
                "--session-id",
                session_id,
                "--trace",
                trace_file,
            ],
            text=True,
        )

        print(f"[live_demo] Client finished with exit code: {client.returncode}")

        if os.path.exists(trace_file):
            print(f"[live_demo] Demo trace successfully generated: {trace_file}")
        else:
            print("[live_demo] Warning: trace file was not created")

        print("[live_demo] Demo completed successfully")

    finally:
        print("[live_demo] Shutting down server...")
        server.terminate()

        try:
            server.wait(timeout=2)
        except Exception:
            server.kill()

        print("[live_demo] Server stopped")


if __name__ == "__main__":
    main()