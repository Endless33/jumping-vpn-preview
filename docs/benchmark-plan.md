# Benchmark Plan — Jumping VPN (Preview)

This document defines the measurement strategy for evaluating
deterministic recovery under transport volatility.

This is not a performance claim.
This is a reproducible testing plan.

---

## 1. Objectives

Measure:

- Session continuity under transport death
- Recovery latency (ms)
- Switch rate stability (anti-flap)
- Identity persistence guarantees
- Behavior under packet loss spikes

---

## 2. Test Scenarios

### Scenario A — Single Transport Death

Conditions:
- Active UDP transport
- Abrupt socket termination

Expected:
- Explicit transport switch
- No session reset
- No identity renegotiation

Metrics:
- Time to reattach (ms)
- State transitions count
- Audit events emitted

---

### Scenario B — Packet Loss Spike

Conditions:
- 20–40% packet loss for 2–5 seconds

Expected:
- VOLATILE → RECOVERING → ATTACHED
- No uncontrolled termination

Metrics:
- Volatility detection delay
- Switch decision latency
- Recovery window duration

---

### Scenario C — Transport Flapping

Conditions:
- Rapid path degradation events

Expected:
- Rate-limited switching
- Dampening applied
- Possible DEGRADED state

Metrics:
- Switches per minute
- Policy enforcement behavior
- Final state outcome

---

## 3. Measurement Environment

Testing tools (planned):

- tc / netem (Linux)
- Controlled packet loss injection
- UDP socket-level interruption
- Synthetic multi-path simulation

---

## 4. Metrics Definition

| Metric | Definition |
|--------|------------|
| RecoveryLatencyMs | Time between transport death and reattach |
| SwitchRate | Switches per minute |
| SessionResetCount | Must remain zero under bounded volatility |
| DualBindingIncidents | Must remain zero |
| InvariantViolations | Must remain zero |

---

## 5. Non-Goals

This benchmark does NOT measure:

- Throughput optimization
- Encryption performance
- Global latency minimization
- Anonymity guarantees

Scope is strictly:

Deterministic recovery under transport instability.

---

## 6. Publication Policy

Performance data will only be published:

- With reproducible scripts
- With environment disclosure
- With network condition transparency

No synthetic marketing benchmarks.

---

Session continuity must be measurable —
or it is not a guarantee.