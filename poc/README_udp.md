# Real UDP Prototype — Session Reattach Without Session Reset

This prototype demonstrates a **real UDP** client/server flow where:

- A session is created once (`session_id`)
- The client transport dies (socket closed, port changes)
- The client reattaches a **new transport** to the same session
- The server logs an explicit `TransportSwitch`
- The session continues without creating a new session

⚠️ This is a behavioral prototype.
It does NOT implement production cryptography.
It uses an HMAC as "proof of possession" for demonstration.

---

## Requirements

- Python 3.10+ recommended (3.8+ should work)
- Two terminals (or two devices)

---

## Run (Local)

### Terminal 1 — Start Server

From repository root:

```bash
python poc/real_udp_prototype.py server --bind 0.0.0.0:9999

You should see JSON logs such as:
ServerStart
SessionCreated
Terminal 2 — Start Client
From repository root:
Bash
Копировать код
python poc/real_udp_prototype.py client --server 127.0.0.1:9999
Expected sequence:
Client performs HANDSHAKE_INIT → receives session_id
Client sends a few DATA messages
Client closes the UDP socket (simulated transport death)
Client creates a new UDP socket (new local port)
Client sends REATTACH_REQUEST with session-bound proof
Server emits TransportSwitch
Client continues sending DATA under the same session
What to Look For (Proof)
On the server output
You should see:
SessionCreated
TransportSwitch
Example fields:
session_id
from_transport
to_transport
explicit: true
auditable: true
On the client output
You should see:
SessionEstablished
SimulateTransportDeath
ReattachResult (with REATTACH_ACK)
continued DataRoundtrip events after reattach
Notes
Transport change is simulated by closing and recreating the UDP socket. This usually changes the client’s source port, representing a new transport binding.
Session persistence on the server is bounded by a TTL: SESSION_TTL_SEC = 30
If the client waits longer than the TTL before reattaching, the server will drop the session and reject reattachment.
Security Reminder
This prototype is for behavioral validation only.
Production-grade security requires:
proper key exchange
robust anti-replay design
hardened session binding
security review
See: docs/threat-model.md and docs/security-review-plan.md.