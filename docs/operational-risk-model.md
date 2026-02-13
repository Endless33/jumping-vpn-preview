# Operational Risk Model — Jumping VPN

This document maps real-world operational risks
to deterministic behavioral responses in Jumping VPN.

The purpose is not theoretical security modeling —
but operational survivability under transport volatility.

---

# 1. Risk Categories

Operational risks are grouped into five classes:

1) Transport Instability
2) Control-Plane Abuse
3) Cluster Consistency Failures
4) Resource Exhaustion
5) Observability Failures

Each risk must have:

- Explicit detection criteria
- Deterministic state reaction
- Bounded impact window
- Defined termination condition

---

# 2. Transport Instability Risks

## 2.1 Packet Loss Spikes

Risk:
Burst loss causes transport to appear dead.

Detection:
Consecutive loss threshold exceeded within observation window.

Response:
ATTACHED → RECOVERING

Bound:
Recovery limited by MaxRecoveryWindowMs.

Escalation:
If candidate exists → REATTACH
If no candidate → TERMINATED

---

## 2.2 NAT Churn / IP Change

Risk:
Return path changes unexpectedly.

Detection:
Inbound traffic mismatch OR delivery timeout.

Response:
RECOVERING → REATTACH_REQUEST

Invariant:
SessionID unchanged.

---

## 2.3 Asymmetric Routing

Risk:
Return path differs from outbound.

Response:
Accept new binding only if proof + freshness valid.

Ambiguity:
Reject reattach.

---

# 3. Control-Plane Abuse

## 3.1 Reattach Flood

Risk:
Attacker spams REATTACH_REQUEST.

Mitigation:
- Rate limiter
- Early session existence check
- Replay window enforcement

Behavior:
Reject without mutating state.

Never:
Trigger uncontrolled switching.

---

## 3.2 Nonce Replay

Risk:
Old proof reused.

Detection:
Nonce already seen OR outside window.

Response:
Reject.
Emit SECURITY_EVENT.
No state change.

---

## 3.3 Version Rollback Attempt

Risk:
Client sends stale state_version.

Response:
Reject.
No state mutation.

Invariant:
Monotonic state progression.

---

# 4. Cluster Risks

## 4.1 Split-Brain

Risk:
Two nodes attempt to bind same session.

Mitigation:
- Sticky routing
OR
- Atomic CAS in shared store

If ownership ambiguous:
Reject or TERMINATE.

Consistency preferred over availability.

---

## 4.2 Partial Cluster Failure

Risk:
Some nodes unreachable.

Behavior:
Session remains valid only if authoritative owner reachable.

Otherwise:
REJECT reattach.

---

# 5. Resource Exhaustion

## 5.1 Replay Window Memory Growth

Constraint:
Replay structure must be bounded.

Eviction:
Sliding window or ring buffer.

Invariant:
Memory O(1) per session.

---

## 5.2 Candidate Explosion

Constraint:
Candidate transport set bounded by policy.

Never:
Unbounded exploration.

---

## 5.3 Session Table Overload

Risk:
High churn creates pressure.

Mitigation:
TTL enforcement + eviction policy.

Behavior:
Exceeding limits → TERMINATED (explicit).

---

# 6. Observability Failures

## 6.1 Logging Backend Down

Risk:
SIEM unreachable.

Rule:
Telemetry must be non-blocking.

State transitions MUST proceed regardless.

---

## 6.2 Partial Audit Delivery

Impact:
Reduced visibility.

But:
Correctness unaffected.

Observability failure must not mutate state.

---

# 7. Catastrophic Transport Collapse

Scenario:
All transports fail simultaneously.

Behavior:
ATTACHED → RECOVERING

If no viable candidate within recovery window:
RECOVERING → TERMINATED

Never:
Infinite recovery loop.

---

# 8. Safety Priority Model

If at any time:

- ownership ambiguous
- proof invalid
- version inconsistent
- TTL expired
- replay violation detected

The session MUST fail closed.

TERMINATED > Undefined Behavior.

---

# 9. Explicit Escalation Ladder

RECOVERING  
→ DEGRADED (if partial viability exists)  
→ TERMINATED (if invariants violated or bounds exceeded)

No hidden fallback.

---

# 10. Risk Philosophy

The goal is not to prevent transport instability.

It is to ensure instability:

- does not corrupt identity
- does not create ambiguity
- does not cause silent downgrade
- does not violate invariants

Failure is acceptable.
Ambiguity is not.

---

Session is the anchor.
Transport is volatile.
Correctness dominates survivability.