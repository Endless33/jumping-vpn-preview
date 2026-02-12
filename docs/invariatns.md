# Jumping VPN — Architectural Invariants

This document defines the invariants that must always hold true
for Jumping VPN to remain architecturally correct.

If an invariant is violated, the system is considered broken.

---

## 1) Session Identity Invariant

A session identity must not silently reset.

- Session ID cannot change without explicit termination.
- Reattachment must preserve identity continuity.
- Any identity change must emit an explicit `SessionTerminated` event.

Transport death does not imply session identity change.

---

## 2) Transport Replacement Invariant

Transport death ≠ session death (within defined bounds).

If:
- session TTL not exceeded
- valid reattachment proof provided
- policy limits respected

Then:
- the session must survive
- a `TransportSwitch` event must be emitted
- continuity must be preserved

---

## 3) Explicit Transition Invariant

All critical state transitions must be:

- explicit
- logged
- reason-coded

No hidden transitions.
No silent renegotiation.
No implicit recovery without audit trace.

---

## 4) Bounded Adaptation Invariant

Adaptation must remain bounded.

This includes:

- maximum transport switch rate
- anti-flapping dampening
- recovery windows
- deterministic timeout behavior

The system must never enter uncontrolled oscillation.

---

## 5) Deterministic Termination Invariant

Session termination must be deterministic.

Termination may occur if:

- TTL exceeded
- no viable transport available
- cryptographic validation fails
- policy constraints violated

Termination must:

- emit `SessionTerminated`
- include a reason code
- never occur silently

---

## 6) Replay Resistance Invariant (Hardened Layer)

Reattachment must require valid proof of possession.

The system must reject:

- stale reattach attempts
- replayed proofs
- transport hijacking attempts

Preview implementations may simulate this,
but production systems must enforce it strictly.

---

## 7) Observability Invariant

Every transport switch and session state change must be observable.

Operators must be able to reconstruct:

- why a switch occurred
- when it occurred
- under what policy condition
- what transport replaced what

If a switch cannot be explained,
the system violates its observability invariant.

---

## 8) No Undefined States Invariant

The state machine must not contain:

- unreachable states
- contradictory transitions
- ambiguous recovery paths

All states must be:

- finite
- defined
- policy-bounded

---

## Summary

Jumping VPN is not defined by features.
It is defined by invariants that constrain behavior over time.

If these invariants hold,
session continuity remains trustworthy
even under transport volatility.