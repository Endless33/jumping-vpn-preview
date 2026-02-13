# Security Boundary Model — Jumping VPN (Preview)

This document defines the security boundaries,
trust assumptions, and attacker model
for Jumping VPN’s behavioral architecture.

This is a boundary model — not a cryptographic proof.

---

## 1) Security Philosophy

Jumping VPN does not assume stable networks.
It assumes disruption is normal.

Security goal:
- Preserve session identity under volatility
- Prevent hijack during reattach
- Avoid silent corruption
- Fail closed on ambiguity

Continuity must never weaken identity guarantees.

---

## 2) Trust Boundaries

### 2.1 Trusted Components

- Client Agent (within OS trust boundary)
- Server Gateway (authoritative session owner)
- Session Table / Ownership Layer
- Policy Engine (deterministic rules)

### 2.2 Semi-Trusted

- Underlying transport channels
- NAT devices
- Intermediate routing nodes

These may:
- drop packets
- reorder traffic
- introduce delay
- change ports
- disappear entirely

Transport is NOT trusted for identity continuity.

---

## 3) Attacker Model

Assume attacker can:

- Observe transport-level metadata
- Induce packet loss
- Force path instability
- Drop traffic selectively
- Attempt replay of control-plane messages
- Attempt reattach hijack
- Attempt reattach flood (DoS)
- Attempt cluster ownership confusion

Assume attacker cannot:

- Break cryptographic primitives
- Forge proof-of-possession without key material
- Control authoritative session store (unless compromised)

---

## 4) Threat Categories

### 4.1 Replay Attack

Goal:
Reuse a previously valid reattach message.

Mitigation:
- Freshness marker (nonce/timestamp)
- Bounded anti-replay window
- Deterministic rejection
- Security event emission

---

### 4.2 Reattach Hijack

Goal:
Bind attacker-controlled transport to victim session.

Mitigation:
- Proof-of-possession validation
- Session-bound key material
- Ownership authority validation
- Fail closed on ambiguity

---

### 4.3 Control-Plane Flood

Goal:
Overload reattach validation to degrade service.

Mitigation:
- Rate limiting
- Early rejection of unknown SessionID
- Bounded memory structures
- Fail closed without mutating state

---

### 4.4 Dual-Active Binding

Goal:
Cause two transports to be active simultaneously.

Mitigation:
- Single owner invariant
- Atomic state update (CAS/transaction)
- Versioned state transitions
- Explicit rejection on conflict

---

### 4.5 Forced Volatility / Churn

Goal:
Trigger infinite switching.

Mitigation:
- MaxSwitchesPerMinute
- CooldownAfterSwitch
- Degraded mode
- Explicit termination if bounds exceeded

---

## 5) Security Invariants

S1. A session can have at most one ACTIVE binding.
S2. SessionID cannot change without explicit handshake.
S3. Reattach requires proof-of-possession.
S4. Replay attempts are rejected deterministically.
S5. Ambiguous authority results in rejection.
S6. Recovery attempts are bounded by policy.
S7. Control-plane abuse cannot silently mutate session state.

---

## 6) Failure Boundaries

If security conditions fail:

- Reject reattach explicitly
- Emit security event
- Do NOT silently reset identity
- Do NOT silently migrate authority

Ambiguity is treated as failure.

---

## 7) Out of Scope

This model does NOT claim:

- Anonymity guarantees
- Traffic obfuscation
- Censorship bypass
- Endpoint compromise protection
- Post-quantum cryptography

It defines behavioral continuity under volatility,
not universal privacy.

---

## 8) Security Review Target

A production implementation must undergo:

- Cryptographic review
- Replay window correctness validation
- Control-plane abuse simulation
- Cluster ownership safety review
- Resource exhaustion testing

This repository documents behavioral intent,
not final hardened implementation.

---

Security must remain stronger than continuity.

Session is the anchor.  
Transport is volatile.