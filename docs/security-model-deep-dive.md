# Security Model Deep Dive — Jumping VPN (Preview)

This document defines the security boundaries,
assumptions, and guarantees of the Jumping VPN architecture.

It is not a cryptographic specification.
It is a behavioral and adversarial model clarification.

---

# 1. Security Philosophy

Jumping VPN does not assume:

- Stable transport
- Benevolent network conditions
- Reliable path continuity

It assumes:

- Transport volatility is normal
- On-path observation is possible
- Transport disruption is common
- Session continuity must be bounded

Security is defined as:

Deterministic identity preservation under bounded volatility.

---

# 2. Adversary Model

## 2.1 On-Path Attacker

Capabilities:

- Observe transport metadata
- Drop packets
- Inject delay
- Induce packet loss
- Force transport churn

Limitations:

- Cannot forge proof-of-possession
- Cannot bypass replay validation
- Cannot break cryptographic primitives (assumed secure)

---

## 2.2 Off-Path Attacker

Capabilities:

- Flood control-plane endpoints
- Attempt replay attacks
- Attempt session guessing
- Trigger reattach abuse

Mitigations:

- Unknown SessionID rejection
- Rate-limited reattach handling
- Replay window validation
- Bounded resource allocation

---

## 2.3 Cluster-Level Threats

Threats:

- Dual-active session ownership
- Split-brain during reattach
- Stale state reactivation

Mitigation principle:

Consistency over availability.

If ownership is ambiguous:
- Reject reattach
- Terminate deterministically

Dual-active identity is forbidden.

---

# 3. Identity Binding Model

## 3.1 Session Identity

Session identity consists of:

- SessionID
- Key material (abstracted in preview)
- Policy context
- State version

Transport binding is not identity.

---

## 3.2 Reattach Validation

Reattach requires:

- Proof-of-possession (session-bound)
- Freshness validation (anti-replay window)
- Ownership authority verification
- Policy-bound eligibility

If any check fails:
- Reattach is rejected
- No state mutation occurs

---

# 4. Replay Handling

Replay handling requires:

- Monotonic nonce tracking
- Sliding replay window
- Bounded storage per session
- Deterministic rejection of stale packets

Replay must never:

- Trigger state rollback
- Rebind transport
- Reset identity

---

# 5. Transport Switching Safety

Transport switching must:

- Be explicit
- Be reason-coded
- Increment state_version
- Respect switch-rate bounds
- Emit auditable event

Transport switch must NOT:

- Reset session identity
- Duplicate active binding
- Occur silently

---

# 6. Bounded Recovery Model

Two key timers:

Session TTL:
- Maximum lifetime of session identity

Transport-Loss TTL:
- Maximum duration session may remain unattached

If transport-loss TTL expires:
- Session transitions to TERMINATED deterministically

Recovery is bounded.
Infinite volatility loops are forbidden.

---

# 7. Anti-Flap Mechanism

To prevent oscillation:

- Consecutive failure threshold
- Minimum observation window
- Cooldown after switch
- Maximum switches per time window

Switching is not heuristic.
It is policy-gated.

---

# 8. Observability as Security Control

All critical events must be:

- Explicit
- Structured
- Exportable
- Non-blocking

Security events include:

- Reattach rejected
- Replay detected
- Ownership conflict
- Policy-bound termination

Logging failure must not affect correctness.

---

# 9. Non-Goals (Security Scope Limits)

Jumping VPN does NOT claim:

- Anonymity against global passive adversary
- Censorship evasion guarantees
- Endpoint compromise protection
- Anti-forensic invisibility
- Perfect forward secrecy (not specified here)

Security scope is explicitly bounded.

---

# 10. Hard Safety Invariants

The following must always hold:

- One session → one active transport
- SessionID never changes during lifecycle
- All transitions are explicit
- Ambiguity resolves to rejection or termination
- No silent identity reset
- No dual-active ownership

Violation of any invariant is a correctness failure.

---

# 11. Engineering Security Boundary

This preview focuses on:

Behavioral security under volatility.

Cryptographic hardening,
key exchange protocols,
cipher selection,
and handshake formalization
are out of scope for this repository stage.

---

# 12. Summary

Security in Jumping VPN is defined as:

Identity continuity under hostile, unstable transport conditions,
bounded by deterministic policy rules.

It is not magic routing.
It is disciplined state control.

---

Session is the anchor.  
Transport is volatile.  
Security requires determinism.