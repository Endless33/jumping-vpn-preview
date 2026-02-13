# Formal Properties — Jumping VPN (Preview)

This document describes the formal behavioral properties
that the Jumping VPN architecture aims to guarantee.

It is not a formal proof.
It is a machine-reasonable contract definition.

---

# 1. Model Overview

Let:

S = Session  
T = Transport  
P = Policy  
State ∈ {BIRTH, ATTACHED, VOLATILE, DEGRADED, RECOVERING, TERMINATED}

A session S may be bound to at most one active transport T at any time.

---

# 2. Identity Invariance

Property 1 — Session Identity Stability

For any session S:

If State(S) ≠ TERMINATED  
Then SessionID(S) is constant across all transport reattachments.

Formally:

∀ t₁, t₂  
If S exists at time t₁ and t₂ and not TERMINATED in between  
Then SessionID(t₁) = SessionID(t₂)

---

# 3. Single Active Binding

Property 2 — Single Transport Binding

At any time:

|ActiveTransports(S)| ≤ 1

No state transition may produce two simultaneous active bindings.

Violation = correctness failure.

---

# 4. Deterministic State Transition

Property 3 — Explicit Transition Rule

For any state transition:

Stateₙ → Stateₙ₊₁

There exists:

- an explicit trigger
- a deterministic reason_code
- a policy-bound decision rule

No transition may occur implicitly.

---

# 5. Bounded Recovery

Property 4 — Bounded Recovery Window

Let:

TransportLossTtlMs = P.transport_loss_ttl

If no active transport exists for duration > TransportLossTtlMs  
Then:

State(S) = TERMINATED

Recovery cannot be infinite.

---

# 6. No Silent Identity Reset

Property 5 — Identity Continuity

If a transport switch occurs:

TransportSwitch(S, T_old → T_new)

Then:

SessionID remains unchanged  
Cryptographic context remains bound  
No implicit handshake resets identity

Unless policy explicitly requires new session.

---

# 7. Anti-Flap Constraint

Property 6 — Bounded Switch Rate

Let:

MaxSwitchesPerMinute = P.max_switch_rate

If SwitchCount(S, window) > MaxSwitchesPerMinute  
Then:

Further switches are denied  
Session enters DEGRADED or TERMINATED

Switching must be rate-limited.

---

# 8. Replay Safety

Property 7 — Monotonic Freshness

For any REATTACH_REQUEST:

nonce_new > nonce_last_accepted

If not:

Reject request  
No state mutation occurs

Replay must never alter session state.

---

# 9. Version Monotonicity

Property 8 — State Version Monotonicity

Let:

state_version ∈ ℕ

Each valid state transition:

state_versionₙ₊₁ = state_versionₙ + 1

If incoming transition references stale version:

Reject mutation

Prevents rollback.

---

# 10. Cluster Safety

Property 9 — No Dual Ownership

At any time:

|Owners(S)| ≤ 1

If ownership ambiguity detected:

Reattach must be rejected  
Session must not become dual-active

Consistency > availability.

---

# 11. Explicit Termination

Property 10 — Deterministic Termination

Termination must occur only when:

- Session TTL exceeded
- TransportLoss TTL exceeded
- Policy violation exceeded bounds
- Security violation detected

Termination must emit:

STATE_CHANGE → TERMINATED  
with explicit reason_code

No silent disappearance.

---

# 12. Safety vs Liveness

Jumping VPN prioritizes:

Safety over liveness.

If safety invariant conflicts with availability:

System must prefer deterministic termination
over ambiguous continuation.

---

# 13. Behavioral Definition

The architecture defines correctness as:

For all valid execution traces:

- No identity ambiguity
- No dual-active transport
- No silent state transitions
- No unbounded recovery
- No state rollback

If these properties hold,
the system is behaviorally sound.

---

# 14. Scope

This document defines:

Behavioral formal properties.

It does not define:

- Cryptographic proofs
- Cipher strength
- Topology secrecy
- Anonymity guarantees

---

Session is the anchor.  
Transport is volatile.  
Correctness requires determinism.