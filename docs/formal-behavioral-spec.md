# Formal Behavioral Specification — Jumping VPN (Preview)

This document defines the behavioral model of Jumping VPN
in a formalized, constraint-oriented manner.

It describes:

- States
- Transitions
- Preconditions
- Postconditions
- Safety properties
- Liveness guarantees

This is not cryptographic specification.
This is behavioral determinism specification.

---

# 1. Session Model

Let:

S = Session
T = Transport
V = state_version
P = Policy

Each session is defined as:

S = {
  session_id,
  state,
  state_version,
  active_transport (nullable),
  ttl_expiry,
  policy_snapshot
}

---

# 2. State Set

States ∈ {
  BIRTH,
  ATTACHED,
  VOLATILE,
  RECOVERING,
  DEGRADED,
  TERMINATED
}

TERMINATED is absorbing.

---

# 3. Core Invariants

Invariant I1:
At most one active transport per session.

Invariant I2:
SessionID is immutable.

Invariant I3:
state_version is strictly monotonic.

Invariant I4:
Dual-active binding is forbidden.

Invariant I5:
All state transitions are explicit and reason-coded.

---

# 4. Transition Function

Let δ(S, event) → S'

Transitions are deterministic.

---

## 4.1 BIRTH → ATTACHED

Preconditions:
- Valid handshake
- SessionID assigned
- state_version == 0

Postconditions:
- active_transport ≠ null
- state = ATTACHED
- state_version++

---

## 4.2 ATTACHED → RECOVERING

Trigger:
TRANSPORT_DEAD

Preconditions:
- active_transport ≠ null
- transport health failure validated

Postconditions:
- active_transport = null
- state = RECOVERING
- state_version++

---

## 4.3 RECOVERING → ATTACHED

Trigger:
REATTACH_ACK

Preconditions:
- proof-of-possession valid
- nonce fresh
- TTL not expired
- no ownership ambiguity
- state_version matches expected

Postconditions:
- active_transport ≠ null
- state = ATTACHED
- state_version++

---

## 4.4 RECOVERING → DEGRADED

Trigger:
Recovery attempt rejected but TTL not expired

Preconditions:
- recovery bound exceeded
- switch rate threshold hit

Postconditions:
- state = DEGRADED
- active_transport = null
- state_version++

---

## 4.5 ANY → TERMINATED

Trigger:
- Session TTL expired
- Transport-loss TTL expired
- Ownership ambiguity
- Policy hard failure
- Explicit terminate

Postconditions:
- active_transport = null
- state = TERMINATED
- state_version++
- No further transitions allowed

---

# 5. Version Semantics

For every successful transition:

V_new = V_old + 1

Server MUST reject:

If V_request ≠ V_current

This prevents rollback and race corruption.

---

# 6. Safety Properties

Safety S1:
No two transports can be active simultaneously.

Safety S2:
Session identity cannot be reset silently.

Safety S3:
Replay of reattach cannot mutate session state.

Safety S4:
Ambiguous ownership results in rejection or termination.

Safety S5:
Transport mutation cannot bypass state machine.

---

# 7. Liveness Properties

Liveness L1:
If a valid transport candidate exists within recovery bounds,
session can return to ATTACHED.

Liveness L2:
If no candidate exists and TTL not expired,
session remains in RECOVERING or DEGRADED.

Liveness L3:
If recovery bound exceeded,
session eventually transitions to TERMINATED.

No infinite loops allowed.

---

# 8. Bounded Recovery Guarantee

Recovery is bounded by:

- TransportLossTtlMs
- MaxSwitchesPerMinute
- RecoveryWindowMs

No unbounded retry allowed.

Bounded recovery prevents flapping collapse.

---

# 9. Rejection Rules

Server MUST reject transition if:

- state_version mismatch
- proof invalid
- nonce replay
- TTL expired
- dual-active detected
- ownership conflict

Rejection must not mutate state.

---

# 10. Failure Determinism

If invariants cannot be preserved:

Transition → TERMINATED

Correctness > Continuity.

---

# 11. Proof Sketch (Informal)

Given:

- Monotonic version increments
- Single active transport rule
- Ownership validation
- Explicit transition table

It follows:

Identity duplication is impossible
if and only if invariants are preserved.

Thus:

Session continuity is safe within bounds.

---

# Final Principle

Transport behavior is volatile.

Session behavior is constrained.

Determinism is enforced
through explicit transitions and invariant preservation.

Session is the anchor.
Transport is volatile.