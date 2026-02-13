# Formal Constraints — Jumping VPN Behavioral Core

This document defines formal constraints governing session behavior.

These constraints are implementation-agnostic and must hold
regardless of language, deployment model, or transport type.

If a constraint cannot be enforced,
the protocol must terminate the session.

---

# 1. Identity Constraints

C1 — Session Identity Stability  
A SessionID MUST remain constant for the lifetime of a session.

C2 — No Implicit Identity Reset  
Identity renegotiation MUST NOT occur without explicit TERMINATED → BIRTH cycle.

C3 — Single Anchor Principle  
At any time, a session MUST have exactly one logical identity anchor.

---

# 2. Transport Binding Constraints

C4 — Single Active Transport  
At most one ACTIVE transport binding per session.

C5 — No Dual-Active Condition  
Concurrent valid bindings MUST NOT exist.

If detected → TERMINATED.

C6 — Binding Requires Validation  
New transport binding MUST validate:

- proof-of-possession
- freshness (anti-replay)
- ownership authority
- TTL validity

---

# 3. Versioning Constraints

C7 — Monotonic State Version  
state_version MUST increase strictly on each transition.

C8 — No Rollback  
Transitions with stale state_version MUST be rejected.

C9 — CAS Requirement (Cluster Mode)  
Ownership update MUST be atomic.

Ambiguous ownership → reject or terminate.

---

# 4. Recovery Constraints

C10 — Bounded Recovery Window  
RECOVERING state duration MUST NOT exceed MaxRecoveryWindowMs.

C11 — Bounded Switch Rate  
Transport switches MUST NOT exceed MaxSwitchesPerMinute.

C12 — Deterministic Escalation  
If recovery bounds exceeded → DEGRADED or TERMINATED.

No silent looping.

---

# 5. Failure Handling Constraints

C13 — Explicit Failure Signaling  
All transport death events MUST trigger explicit state transition.

C14 — No Silent Continuation  
If transport unusable and no candidate exists → TERMINATED.

C15 — TTL Enforcement  
Session TTL expiration MUST result in TERMINATED.

No exception.

---

# 6. Replay & Security Constraints

C16 — Replay Window Bounded  
Replay tracking MUST use bounded memory.

C17 — Freshness Before Binding  
Freshness validation MUST occur before transport binding.

C18 — Fail Closed  
On ambiguity or validation failure, session MUST NOT continue.

---

# 7. Observability Constraints

C19 — All Critical Transitions Auditable  
STATE_CHANGE events MUST include:

- from_state
- to_state
- reason_code
- state_version

C20 — Telemetry Must Not Affect Correctness  
Logging failure MUST NOT block state transition logic.

---

# 8. Resource Constraints

C21 — Per-Session Memory Bound  
Session memory MUST scale O(1) with bounded structures.

C22 — Replay Structure Bound  
Replay protection MUST use fixed window size.

C23 — Candidate Transport Bound  
Candidate set MUST be limited by policy.

---

# 9. Determinism Constraint

C24 — Deterministic Transition Rule  
Given:

(current_state, event, policy_snapshot)

Next state MUST be uniquely determined.

No randomness in state mutation.

---

# 10. Safety Over Liveness

C25 — Safety Priority  
If safety invariants conflict with availability,
the session MUST terminate.

Ambiguity is worse than interruption.

---

# 11. Forbidden Behaviors

The system MUST NEVER:

- allow dual-active transport binding
- silently downgrade state
- accept stale version updates
- continue without proof validation
- recover indefinitely without bounds

---

# Final Constraint

If any invariant cannot be enforced,
the only valid deterministic action is:

TERMINATED.

---

Session is the anchor.
Transport is volatile.
Determinism is mandatory.