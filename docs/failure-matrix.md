# Failure Matrix — Deterministic Outcomes (Preview)

This document defines the deterministic failure handling model
for Jumping VPN.

For every relevant failure category, the system must produce:

- An explicit state transition
- A reason-coded outcome
- A bounded behavioral result
- No silent ambiguity

This matrix is intended for reviewers and auditors.

---

# 1) Transport-Level Failures

| Event | Current State | Condition | Resulting State | Deterministic Outcome | Silent Allowed? |
|--------|---------------|-----------|-----------------|----------------------|-----------------|
| Packet loss spike | ATTACHED | Below volatility threshold | ATTACHED | No state change | Yes |
| Packet loss spike | ATTACHED | Above threshold | VOLATILE | Emit VOLATILITY_SIGNAL | No |
| Sustained instability | VOLATILE | Within recovery window | RECOVERING | Attempt reattach | No |
| Sustained instability | RECOVERING | Reattach succeeds | ATTACHED | Emit TransportSwitch | No |
| Sustained instability | RECOVERING | Reattach fails | DEGRADED | Explicit failure | No |
| No viable transport | RECOVERING | TTL exceeded | TERMINATED | Reason-coded termination | No |

Transport death must never implicitly reset identity.

---

# 2) Control-Plane Failures

| Event | Condition | Outcome | State Impact | Notes |
|--------|-----------|----------|--------------|-------|
| state_version mismatch | Client version stale | REJECT | No mutation | Protects against rollback |
| Replay nonce detected | Nonce reused | REJECT + SECURITY_EVENT | No mutation | Anti-replay enforcement |
| Invalid proof-of-possession | Signature invalid | REJECT | No mutation | Identity protection |
| Unknown session_id | Session not found | REJECT | No mutation | Fail closed |
| TTL expired | Session expired | TERMINATED | Final state | No revival allowed |

Rejection must not mutate session state.

---

# 3) Ownership & Consistency Failures

| Event | Condition | Outcome | Deterministic Rule |
|--------|-----------|----------|--------------------|
| Dual-active binding attempt | Active transport exists | REJECT | Only one active transport allowed |
| Split-brain ambiguity | Ownership uncertain | REJECT or TERMINATE | Consistency > availability |
| CAS failure | Version conflict | REJECT | Retry required with updated version |
| Concurrent reattach race | Two requests | One succeeds, one rejects | Monotonic versioning resolves |

Ambiguity must never result in dual identity.

---

# 4) Policy-Bound Failures

| Event | Condition | Result | State |
|--------|-----------|--------|-------|
| Switch rate exceeded | > MaxSwitchesPerMinute | DEGRADED or TERMINATED | Policy-driven |
| Recovery window exceeded | > MaxRecoveryWindowMs | TERMINATED | Bounded recovery |
| Transport-loss TTL exceeded | No viable transport | TERMINATED | Explicit end |
| Session TTL exceeded | Time expired | TERMINATED | Final |

Policy bounds define the outer safety envelope.

---

# 5) Resource & Abuse Failures

| Event | Condition | Result | Notes |
|--------|-----------|--------|------|
| Reattach flood | Rate limit exceeded | Reject + throttle | No state mutation |
| Excessive volatility | Continuous oscillation | DEGRADED | Anti-flap safeguard |
| Replay flood | Repeated nonce attempts | Reject | Security event logged |
| Log export failure | Observability offline | Continue session | Logging is non-blocking |

Correctness must not depend on observability success.

---

# 6) Security Failures

| Event | Impact | Deterministic Response |
|--------|--------|------------------------|
| Identity hijack attempt | Proof invalid | Reject |
| Transport spoofing | Validation fails | Reject |
| Ownership mismatch | Ambiguous | Reject |
| Integrity violation | Detected | TERMINATE |

The system must fail closed on integrity violation.

---

# 7) Explicit Prohibitions

The system must NEVER:

- Silently reset identity
- Allow dual-active binding
- Accept stale state_version
- Accept reused nonce
- Continue session past TTL
- Downgrade state without explicit transition

---

# 8) Deterministic Outcome Principles

1. Every failure produces a reason-coded outcome.
2. Every state mutation increments state_version.
3. All ambiguity fails closed.
4. Termination is explicit, never implicit.
5. Recovery is bounded and measurable.

---

# 9) Behavioral Guarantees Summary

Under any failure:

- Identity remains bound to SessionID.
- Recovery attempts are bounded by policy.
- State transitions are explicit.
- No silent renegotiation occurs.
- No dual identity state can exist.

---

# Final Principle

Failure must reduce ambiguity —
never introduce it.

If correctness cannot be guaranteed,
the session must terminate explicitly.

Session is the anchor.  
Transport is volatile.