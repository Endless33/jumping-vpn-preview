# What Would Make This Architecture Fail

Status: Architectural Honesty Document  
Purpose: Define explicit failure conditions  

This document defines the conditions under which
Jumping VPN would be considered architecturally invalid.

If any of the below are observed,
the design assumptions must be revisited.

---

# 1. Identity Safety Failure

The architecture fails if:

- A session silently resets identity during transport switch
- SessionID changes without explicit termination
- Reattach implicitly creates a new session

Identity continuity is a non-negotiable invariant.

---

# 2. Dual-Active Binding

The architecture fails if:

- Two transports are simultaneously ACTIVE for the same session
- Cluster split-brain produces identity ambiguity
- Ownership conflict allows concurrent continuation

Single-anchor identity must hold absolutely.

---

# 3. Unbounded Recovery

The architecture fails if:

- RECOVERING state can persist indefinitely
- Recovery attempts are unbounded
- Switch rate is not rate-limited
- Cooldown enforcement fails

Recovery must be bounded.

---

# 4. Version Rollback

The architecture fails if:

- state_version decreases
- Stale mutation is accepted
- Concurrent reattach produces version ambiguity

Version monotonicity is mandatory.

---

# 5. Replay Acceptance

The architecture fails if:

- Reused nonce is accepted
- Stale proof-of-possession is accepted
- Replay mutates state

Replay rejection must be deterministic and state-safe.

---

# 6. Silent Failure

The architecture fails if:

- Session silently resets instead of explicit transition
- Transition occurs without reason_code
- Observability misses a state mutation
- Policy violation produces no explicit state change

Ambiguity equals failure.

---

# 7. Resource Explosion

The architecture fails if:

- Replay window grows unbounded
- Candidate transport list grows unbounded
- Switch attempts grow unbounded
- Memory per session grows super-linearly

Scalability must remain predictable.

---

# 8. Non-Deterministic Behavior

The architecture fails if:

- Identical event sequences produce different outcomes
- Cluster race resolution is inconsistent
- Transition decisions depend on non-deterministic timing

Determinism is required for safety.

---

# 9. Cluster Ownership Ambiguity

The architecture fails if:

- No authoritative owner exists
- Ownership migration allows dual binding
- CAS semantics do not protect version integrity

Consistency > availability.

---

# 10. Observability Dependency

The architecture fails if:

- Logging pipeline failure breaks state machine
- Telemetry availability affects correctness
- Control-plane blocks on audit delivery

Observability must be non-blocking.

---

# 11. Policy Bypass

The architecture fails if:

- Switch limits can be bypassed
- Recovery window is ignored
- TTL expiration does not terminate
- Anti-flap rules can be disabled silently

Policy must be enforceable.

---

# 12. Volatility-Induced Identity Drift

The architecture fails if:

- Transport churn leads to identity mutation
- Rapid flapping causes unintended renegotiation
- Volatility degrades into silent reset

Volatility must not corrupt identity.

---

# 13. False Claim Scenario

The architecture fails if:

- It is marketed as anonymity system
- It is claimed to prevent censorship universally
- It is claimed to replace all VPN models
- It hides its own limitations

Scope must remain constrained.

---

# 14. Formal Review Failure

The architecture fails if:

- Invariants cannot be expressed formally
- Determinism cannot be tested
- Failure cases cannot be simulated
- Boundaries cannot be documented

Engineering must be auditable.

---

# 15. Honest Conclusion

If any invariant becomes unverifiable,
the system must not be promoted as resilient.

Correctness > perception.

---

# Final Principle

A resilient architecture must define
the conditions under which it is wrong.

Session is the anchor.  
Transport is volatile.  
If invariants fail — the system fails.