# Jumping VPN — Core Invariants (Preview)

This document defines the **non-negotiable invariants** of the Jumping VPN architecture.

Invariants are written as **review rules**:
- if an invariant is violated, the protocol is considered incorrect
- the demo trace + validator exist to make these invariants observable

---

## Invariant 0 — Terminology

- **Session Anchor**: the stable identity + continuity state.
- **Transport Attachment**: a volatile carrier (path/socket) attached to a session.
- **Continuity**: monotonic progression of session state over time.

---

## Invariant 1 — Session identity is transport-independent

A session must remain valid even if:
- IP changes
- NAT mapping rebinding occurs
- UDP path dies
- jitter/loss spikes occur
- the system switches transport

**Rule:** transport failure must never implicitly reset session identity.

---

## Invariant 2 — Explicit state transitions only

State must change only via explicit transitions:

- transition must include `from`, `to`, and `reason`
- transition must increase `state_version`

**Rule:** no silent transitions.

---

## Invariant 3 — Single active attachment

At any time, there is at most **one active transport attachment** for a session.

**Rule:** dual-active attachments are forbidden.

If multiple attachments appear:
- exactly one can become active
- others must be rejected or pruned as stale/zombie

---

## Invariant 4 — Continuity is monotonic

Continuity must be monotonic over session lifetime.

- every accepted event/frame must progress continuity state
- rejected events must not mutate session state

**Rule:** the session must never accept a stale continuity progression.

---

## Invariant 5 — Replay and injection are rejected before mutation

Architectural model:

- every frame/event is bound to the session identity
- every frame/event has a monotonic counter
- receiver validates a bounded window

Reject conditions:

- duplicate counter
- out-of-window counter
- invalid binding/authentication
- invalid session_id binding

**Rule:** rejection happens **before** any state transition or flow-control mutation.

---

## Invariant 6 — Transport switch is explicit and auditable

A transport switch must emit an event:

- `TRANSPORT_SWITCH`
- `from_path`
- `to_path`
- `reason`

Switching must be policy-bounded (cooldown/switch-rate).

**Rule:** no implicit switch.

---

## Invariant 7 — Volatility is a modeled state

Transport instability must not be treated as "random noise".

When volatility is detected, the session must enter a volatility state:

- `ATTACHED → VOLATILE` (reason-coded)
- bounded adaptation may occur

**Rule:** volatility is observable in the trace.

---

## Invariant 8 — Deterministic recovery

Recovery is deterministic and reason-coded:

- the system enters a recovery window
- stability criteria returns the session to `ATTACHED`
- recovery must not require renegotiation of identity

**Rule:** trace replay must reconstruct the same state trajectory.

---

## Invariant 9 — Termination is explicit and final

Termination must be explicit:

- `STATE_CHANGE ... → TERMINATED`
- includes reason

**Rule:** after termination, no new attachments can revive the session
unless a new session is created with a new identity.

---

## Invariant 10 — Observability contract

The demo/trace must allow a reviewer to confirm:

- session was created
- volatility occurred
- adaptation/switch occurred
- recovery completed
- session remained continuous

If the trace cannot prove these claims, the demo fails.

---

## Summary

Jumping VPN is correct only if:

- **identity remains anchored to session**
- transport remains replaceable
- volatility is modeled
- recovery is deterministic
- replay/injection are rejected before mutation
- transitions are explicit + auditable