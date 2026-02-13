# Formal Guarantees — Jumping VPN (Preview)

This document defines the behavioral guarantees of Jumping VPN
under bounded transport volatility.

These guarantees are architectural claims.
They are not marketing statements.

---

# 1. Scope of Guarantees

Guarantees apply only when:

- Session lifetime has not expired
- Recovery window is within policy bounds
- At least one valid transport candidate exists
- No cryptographic compromise is detected

Outside these bounds, termination is explicit.

---

# 2. Session Identity Guarantee

## Guarantee G1 — Identity Persistence

If a transport fails and a valid backup exists:

- SessionID remains unchanged
- Cryptographic context remains bound
- No full renegotiation occurs

Identity reset is forbidden unless:
- Session TTL expires
- Security violation detected
- Policy explicitly forces reset

---

# 3. Single Active Transport Guarantee

## Guarantee G2 — No Dual Binding

At any moment:

|ActiveTransport(session)| ≤ 1

It is forbidden for two transports to be active simultaneously for the same session.

Violation must trigger:
- Immediate termination OR
- Explicit invariant breach event

---

# 4. Deterministic State Transition Guarantee

## Guarantee G3 — No Silent Transitions

All session state transitions:

- Must emit a STATE_CHANGE event
- Must include reason_code
- Must be policy-bounded

No implicit transitions are allowed.

---

# 5. Bounded Recovery Guarantee

## Guarantee G4 — Recovery Window

Transport recovery must occur within:

RecoveryWindowMs ≤ Policy.MaxRecoveryWindowMs

If recovery exceeds bound:

Session enters TERMINATED explicitly.

No undefined hanging states allowed.

---

# 6. Rate-Limited Adaptation Guarantee

## Guarantee G5 — Anti-Flapping Constraint

Transport switches per session are bounded:

SwitchRate ≤ Policy.MaxSwitchesPerMinute

Exceeding bound results in:

- DEGRADED state OR
- Explicit termination

---

# 7. Invariant Enforcement Guarantee

## Guarantee G6 — Observable Violations

If any invariant is violated:

- An AUDIT_EVENT must be emitted
- Session behavior must be deterministic
- No undefined continuation allowed

---

# 8. Non-Guaranteed Properties

Jumping VPN does NOT guarantee:

- Global anonymity
- Resistance to endpoint compromise
- Immunity to active MITM at crypto layer
- Infinite recovery under sustained attack
- Censorship bypass

Scope is strictly:

Deterministic recovery under bounded transport volatility.

---

# 9. Contract Philosophy

If a property cannot be:

- Measured
- Logged
- Bounded
- Audited

It is not considered a guarantee.

---

Session remains the anchor.
Transport is volatile.