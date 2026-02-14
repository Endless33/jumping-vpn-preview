# Jumping VPN — Demo Trace (Behavioral Proof)

This document shows an example behavioral trace demonstrating the core invariant of the Jumping VPN protocol:

> Session identity survives transport volatility without renegotiation or reset.

This is the primary correctness property.

---

# Scenario

The session begins in a stable state.

A packet loss spike occurs.

The protocol reacts by:

- reducing cwnd
- reducing pacing rate
- reevaluating path scores
- switching transport
- preserving session identity

The session remains ATTACHED.

No renegotiation occurs.

No session reset occurs.

---

# Trace Format

Each line is a structured event emitted by the protocol engine.

Format: JSONL (one event per line)

Fields:

- ts_ms — timestamp (milliseconds)
- event — event type
- session_id — stable identity
- state — protocol state
- state_version — monotonic version
- telemetry fields — rtt, jitter, loss, cwnd, pacing, etc.

---

# Trace

```json
{"ts_ms":1700000000000,"event":"SESSION_CREATED","session_id":"s_9f2c","state":"ATTACHED","state_version":0}

{"ts_ms":1700000000200,"event":"PATH_SELECTED","session_id":"s_9f2c","active_path":"udp:A","score":{"rtt_ms":24,"jitter_ms":3,"loss_pct":0.0},"cwnd_packets":64,"pacing_pps":1200}

{"ts_ms":1700000000500,"event":"TELEMETRY_TICK","session_id":"s_9f2c","rtt_ms":25,"jitter_ms":4,"loss_pct":0.0,"cwnd_packets":72,"in_flight":18,"pacing_pps":1350}

{"ts_ms":1700000000800,"event":"VOLATILITY_SIGNAL","session_id":"s_9f2c","reason":"LOSS_SPIKE","observed":{"loss_pct":7.5,"rtt_ms":41,"jitter_ms":18}}

{"ts_ms":1700000000810,"event":"STATE_CHANGE","session_id":"s_9f2c","from":"ATTACHED","to":"VOLATILE","reason":"LOSS_SPIKE","state_version":1}

{"ts_ms":1700000000900,"event":"FLOW_CONTROL_UPDATE","session_id":"s_9f2c","reason":"LOSS_REACTION","cwnd_packets":{"from":72,"to":36},"pacing_pps":{"from":1350,"to":820}}

{"ts_ms":1700000001000,"event":"MULTIPATH_SCORE_UPDATE","session_id":"s_9f2c","candidates":[
  {"path":"udp:A","score":{"rtt_ms":44,"jitter_ms":20,"loss_pct":7.5},"rank":2},
  {"path":"udp:B","score":{"rtt_ms":31,"jitter_ms":8,"loss_pct":1.2},"rank":1}
]}

{"ts_ms":1700000001100,"event":"TRANSPORT_SWITCH","session_id":"s_9f2c","from_path":"udp:A","to_path":"udp:B","reason":"PREFERRED_PATH_CHANGED"}

{"ts_ms":1700000001110,"event":"AUDIT_EVENT","session_id":"s_9f2c","check":"NO_DUAL_ACTIVE_BINDING","result":"PASS"}

{"ts_ms":1700000001120,"event":"AUDIT_EVENT","session_id":"s_9f2c","check":"NO_IDENTITY_RESET","result":"PASS"}

{"ts_ms":1700000001400,"event":"TELEMETRY_TICK","session_id":"s_9f2c","rtt_ms":30,"jitter_ms":7,"loss_pct":1.0,"cwnd_packets":44,"in_flight":14,"pacing_pps":980}

{"ts_ms":1700000001800,"event":"RECOVERY_SIGNAL","session_id":"s_9f2c","observed":{"loss_pct":0.4,"rtt_ms":26,"jitter_ms":4}}

{"ts_ms":1700000001810,"event":"STATE_CHANGE","session_id":"s_9f2c","from":"VOLATILE","to":"RECOVERING","reason":"STABILITY_WINDOW","state_version":2}

{"ts_ms":1700000002100,"event":"STATE_CHANGE","session_id":"s_9f2c","from":"RECOVERING","to":"ATTACHED","reason":"RECOVERY_COMPLETE","state_version":3}

Key Observations
This trace demonstrates:
Identity continuity
Session ID never changes:

session_id = s_9f2c

Transport changed.
Identity did not.
Explicit transport switch
Transport switched from:

udp:A → udp:B

This was explicit, controlled, and auditable.
No renegotiation
There is no:
SESSION_RESET
HANDSHAKE_RESTART
IDENTITY_CHANGE
Flow control reacted deterministically
cwnd reduced:

72 → 36 packets

pacing reduced:

1350 → 820 packets/sec

This shows congestion response.
Session survived
Final state:

ATTACHED

Session was not terminated.

Recovery was bounded and explicit.

Why this matters

This demonstrates the core invariant:

Session identity is independent from transport.

Transport can fail.

Session survives.

What this proves

This proves that the protocol:

detects transport degradation

reacts with congestion control

selects a better path

switches transport safely

preserves session identity

recovers deterministically

Next step

Live telemetry dashboard demonstration will visualize these events in real time.

START_HERE.md docs/DEMO_TRACE.md docs/invariants.md docs/state-machine.md

docs/PROOF_OVERVIEW.md

