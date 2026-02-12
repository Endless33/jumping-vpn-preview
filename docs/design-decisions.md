# Jumping VPN — Design Decisions (Public Preview)

This document explains key architectural decisions behind Jumping VPN.

The purpose is not marketing.
The purpose is clarity.

---

## DD-01 — Session is Primary, Transport is Replaceable

Decision:
The session is treated as the source of truth.
Transports are considered ephemeral bindings.

Rationale:
Modern networks are volatile.
Binding identity directly to transport creates fragility.

Alternative considered:
Transport-bound identity (traditional tunnel model).

Rejected because:
Transport volatility would implicitly terminate identity.

---

## DD-02 — No Silent Renegotiation

Decision:
Transport failure must not trigger hidden full renegotiation.

Rationale:
Implicit renegotiation hides state changes from operators.
Security-sensitive systems require explicit transitions.

Alternative considered:
Automatic transparent re-handshake.

Rejected because:
It obscures auditability and weakens deterministic guarantees.

---

## DD-03 — Explicit Transport Switching

Decision:
All transport changes must be explicit and logged.

Rationale:
Security events must be observable.
Operators should never guess why continuity changed.

Alternative considered:
Silent best-path switching.

Rejected because:
Unobservable adaptation complicates incident analysis.

---

## DD-04 — Bounded Adaptation

Decision:
Switch rate, recovery windows, and volatility thresholds are limited by policy.

Rationale:
Unbounded adaptation can be abused.
Oscillation can degrade availability more than failure itself.

Alternative considered:
Unlimited adaptive switching.

Rejected because:
It creates instability under adversarial conditions.

---

## DD-05 — Deterministic Failure Boundaries

Decision:
If recovery is not possible within policy constraints,
the session must terminate explicitly.

Rationale:
Undefined limbo states are dangerous.
Failing explicitly is safer than pretending stability.

Alternative considered:
Indefinite degraded persistence.

Rejected because:
It hides systemic failure and complicates recovery guarantees.

---

## DD-06 — Observability as a First-Class Feature

Decision:
State transitions and transport switches emit structured events.

Rationale:
SOC, NOC, and audit teams require traceable behavior.

Alternative considered:
Minimal logging.

Rejected because:
Behavior without traceability cannot be trusted.

---

## DD-07 — Volatility as a Modeled State

Decision:
Volatility is treated as a formal session state.

Rationale:
Instability is normal in modern networks.
Modeling it explicitly allows bounded response.

Alternative considered:
Treat volatility as error condition only.

Rejected because:
It conflates transient instability with fatal failure.

---

## DD-08 — Clear Non-Goals

Decision:
The protocol does not claim:
- Endpoint compromise resistance
- Full anonymity guarantees
- Censorship bypass capabilities
- Malware protection

Rationale:
Scope clarity increases credibility.
Overextended claims reduce trust.

---

## DD-09 — Policy-Driven Behavior

Decision:
Transport behavior is constrained by configurable policy.

Rationale:
Different environments require different tolerance levels.

Example:
- High-availability enterprise
- Mobile field operations
- Edge compute cluster

Behavior must adapt within bounded constraints.

---

## DD-10 — Architectural Before Implementation

Decision:
Public repository prioritizes architectural clarity over production code.

Rationale:
Early transparency builds informed discussion.
Security-critical logic requires staged hardening.

---

## Summary

Jumping VPN is not defined by features.

It is defined by:

- Bounded adaptation
- Explicit state modeling
- Deterministic failure behavior
- Session-centric identity
- Auditable transitions

Design decisions are intentional,
not emergent side effects.