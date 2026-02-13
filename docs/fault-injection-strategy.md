# Fault Injection Strategy — Jumping VPN

Status: Architectural Validation  
Scope: Controlled failure modeling  

This document defines how transport volatility and failure conditions
are intentionally injected and tested to validate deterministic behavior.

Correctness must be proven under stress — not assumed.

---

# 1. Purpose

Fault injection exists to validate:

- Deterministic state transitions
- Bounded recovery
- Anti-flap enforcement
- Replay resistance
- Version safety
- Explicit termination behavior

If the system only works under ideal conditions,
it is incomplete.

---

# 2. Categories of Injected Failures

## 2.1 Transport-Level Failures

- Hard socket close
- Silent packet drop
- 100% packet loss spike
- Latency spike (> policy threshold)
- Jitter instability
- NAT mapping expiration
- Remote IP change
- Port change

Expected behavior:

ATTACHED → RECOVERING  
RECOVERING → ATTACHED (bounded)  
or → DEGRADED / TERMINATED  

No silent identity reset.

---

## 2.2 Control-Plane Failures

- Reattach replay attempt
- Stale state_version
- Invalid proof-of-possession
- Duplicate nonce
- Concurrent reattach race
- Ownership ambiguity

Expected behavior:

- Deterministic rejection
- No state mutation
- Security event emitted
- No dual-active binding

---

## 2.3 Policy Boundary Violations

- Switch rate exceeded
- Recovery window exceeded
- Session TTL exceeded
- Transport-loss TTL exceeded

Expected behavior:

Explicit:

→ DEGRADED  
or → TERMINATED  

Never indefinite RECOVERING.

---

# 3. Volatility Stress Tests

### 3.1 Rapid Flap Simulation

Inject alternating:

alive → dead → alive → dead

Goal:

Verify dampening:
- max switches per minute enforced
- cooldown respected
- bounded retries

Outcome must not oscillate infinitely.

---

### 3.2 High Churn Environment

Simulate:

10k+ sessions
Randomized packet loss
Random NAT churn

Measure:

- recovery latency distribution
- switch rate
- rejection correctness
- no memory leak
- no version regression

---

# 4. Replay Attack Simulation

Inject:

- Reattach with reused nonce
- Reattach with old state_version
- Reattach with valid proof but stale version

Expected:

RejectError
No state change
Security event logged

Replay must not mutate session.

---

# 5. Cluster Race Simulation

Simulate:

Two nodes receive REATTACH_REQUEST simultaneously.

Goal:

Ensure:

- Only one CAS succeeds
- Second attempt rejected
- No dual-active state
- Deterministic resolution

Consistency > availability.

---

# 6. Degradation Mode Testing

Inject:

Partial packet loss (e.g., 40%)
Latency > quality floor
Intermittent delivery

Expected:

ATTACHED → VOLATILE → DEGRADED

Session remains alive.
No silent corruption assumption.

---

# 7. Termination Correctness Tests

Inject:

Transport-loss TTL expiry
Session TTL expiry
Policy hard stop

Expected:

ANY → TERMINATED
Version increment
Termination reason logged
No further state mutation allowed

---

# 8. Observability Verification

For every injected failure:

Verify:

- STATE_CHANGE emitted
- reason_code present
- state_version incremented
- no hidden transition

If mutation occurs without audit:
Failure.

---

# 9. Failure Injection Interface (Future)

Planned injection hooks:

- transport.kill()
- transport.delay(ms)
- transport.drop(percent)
- control.inject_replay()
- cluster.inject_race()

Testing must not depend on external network unpredictability alone.

---

# 10. Determinism Criteria

Given identical injected sequence:

The state machine must produce identical:

- state transitions
- version increments
- rejection outcomes
- termination decisions

Non-deterministic behavior is unacceptable.

---

# 11. Evidence Collection

Each test run must produce:

- timestamped event stream
- state_version progression
- recovery duration
- decision reasons
- pass/fail assertion

Evidence stored in:

docs/evidence-log.md

---

# 12. Engineering Principle

A resilient protocol is defined by its failure behavior —
not its success path.

Volatility must be provoked,
not merely tolerated.

---

# Final Principle

If a fault can produce ambiguity,
the session must fail closed.

Determinism over optimism.

Session is the anchor.  
Transport is volatile.  
Failures must be measurable.