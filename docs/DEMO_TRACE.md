# Jumping VPN — Demo Trace (Example / Expected Output)

This document provides an **example trace format** for Demo v1.

It is an **expected output contract** that shows what a real run must produce:
explicit state transitions, transport switching, and identity continuity.

> Note: This is an example trace for reviewers.  
> Real traces will be published once the runnable demo is packaged for reproduction.

---

## Scenario

- Start stable (ATTACHED)
- Inject packet loss spike (VOLATILE)
- Flow-control reacts (cwnd/pacing)
- Multipath scoring changes
- Switch transport (explicit)
- Recover back to ATTACHED

---

## Trace (JSONL)

```json
{"ts_ms":1700000000000,"event":"SESSION_CREATED","session_id":"s_9f2c","state":"ATTACHED","state_version":0}
{"ts_ms":1700000000200,"event":"PATH_SELECTED","session_id":"s_9f2c","active_path":"udp:A","metrics":{"rtt_ms":24,"jitter_ms":3,"loss_pct":0.0},"flow":{"cwnd_packets":64,"pacing_pps":1200}}
{"ts_ms":1700000000500,"event":"TELEMETRY_TICK","session_id":"s_9f2c","metrics":{"rtt_ms":25,"jitter_ms":4,"loss_pct":0.0},"flow":{"cwnd_packets":72,"pacing_pps":1350}}

{"ts_ms":1700000000800,"event":"VOLATILITY_SIGNAL","session_id":"s_9f2c","reason":"LOSS_SPIKE","metrics":{"loss_pct":7.5,"rtt_ms":41,"jitter_ms":18}}
{"ts_ms":1700000000810,"event":"STATE_CHANGE","session_id":"s_9f2c","from":"ATTACHED","to":"VOLATILE","reason":"LOSS_SPIKE","state_version":1}

{"ts_ms":1700000000900,"event":"FLOW_CONTROL_UPDATE","session_id":"s_9f2c","reason":"LOSS_REACTION","flow":{"cwnd_packets":{"from":72,"to":36},"pacing_pps":{"from":1350,"to":820}}}

{"ts_ms":1700000001000,"event":"MULTIPATH_SCORE_UPDATE","session_id":"s_9f2c","candidates":[
  {"path":"udp:A","metrics":{"rtt_ms":44,"jitter_ms":20,"loss_pct":7.5},"rank":2},
  {"path":"udp:B","metrics":{"rtt_ms":31,"jitter_ms":8,"loss_pct":1.2},"rank":1}
]}

{"ts_ms":1700000001100,"event":"TRANSPORT_SWITCH","session_id":"s_9f2c","reason":"PREFERRED_PATH_CHANGED","details":{"from_path":"udp:A","to_path":"udp:B"}}
{"ts_ms":1700000001110,"event":"AUDIT_EVENT","session_id":"s_9f2c","details":{"check":"NO_DUAL_ACTIVE_BINDING","result":"PASS"}}
{"ts_ms":1700000001120,"event":"AUDIT_EVENT","session_id":"s_9f2c","details":{"check":"NO_IDENTITY_RESET","result":"PASS"}}

{"ts_ms":1700000001800,"event":"RECOVERY_SIGNAL","session_id":"s_9f2c","metrics":{"loss_pct":0.4,"rtt_ms":26,"jitter_ms":4}}
{"ts_ms":1700000001810,"event":"STATE_CHANGE","session_id":"s_9f2c","from":"VOLATILE","to":"RECOVERING","reason":"STABILITY_WINDOW","state_version":2}
{"ts_ms":1700000002100,"event":"STATE_CHANGE","session_id":"s_9f2c","from":"RECOVERING","to":"ATTACHED","reason":"RECOVERY_COMPLETE","state_version":3}

What a reviewer should verify

PASS criteria:

session_id stays constant across the entire trace

state_version is monotonic

transport switching is explicit and reason-coded

no TERMINATED occurs in this scenario

audit events prove invariants (no dual-active, no identity reset)

Session is the anchor. Transport is volatile.

---

## 2) `docs/INVARIANTS.md` (создай новый файл)
```md
# Jumping VPN — Architectural Invariants

This document defines the **non-negotiable safety properties** of the protocol.
If any invariant cannot be preserved, the protocol must fail closed
(reject reattach or terminate deterministically).

---

## Identity & Session Invariants

### INV-1: Session is the identity anchor
- SessionID is stable for the lifetime of a session.
- Transport changes must not change SessionID.

### INV-2: No silent identity reset
- The protocol must never silently create a new session to recover.
- If recovery is impossible, termination must be explicit and reason-coded.

### INV-3: Session state transitions are explicit
- All state changes must be emitted as explicit events.
- No implicit transitions.

---

## Transport Binding Invariants

### INV-4: Single active binding
- A session must have **at most one ACTIVE transport** at any time.

### INV-5: Dual-active binding is forbidden
- Two transports must never be simultaneously accepted as ACTIVE for the same session.
- If ownership is ambiguous → reject (fail closed).

### INV-6: Transport death ≠ session death (within bounds)
- Loss of a transport transitions the session into RECOVERING/VOLATILE.
- Session can remain alive within policy TTL bounds.

---

## Determinism & Policy Invariants

### INV-7: Bounded recovery
- Recovery must complete within a policy-defined window.
- If bounds are exceeded → DEGRADED or TERMINATED explicitly.

### INV-8: Rate-limited switching (anti-flap)
- Transport switching must be bounded by policy (cooldown + max switches per time window).
- Oscillation must be prevented deterministically.

### INV-9: Monotonic state version
- Each accepted state mutation increments `state_version`.
- Stale updates must be rejected. Rollback is forbidden.

---

## Security Invariants (Control-Plane)

### INV-10: Reattach requires proof-of-possession
- A reattach request must prove knowledge of session-bound secret context.

### INV-11: Anti-replay freshness
- Reattach must include freshness (nonce/timestamp window).
- Replays must be rejected deterministically and logged.

### INV-12: Ambiguity fails closed
- If the server cannot prove correct ownership/binding, it must not accept reattach.

---

## Observability Invariants

### INV-13: All critical decisions are auditable
- transport switches
- termination
- degraded entry
- replay rejects
- policy limit triggers

Logging must be non-blocking: failure to export logs must not affect correctness.

---

Session is the anchor. Transport is volatile.

