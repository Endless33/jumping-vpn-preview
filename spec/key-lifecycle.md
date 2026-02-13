# Jumping VPN — Key Lifecycle (Abstract Requirements)

Status: Normative Security Requirements (Public Preview)

This document defines key lifecycle semantics for a session-centric,
transport-volatile VPN model.

Cryptographic primitives and exact wire formats are abstracted.
Behavioral requirements are normative.

---

## 1. Goals

Key lifecycle must support:

- session continuity across transport changes
- bounded session lifetime
- explicit reattach validation
- controlled key expiry and rotation
- prevention of hijack during volatility

---

## 2. Key Categories (Logical)

A Jumping VPN session may maintain (conceptually):

- **Session Root Context** (longer-lived anchor for the session)
- **Traffic Keys** (used for DATA plane encryption/authentication)
- **Control Keys** (used for state-mutating control messages, e.g., reattach)

Implementations may collapse categories, but must preserve semantics.

---

## 3. Binding Requirements (Normative)

### K1 — Keys bound to SessionID
All session keys MUST be cryptographically bound to:

- SessionID
- session identity context
- and validation freshness constraints

A valid key for one session MUST NOT validate another session.

---

### K2 — Reattach requires proof-of-possession
Reattach MUST require proof-of-possession of valid session key material.

Reattach MUST fail if:

- keys expired
- proof invalid
- replay detected

---

### K3 — Key expiry is explicit
If keys expire:

- session MUST NOT silently continue
- transition MUST be explicit and reason-coded

Allowed outcomes:

- require full re-handshake (new session)
- or terminate per policy

---

## 4. Lifetime Controls (Normative)

### 4.1 SESSION_MAX_LIFETIME_MS
Session lifetime imposes an upper bound on key validity.

If session lifetime exceeded:

- state → TERMINATED
- reason: session_lifetime_exceeded

### 4.2 KEY_MAX_AGE_MS (optional)
If keys are bounded shorter than session TTL:

- reattach may require re-key or new handshake
- must be explicit (no silent key rollover)

---

## 5. Rekey Semantics (Normative)

Rekey MUST be:

- policy-driven
- bounded
- observable

Allowed triggers:

- `time_elapsed`
- `transport_change`
- `policy_trigger`
- `security_event`

Rekey MUST NOT be triggered infinitely.

Rekey decisions MUST emit events (observability contract).

---

## 6. Rekey vs Rehandshake

### Rekey
Means:

- session identity remains the same
- keys rotate within the session
- continuity preserved

### Rehandshake (New Session)
Means:

- session identity is replaced
- SessionID changes explicitly
- old session terminates

No silent upgrade from rekey → new session.

---

## 7. Compromise & Revocation (Normative)

If compromise suspected (policy-defined):

- session MUST transition to TERMINATED
- reason: security_failure
- optionally emit `SecurityKeyCompromiseSuspected`

Revocation MUST be explicit.

---

## 8. Recovery Implications

During RECOVERING:

- keys MUST remain valid for reattach attempts within TTL
- if keys expire mid-recovery:
  - reattach MUST fail
  - session transitions deterministically to DEGRADED or TERMINATED

No undefined half-valid session state.

---

## 9. Observability Requirements

Key lifecycle events MUST be observable:

- `KeyRotated`
- `KeyExpired`
- `RekeyDenied`
- `SecurityKeyCompromiseSuspected`

Each MUST include:

- session_id
- ts_ms
- reason_code
- policy_version

---

## 10. Non-Goals

This document does NOT:

- define specific algorithms (AES/ChaCha/etc.)
- define wire formats
- define perfect forward secrecy details
- claim anonymity properties

It defines behavioral semantics for secure session continuity.

---

## Final Statement

Transport changes are normal.

Keys must survive transport changes — but not forever.

Jumping VPN enforces:

- session-bound keys
- bounded lifetime
- explicit expiry
- observable rotation

Security must remain deterministic under volatility.