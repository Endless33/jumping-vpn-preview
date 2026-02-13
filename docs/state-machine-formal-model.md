# State Machine — Formal Behavioral Model (Preview)

Status: Formalization Draft  
Scope: Deterministic session lifecycle under transport volatility  

This document defines the formal behavioral model of the Jumping VPN session state machine.

It is written to enable:

- Implementation clarity
- Reviewer reasoning
- Formal verification (future work)
- Determinism analysis

This document does not define cryptography or packet formats.

---

# 1. State Set

Let S be the finite set of possible session states:

S = {
  BIRTH,
  ATTACHED,
  VOLATILE,
  RECOVERING,
  DEGRADED,
  TERMINATED
}

TERMINATED is an absorbing state.

---

# 2. Transition Function

Define deterministic transition function:

δ : (state, event, policy) → (new_state, reason_code)

All transitions must:

- Be explicit
- Increment state_version
- Emit audit event
- Be policy-bounded

No implicit transitions allowed.

---

# 3. Events

Let E be the set of possible events:

E = {
  HANDSHAKE_SUCCESS,
  TRANSPORT_HEALTH_DEGRADED,
  TRANSPORT_DEAD,
  REATTACH_SUCCESS,
  REATTACH_REJECT,
  POLICY_LIMIT_EXCEEDED,
  SESSION_TTL_EXPIRED,
  SECURITY_VIOLATION
}

---

# 4. Deterministic Transition Table

BIRTH:
  HANDSHAKE_SUCCESS → ATTACHED

ATTACHED:
  TRANSPORT_HEALTH_DEGRADED → VOLATILE
  TRANSPORT_DEAD → RECOVERING
  SESSION_TTL_EXPIRED → TERMINATED
  SECURITY_VIOLATION → TERMINATED

VOLATILE:
  TRANSPORT_DEAD → RECOVERING
  HEALTH_RECOVERED → ATTACHED
  POLICY_LIMIT_EXCEEDED → DEGRADED
  SESSION_TTL_EXPIRED → TERMINATED

RECOVERING:
  REATTACH_SUCCESS → ATTACHED
  REATTACH_REJECT → DEGRADED or TERMINATED (policy-defined)
  SESSION_TTL_EXPIRED → TERMINATED
  SECURITY_VIOLATION → TERMINATED

DEGRADED:
  STABILITY_WINDOW_DETECTED → RECOVERING
  POLICY_LIMIT_EXCEEDED → TERMINATED
  SESSION_TTL_EXPIRED → TERMINATED

TERMINATED:
  (no outgoing transitions)

---

# 5. Determinism Requirements

For any (state, event):

- Exactly one valid transition must exist
- If no valid transition exists → reject event
- If multiple transitions possible → violation

Ambiguity is forbidden.

---

# 6. Invariants

The state machine must preserve:

I1: Single Active Transport  
At most one transport may be ACTIVE at any time.

I2: Version Monotonicity  
state_version must strictly increase on every transition.

I3: No Implicit Reset  
Session identity may never reset without explicit TERMINATED → BIRTH cycle.

I4: Bounded Recovery  
Time spent in RECOVERING must not exceed TransportLossTTL.

I5: No Dual-Active Binding  
Concurrent active bindings are forbidden.

---

# 7. Absorbing State Property

TERMINATED is absorbing:

∀ e ∈ E:
δ(TERMINATED, e) = undefined

Any event received in TERMINATED must be rejected.

---

# 8. Policy-Bounded Transitions

Policy P defines constraints:

- MaxSwitchesPerMinute
- MaxRecoveryWindowMs
- SessionTTL
- QualityFloor
- ReplayWindowSize

If policy violation occurs:

δ(state, POLICY_LIMIT_EXCEEDED, P) → DEGRADED or TERMINATED

Policy may not override invariants.

---

# 9. Version Semantics

Let V be state_version.

Rules:

- On successful transition:
  V_new = V_old + 1

- On rejected transition:
  V remains unchanged

- Stale version events must be rejected

Version rollback is forbidden.

---

# 10. Failure Handling Philosophy

If correctness cannot be guaranteed:

The state machine must prefer TERMINATED
over ambiguous continuation.

Correctness > availability.

---

# 11. Formal Verification Targets (Future Work)

The following properties should be formally proven:

- No dual-active state reachable
- No cycle without version increment
- TERMINATED unreachable without explicit event
- Recovery bounded by policy
- All transitions deterministic

Suggested modeling tools:

- TLA+
- Alloy
- PlusCal

---

# 12. Behavioral Contract Summary

The state machine guarantees:

- Explicit transitions
- Deterministic recovery
- Bounded volatility handling
- Absorbing termination
- Version-safe mutation

Transport may fail.

The session must not become ambiguous.

---

# Final Principle

A protocol is not defined by features.

It is defined by how it behaves over time.

Session is the anchor.  
Transport is volatile.