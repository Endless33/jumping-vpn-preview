# Formal Invariants (Machine-Oriented) — Jumping VPN

This document expresses Jumping VPN invariants
in a machine-oriented, semi-formal style.

It is not a mathematical proof.
It is a deterministic behavioral contract.

---

# 1) State Model

Let:

S = { BIRTH, ATTACHED, VOLATILE, DEGRADED, RECOVERING, TERMINATED }

Each session has:

session_id: UUID
state: S
state_version: integer (monotonic)
active_transport: TransportID | null
last_state_change_ts: int64
policy: PolicySnapshot

---

# 2) Core Safety Invariants

## I1 — Single Active Transport

For any session:

∀ t:
count(active_transport where session_id == X AND state ∈ {ATTACHED, VOLATILE, RECOVERING}) ≤ 1

No dual-active binding is permitted.

Violation outcome:
→ Reject new binding OR terminate deterministically.

---

## I2 — Identity Stability

If session.state != TERMINATED:

session_id must remain constant across transport changes.

TransportSwitch does NOT mutate session_id.

---

## I3 — Monotonic State Version

For every state transition:

new.state_version = old.state_version + 1

No transition may reuse or decrement state_version.

Stale transitions MUST be rejected.

---

## I4 — Explicit Transition Rule

Every state change MUST:

- define previous_state
- define next_state
- include reason_code
- increment state_version

Implicit state mutation is forbidden.

---

## I5 — Bounded Recovery Window

Let:

transport_loss_ttl_ms = policy.TransportLossTtlMs

If:

current_time - last_successful_delivery > transport_loss_ttl_ms

AND no valid reattach occurred,

Then:

state MUST transition → TERMINATED
with reason_code = TRANSPORT_TTL_EXPIRED

---

## I6 — Rate-Limited Switching

Let:

switch_count_in_window ≤ policy.MaxSwitchesPerMinute

If exceeded:

Transition MUST be:

→ DEGRADED
OR
→ TERMINATED (if repeated abuse detected)

Switch oscillation is forbidden.

---

## I7 — Reattach Authenticity

A reattach is valid only if:

validate(proof_of_possession) == true
AND freshness_window_ok == true
AND ownership_authority_ok == true

Otherwise:

Reattach MUST be rejected without state mutation.

---

## I8 — No Silent Termination

Termination MUST:

- Emit STATE_CHANGE
- Emit AUDIT_EVENT
- Include reason_code

Silent identity loss is forbidden.

---

# 3) Liveness Guarantees

Liveness is bounded.

If:

∃ viable transport candidate
AND reattach occurs within recovery window
AND switch limits not exceeded

Then:

state must eventually return to ATTACHED.

(Under defined policy bounds.)

---

# 4) Degraded Mode Semantics

DEGRADED is not failure.

In DEGRADED:

- Switching frequency may be reduced
- Transport candidates filtered more aggressively
- Policy tightening applies
- Identity continuity remains preserved

DEGRADED must be observable and reason-coded.

---

# 5) Forbidden Conditions

The following states are illegal:

1) Two active transports bound to one session.
2) session_id mutation without TERMINATED.
3) state_version regression.
4) Reattach accepted without proof validation.
5) Recovery attempts beyond TTL without termination.
6) Silent identity reset.

Illegal condition → must trigger explicit termination.

---

# 6) Cluster Safety Rule

In clustered deployment:

∀ session_id:

At most one authoritative owner node at time t.

Ownership transfer MUST be atomic:

CAS(old_owner → new_owner)
WITH state_version increment.

Split-brain continuation is forbidden.

---

# 7) Deterministic Failure Contract

If system cannot guarantee invariants:

It must fail closed.

Prefer explicit termination
over ambiguous continuation.

---

# 8) Formal Intent

This document allows reviewers to reason about:

- Safety
- Determinism
- Ownership
- Replay resistance
- Bounded recovery

This is architectural validation,
not production proof.

---

Session is the anchor.  
Transport is volatile.
Invariants are non-negotiable.