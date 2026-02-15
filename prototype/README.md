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

## 7) `live_demo.py` (в корне репо)

Это one-command runner, который запускает сервер в фоне (через subprocess) и потом клиента.

```python
# live_demo.py
from __future__ import annotations
import subprocess
import sys
import time
import os

def main() -> None:
    psk = "DEMO_PSK_CHANGE_ME"
    host = "127.0.0.1"
    port_a = "40000"
    port_b = "40001"
    session_id = "DEMO-SESSION"
    trace = "DEMO_TRACE.jsonl"

    # Clean trace
    if os.path.exists(trace):
        os.remove(trace)

    print("[live_demo] starting server...")
    server = subprocess.Popen(
        [sys.executable, "-m", "prototype.server",
         "--host", host, "--port-a", port_a, "--port-b", port_b, "--psk", psk],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        time.sleep(0.6)

        print("[live_demo] running client...")
        client = subprocess.run(
            [sys.executable, "-m", "prototype.client",
             "--host", host, "--port-a", port_a, "--port-b", port_b,
             "--psk", psk, "--session-id", session_id, "--trace", trace],
            text=True,
        )

        print("[live_demo] client exit code:", client.returncode)
        print("[live_demo] trace generated:", trace)
        print("[live_demo] done.")

    finally:
        print("[live_demo] stopping server...")
        server.terminate()
        try:
            server.wait(timeout=2)
        except Exception:
            server.kill()

if __name__ == "__main__":
    main()



