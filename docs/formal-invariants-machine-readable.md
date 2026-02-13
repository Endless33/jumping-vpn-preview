# Formal Invariants — Machine-Readable Specification

Status: Architectural Validation  
Scope: Deterministic Session Behavior  

This document defines Jumping VPN invariants in a structured,
implementation-oriented form.

These invariants must hold in all production implementations.

Violation of any invariant is a correctness failure.

---

# 1. Identity Invariants

## INV-IDENTITY-001
A SessionID MUST NOT change during its lifetime.

## INV-IDENTITY-002
Transport reattach MUST NOT create a new session implicitly.

## INV-IDENTITY-003
Session termination MUST be explicit and reason-coded.

---

# 2. Transport Binding Invariants

## INV-TRANSPORT-001
At most one ACTIVE transport per session.

Constraint:
count(active_transports) ≤ 1

## INV-TRANSPORT-002
Transport switch MUST increment state_version.

## INV-TRANSPORT-003
Dual-active transport binding is forbidden.

If detected:
→ reject OR terminate deterministically.

---

# 3. Versioning Invariants

## INV-VERSION-001
state_version MUST increase monotonically.

## INV-VERSION-002
Incoming control-plane mutation with stale state_version MUST be rejected.

## INV-VERSION-003
Version rollback is forbidden.

Formally:
incoming_version < current_version → reject

---

# 4. Recovery Invariants

## INV-RECOVERY-001
RECOVERING state MUST be bounded by MaxRecoveryWindowMs.

## INV-RECOVERY-002
If recovery window exceeded:
→ TERMINATED or DEGRADED explicitly.

## INV-RECOVERY-003
Switch rate MUST NOT exceed MaxSwitchesPerMinute.

---

# 5. Replay Protection Invariants

## INV-REPLAY-001
Reattach nonce MUST be unique within replay window.

## INV-REPLAY-002
Reused nonce MUST be rejected.

## INV-REPLAY-003
Replay rejection MUST NOT mutate session state.

---

# 6. Policy Invariants

## INV-POLICY-001
All transitions MUST be policy-evaluated.

## INV-POLICY-002
Unbounded adaptation is forbidden.

## INV-POLICY-003
Policy violation MUST result in explicit state transition.

---

# 7. Determinism Invariants

## INV-DETERMINISM-001
Given identical event sequence,
state transitions MUST be identical.

## INV-DETERMINISM-002
State transitions MUST be reason-coded.

## INV-DETERMINISM-003
Ambiguity MUST resolve to reject OR terminate — never implicit continuation.

---

# 8. Termination Invariants

## INV-TERM-001
TERMINATED state is final.

## INV-TERM-002
No state mutation allowed after TERMINATED.

## INV-TERM-003
Termination MUST include reason_code.

---

# 9. Observability Invariants

## INV-AUDIT-001
All state transitions MUST emit audit event.

## INV-AUDIT-002
Observability failure MUST NOT affect state correctness.

---

# 10. Cluster Invariants

## INV-CLUSTER-001
Session ownership MUST be singular.

## INV-CLUSTER-002
Ownership conflict MUST NOT result in dual-active state.

## INV-CLUSTER-003
CAS semantics MUST protect version mutation.

---

# 11. Boundedness Invariants

## INV-BOUND-001
Replay window size MUST be bounded.

## INV-BOUND-002
Candidate transport set MUST be bounded.

## INV-BOUND-003
Recovery attempts MUST be bounded.

---

# 12. Failure Safety Invariants

## INV-SAFETY-001
Failure MUST NOT silently reset identity.

## INV-SAFETY-002
Failure MUST NOT bypass policy.

## INV-SAFETY-003
Failure MUST NOT introduce ambiguity.

---

# Implementation Compliance

An implementation is compliant only if:

- All invariants are enforced
- All invariants are testable
- Violations are detectable
- Deterministic rejection is guaranteed

---

# Final Statement

Correctness is defined by invariants —
not by successful packets.

Session is the anchor.  
Transport is volatile.  
Invariants are absolute.