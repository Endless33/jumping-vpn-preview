# Jumping VPN — Architectural Invariants

Architectural invariants define conditions that must remain true at all times.

They are the foundation of deterministic protocol behavior.

If an invariant is violated, the protocol is considered incorrect.

---

# Definition

Invariant:

A condition that must always hold true regardless of transport volatility, path changes, or network instability.

Invariants protect identity continuity.

---

# Invariant 1 — Session Identity Continuity

The session identifier must never change during the lifetime of the session.

Formal definition:

∀ t0, t1 ∈ session_lifetime:
session_id(t0) == session_id(t1)

Transport changes must not modify session identity.

Violation would represent identity discontinuity.

---

# Invariant 2 — Transport Independence of Identity

Session identity must exist independently of transport attachment.

Formal model:

identity = session_anchor transport = attachment(identity)

Transport removal must not destroy identity.

Transport replacement must not recreate identity.

---

# Invariant 3 — Single Active Transport Attachment

At most one active transport attachment may exist at any time.

Formal definition:

active_attachments ≤ 1

This prevents ambiguity and race conditions.

Inactive attachments may exist as candidates.

---

# Invariant 4 — Explicit State Transitions Only

All session state transitions must be explicit.

No implicit or silent transitions are allowed.

Formal definition:

state(t+1) ≠ state(t) ⇒ transition_event must exist

Every state transition must be observable in trace.

---

# Invariant 5 — Deterministic Recovery

Recovery must not recreate identity.

Recovery must restore transport attachment while preserving session identity.

Formal definition:

recovery(session_id) ⇒ session_id unchanged

Recovery is a state transition, not session recreation.

---

# Invariant 6 — No Silent Identity Reset

Identity reset must only occur via explicit session termination.

Forbidden behavior:

transport_failure ⇒ new session_id

Correct behavior:

transport_failure ⇒ attachment replacement

---

# Invariant 7 — Observable State Machine

All state transitions must be observable via event emission.

Example events:

- SESSION_CREATED
- VOLATILITY_SIGNAL
- TRANSPORT_SWITCH
- STATE_CHANGE
- RECOVERY_COMPLETE

Trace must fully represent protocol behavior.

---

# Invariant 8 — Attachment Replaceability

Transport attachment must be replaceable without affecting session identity.

Formal definition:

replace(attachment_A, attachment_B) ⇒ session_id unchanged

This enables transport-independent session continuity.

---

# Invariant 9 — Deterministic Behavior

Given identical input conditions, protocol behavior must be deterministic.

Formal definition:

input(t0) == input(t1) ⇒ output(t0) == output(t1)

This enables replay validation.

---

# Invariant 10 — Session Anchor Persistence

Session anchor must exist independently of attachment lifecycle.

Formal model:

destroy(attachment) ≠ destroy(session_anchor)

Session anchor persists until explicit termination.

---

# Invariant Verification

Invariants can be validated via replay:

python demo_engine/replay.py DEMO_TRACE.jsonl

Validator confirms invariant preservation.

---

# Why Invariants Matter

Without invariants, protocol behavior becomes ambiguous.

Ambiguity creates:

- identity discontinuity
- recovery failures
- unpredictable behavior

Invariants enforce deterministic architecture.

---

# Architectural Impact

These invariants enable:

- transport-independent identity
- deterministic recovery
- observable protocol behavior
- replay validation

Transport becomes replaceable.

Identity persists.

---

# Summary

Jumping VPN is defined by invariant-preserving behavior.

The protocol guarantees identity continuity regardless of transport volatility.

This is the foundation of session-anchored transport architecture.