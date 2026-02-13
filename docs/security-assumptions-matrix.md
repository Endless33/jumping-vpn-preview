# Security Assumptions Matrix — Jumping VPN (Preview)

Status: Draft  
Scope: Explicit security boundaries and adversary model  

This document defines the explicit assumptions made by Jumping VPN
and the guarantees provided within those assumptions.

The goal is clarity — not marketing.

---

# 1. Threat Model Scope

Jumping VPN operates at the session/control layer.

It assumes the presence of network volatility and potential adversarial interference.

It does NOT assume a trusted network.

---

# 2. Adversary Capability Matrix

| Capability                                | Assumed? | Mitigated? | Notes |
|--------------------------------------------|----------|------------|-------|
| Passive traffic observation                | YES      | PARTIAL    | Metadata visible; session identity continuity protected |
| Packet loss injection                      | YES      | YES        | Modeled as volatility |
| Transport interruption                     | YES      | YES        | Explicit RECOVERING state |
| NAT churn / IP rotation                    | YES      | YES        | Reattach mechanism |
| Replay of old reattach messages            | YES      | YES        | Nonce + replay window |
| Stale state mutation attempt               | YES      | YES        | state_version enforcement |
| Dual-active binding attempt                | YES      | YES        | Invariant enforcement |
| Cluster ownership ambiguity                | YES      | YES        | Reattach rejection |
| Control-plane flooding                     | YES      | PARTIAL    | Rate limits required |
| Endpoint compromise                        | YES      | NO         | Out of scope |
| Kernel compromise                          | YES      | NO         | Out of scope |
| Cryptographic primitive break              | YES      | NO         | Assumed secure |
| Nation-state DPI fingerprinting            | YES      | NO         | Out of scope |

---

# 3. Security Boundary Definition

Jumping VPN guarantees:

- No silent identity reset
- No dual-active continuation
- Deterministic rejection on ambiguity
- Bounded recovery window
- Replay protection at session layer

Jumping VPN does NOT guarantee:

- Anonymity
- Censorship bypass
- Endpoint integrity
- Stealth against advanced DPI
- Anti-forensic properties

---

# 4. Attack Surface Layers

Layer 1: Data Plane  
- Transport metadata visible  
- Encryption defined elsewhere  
- Out of scope in this preview  

Layer 2: Control Plane  
- Reattach validation  
- State transitions  
- Version enforcement  
- Replay window  

Layer 3: Session Ownership  
- Authoritative store or sticky routing  
- Atomic update requirement  
- Split-brain rejection  

Layer 4: Policy Layer  
- Switch rate limits  
- Recovery deadlines  
- TTL enforcement  

---

# 5. Failure vs Attack Distinction

Jumping VPN intentionally models:

Volatility ≠ attack  

Transport instability may be:

- natural network behavior
- congestion
- mobile roaming
- adversarial disruption

Behavioral reaction is deterministic regardless of root cause.

---

# 6. Replay Protection Assumption

Security assumption:

Client nonces are monotonic.

Server maintains bounded replay window.

Guarantee:

- Replayed nonce MUST be rejected.
- Rejected replay MUST NOT mutate state.
- Replay rejection MUST be logged.

---

# 7. State Integrity Guarantee

Under defined threat assumptions:

- state_version MUST never decrement
- stale updates MUST be rejected
- transitions MUST be atomic

Ambiguous state → reject or terminate.

---

# 8. Control Plane Flooding

Assumption:

Attacker MAY flood reattach requests.

Mitigation expectation:

- Rate limiter
- Early reject unknown sessions
- Fail closed without mutation

The protocol MUST NOT degrade into uncontrolled switching.

---

# 9. Cluster Safety Model

In multi-node deployment:

Assumption:
Network partition MAY occur.

Requirement:
Ownership ambiguity MUST result in rejection.

Consistency > availability.

---

# 10. Safety vs Liveness Tradeoff

Jumping VPN prioritizes:

Safety invariants
over
Maximal session survival

If invariants cannot be guaranteed:

Session MUST terminate.

---

# 11. Explicit Non-Security Claims

This preview does NOT claim:

- Quantum resistance
- Perfect forward secrecy specification
- Obfuscation layer
- Traffic morphing
- Anti-correlation routing
- Anti-fingerprinting guarantees

Security scope is intentionally constrained to:

Deterministic session continuity under volatility.

---

# 12. Reviewer Guidance

When reviewing:

Verify that:

- All rejection paths are explicit
- No silent fallback exists
- No implicit renegotiation occurs
- No dual binding is possible
- No unbounded retry loop exists

Look for:

Determinism  
Explicit transitions  
Invariant enforcement  

---

# 13. Summary

Security in Jumping VPN is:

Constraint-driven  
Explicit  
Bounded  
Auditable  

It is not stealth-oriented.  
It is correctness-oriented.

Session is the anchor.  
Transport is volatile.  
Ambiguity is rejected.