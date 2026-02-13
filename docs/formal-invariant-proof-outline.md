# Formal Invariant Proof Outline — Jumping VPN (Preview)

This document outlines how core behavioral invariants
can be reasoned about formally.

It is not a machine-verified proof.
It is a proof sketch defining safety arguments.

Scope:
- Session identity safety
- Single-active binding
- Version monotonicity
- Deterministic recovery bounds

---

# 1. Model Definition

We model a session as:

S = (state, state_version, active_transport, policy, ttl)

Where:

state ∈ {BIRTH, ATTACHED, VOLATILE, DEGRADED, RECOVERING, TERMINATED}

active_transport ∈ {None or TransportID}

state_version ∈ ℕ (monotonic)

---

# 2. Core Invariants

## Invariant I1 — Single Active Transport

At any time:

|active_transport| ≤ 1

Proof Sketch:

- All binding operations require CAS(state_version).
- Binding requires:
  - proof-of-possession
  - no existing active transport
  - version match
- Any concurrent binding attempt fails CAS.

Therefore, dual-active state cannot persist.

---

## Invariant I2 — Version Monotonicity

For all valid transitions:

new_state_version > previous_state_version

Proof Sketch:

- Every mutation increments state_version.
- Server rejects any request with stale version.
- Version rollback impossible without store corruption.
- Store corruption → fail-closed.

Thus version strictly increases.

---

## Invariant I3 — Identity Persistence Across Reattach

If:

state ∈ {RECOVERING}
and REATTACH_ACK succeeds

Then:

session_id remains unchanged.

Proof Sketch:

- Reattach requires proof bound to session_id.
- No new session_id is created.
- Session resurrection forbidden.
- Terminated sessions cannot reattach.

Therefore identity continuity preserved.

---

## Invariant I4 — Bounded Recovery

Recovery duration ≤ policy.MaxRecoveryWindow

Proof Sketch:

- Transport-loss TTL enforced.
- Recovery attempts rate-limited.
- If window exceeded → TERMINATED.

Infinite recovery loop impossible.

---

## Invariant I5 — No Silent Reset

There exists no transition:

ATTACHED → ATTACHED (new identity)

Proof Sketch:

- Identity creation only allowed in BIRTH.
- Reattach preserves session_id.
- TERMINATED forbids reuse.
- No implicit handshake allowed without explicit new session.

Thus silent reset impossible.

---

# 3. Failure Conditions

The model guarantees safety under:

- Transport death
- Replay attempts
- Concurrent reattach attempts
- Cluster partition (with authoritative ownership)
- Version race

The model does NOT guarantee:

- Liveness under full partition
- Survival under corrupted store
- Infinite availability

Safety > Liveness.

---

# 4. Ambiguity Handling Rule

If correctness cannot be proven:

Transition → TERMINATED.

This preserves invariants at cost of continuity.

---

# 5. Extensibility

Any future feature must preserve:

- Single active binding
- Monotonic version
- Deterministic transition graph
- Bounded recovery window

Otherwise the model is invalidated.

---

# 6. Verification Directions (Future Work)

Potential formalization tools:

- TLA+
- Alloy
- State machine model checking
- Property-based testing

Target properties:

- No dual-active state reachable
- No version rollback reachable
- No infinite recovery loop reachable

---

# Final Statement

Jumping VPN is defined by invariants,
not by feature count.

Safety properties are first-class.

If a transition cannot preserve invariants,
it must not exist.

Session is the anchor.
Transport is volatile.
Invariants are absolute.