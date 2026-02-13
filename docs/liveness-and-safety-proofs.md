# Liveness & Safety Proof Sketch — Jumping VPN (Preview)

This document provides an informal proof outline
for safety and liveness guarantees of the Jumping VPN
behavioral state machine.

It is not a formal machine-verified proof.
It is a structured reasoning model.

---

# 1. Definitions

Let:

S = session
T = transport
V = state_version
P = policy
δ = transition function

States:

{ BIRTH, ATTACHED, VOLATILE, RECOVERING, DEGRADED, TERMINATED }

TERMINATED is absorbing.

---

# 2. Safety Properties

Safety means:
"Nothing bad ever happens."

We define the following safety properties.

---

## S1 — Single Active Binding

At any time:

|active_transports(S)| ≤ 1

Proof Sketch:

- All binding occurs through explicit transition.
- Reattach requires version match.
- Server enforces CAS-style ownership validation.
- Dual-active attempts are rejected.
- State mutation increments version.

Therefore:
Two active bindings cannot coexist
without violating version or invariant checks.

---

## S2 — Identity Immutability

SessionID never changes.

Proof Sketch:

- SessionID assigned at BIRTH.
- No transition reassigns SessionID.
- No mutation path rewrites identity.
- Termination does not reassign identity.

Therefore:
Identity continuity is preserved.

---

## S3 — No Silent Reset

If transport dies:

ATTACHED → RECOVERING

Never:

ATTACHED → ATTACHED (implicit reset)

Proof Sketch:

- Transport death requires explicit transition.
- All transitions increment state_version.
- No transition bypasses state machine.

Therefore:
Silent identity reset is impossible.

---

## S4 — No Replay Mutation

Reattach requires:

- Fresh nonce
- Proof-of-possession
- Version match

Replay rejected before mutation.

Therefore:
Replay cannot mutate session state.

---

## S5 — No Dual Ownership in Cluster

Clustered deployments require:

- Sticky routing
or
- Atomic shared session store

Reattach must verify ownership.

Ambiguity → reject or terminate.

Thus:
Split-brain identity continuation prevented.

---

# 3. Liveness Properties

Liveness means:
"Something good eventually happens."

---

## L1 — Recovery Possible Under Valid Conditions

If:

- TTL not expired
- Transport candidate valid
- Policy bounds not exceeded

Then:

RECOVERING → ATTACHED possible.

Proof Sketch:

- Reattach logic allows transition.
- No blocking external dependency required.
- Deterministic path selection ensures resolution.

Thus:
Recovery is achievable if valid transport exists.

---

## L2 — Eventual Termination Under Persistent Failure

If:

- No valid transport exists
or
- TTL expired
or
- Policy bound exceeded

Then:

State eventually transitions to TERMINATED.

No infinite RECOVERING loop allowed.

Proof Sketch:

- Recovery bounded by TTL.
- Switch rate limited.
- No infinite retry without version increment.

Thus:
System cannot stall indefinitely.

---

## L3 — No Infinite Oscillation

Switching constrained by:

- MaxSwitchesPerMinute
- Cooldown windows
- Recovery window bounds

If oscillation persists:

Session enters DEGRADED or TERMINATED.

Therefore:
Infinite oscillation is structurally prevented.

---

# 4. Determinism Argument

Transition function:

δ(S, event) → S'

is deterministic because:

- Preconditions are explicit
- Rejection rules are explicit
- Version mismatch prevents ambiguity
- No random mutation

Thus:

Given identical inputs and state,
outputs are identical.

---

# 5. Bounded Recovery Guarantee

Recovery is bounded by:

TransportLossTtlMs
RecoveryWindowMs
SwitchRateLimit

Thus:

Recovery attempts cannot grow unbounded.

Bounded systems scale.
Unbounded systems collapse.

Jumping VPN enforces bounds.

---

# 6. Failure Containment

A failing session:

- Cannot mutate another session.
- Cannot corrupt global state.
- Cannot create cross-session identity leak.

Because:

- No shared mutable identity.
- No cross-session state mutation.
- No global locking dependency.

Isolation preserves safety at scale.

---

# 7. Termination Safety

If invariants cannot be preserved:

Transition → TERMINATED

This ensures:

Correctness > Continuity

The protocol never sacrifices identity integrity
for transport survival.

---

# 8. Summary

Safety guarantees:

- No dual-active binding
- No silent identity reset
- No replay mutation
- No ownership ambiguity
- No infinite oscillation

Liveness guarantees:

- Recovery possible within bounds
- Eventual termination under persistent failure
- Deterministic progression

This defines the behavioral core of Jumping VPN.

---

# Final Principle

Transport instability is tolerated.

Identity ambiguity is not.

Session is the anchor.
Transport is volatile.