# Jumping VPN — Test Scenarios

This document describes conceptual and planned test scenarios
used to validate Jumping VPN’s behavior under transport volatility.

The goal is not throughput optimization,
but deterministic session behavior under stress.

---

## Scenario 1 — Transport Death (Hard Failure)

Description:
Primary transport becomes unavailable during active session.

Conditions:
- Active transport drops to zero availability
- No graceful teardown

Expected Behavior:
- Session transitions to VOLATILE
- Explicit transport switch is attempted
- Session identity preserved
- No renegotiation
- State logged and auditable

Failure Condition:
- Session silently resets
- Unbounded retry loop

---

## Scenario 2 — Packet Loss Spike (Soft Failure)

Description:
Sudden packet loss spike during active session.

Conditions:
- Packet loss increases to 5–15%
- Latency jitter present

Expected Behavior:
- Session transitions to VOLATILE
- Transport scoring degrades
- No immediate session termination
- Controlled switch only if policy threshold exceeded

Failure Condition:
- Immediate session drop
- Uncontrolled oscillation

---

## Scenario 3 — NAT Rebinding

Description:
Client IP and port mapping changes mid-session.

Conditions:
- NAT mapping expires
- New source address observed

Expected Behavior:
- Reattachment validation required
- Session-bound identity verification
- Session continuity preserved

Failure Condition:
- Session fixation
- Identity confusion

---

## Scenario 4 — Transport Flapping

Description:
Multiple transports alternate between usable and unstable.

Conditions:
- Rapid availability changes
- Competing paths

Expected Behavior:
- Switch rate limited
- Dampening applied
- Stable path preferred
- Session remains attached or degraded

Failure Condition:
- Continuous oscillation
- Resource exhaustion

---

## Scenario 5 — Recovery After Degradation

Description:
Previously unstable environment stabilizes.

Conditions:
- Packet loss and latency return to baseline

Expected Behavior:
- Session transitions to RECOVERING
- Stable transport re-evaluated
- Controlled return to ATTACHED

Failure Condition:
- Permanent degraded state
- Stale transport binding

---

## Scenario 6 — Replay Attempt During Reattachment

Description:
Attacker replays old reattachment data.

Conditions:
- Replayed session identifiers
- Invalid temporal context

Expected Behavior:
- Reattachment rejected
- Session remains unchanged
- Security event logged

Failure Condition:
- Session hijack
- State corruption

---

## Scenario 7 — Session Lifetime Expiry

Description:
Session exceeds maximum lifetime.

Conditions:
- Session duration exceeds policy limit

Expected Behavior:
- Session transitions to TERMINATED
- Full handshake required for new session

Failure Condition:
- Silent continuation beyond bounds

---

## Testing Philosophy

Jumping VPN tests focus on:

- Behavior over throughput
- State integrity over convenience
- Predictable failure over silent recovery

A test passes only if behavior is:
- Deterministic
- Auditable
- Bounded by policy

---

## Real Transport Prototype (UDP) — Validation Link

A minimal real UDP prototype exists to validate session reattachment behavior over an actual transport:

- `poc/real_udp_prototype.py`
- Instructions: `poc/README_udp.md`

### Validates these scenarios

- **Scenario 1 — Transport Death (Hard Failure)**
  - Client transport dies (socket closed)
  - Client reattaches using the same session ID
  - Server emits explicit `TransportSwitch`
  - Session continues without session reset

- **Scenario 3 — NAT Rebinding (Transport Binding Change)**
  - New UDP socket uses a new ephemeral port (new binding)
  - Reattachment updates server-side transport binding explicitly

### Proof Points

On server output, verify:
- `SessionCreated`
- `TransportSwitch` (explicit + auditable)
- Continued `DataAccepted` after reattach

This prototype is behavioral validation only (not production security).