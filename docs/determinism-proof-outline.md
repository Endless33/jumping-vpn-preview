# Determinism Proof Outline — Jumping VPN (Preview)

This document outlines the determinism guarantees of the Jumping VPN session model.

This is not a formal mathematical proof.
It is a structured engineering argument showing that:

- State transitions are explicit
- Outcomes are bounded
- Ambiguity is rejected
- Recovery is deterministic
- Identity continuity is preserved within policy limits

---

# 1. Definitions

## 1.1 Session

A session S is defined as:

S = {
    session_id,
    state,
    state_version,
    active_transport,
    policy,
    ttl,
    replay_window
}

The session is the identity anchor.

---

## 1.2 Transport

A transport T is:

T = {
    transport_id,
    proto,
    remote_ip,
    remote_port,
    health_status
}

Transport is attachable and replaceable.

---

## 1.3 Deterministic System

A system is deterministic if:

Given identical:
- prior state
- input message
- time bounds
- policy parameters

The resulting:
- state transition
- output
- rejection reason

is identical.

---

# 2. State Version Monotonicity

Invariant:

state_version MUST strictly increase on every successful state transition.

Proof obligation:

For any transition:

state_version_new = state_version_old + 1

Stale updates (state_version mismatch) are rejected.

This prevents:

- rollback
- split-brain overwrites
- race condition corruption

---

# 3. Single Active Transport Invariant

Invariant:

At any time, a session has at most one ACTIVE transport.

Formally:

∀ session S:
count(transport.status == ACTIVE) ≤ 1

Proof strategy:

On REATTACH_ACCEPT:
- Previous transport is deactivated atomically
- New transport becomes ACTIVE
- State version increments

Dual activation is rejected.

---

# 4. Recovery Bound

Recovery is bounded by:

max_recovery_window_ms

If recovery_time > max_recovery_window_ms:

Session → TERMINATED

This ensures:

- No infinite recovery loops
- No indefinite half-alive sessions
- No unbounded retry storms

Determinism rule:

Recovery outcome is fully determined by:
- elapsed time
- retry count
- policy

---

# 5. Replay Determinism

Replay protection model:

- Client nonce must strictly increase
- Server maintains replay window
- Reused nonce → REJECT

Replay rejection:

- Does not change state
- Does not increment version
- Is logged

Thus:

Replay cannot cause state divergence.

---

# 6. Ambiguity Handling

Ambiguity cases:

- State version mismatch
- Dual-active binding attempt
- Ownership ambiguity (cluster)
- TTL expired
- Invalid proof-of-possession

Rule:

Ambiguity → Deterministic rejection

The system must never:
- Guess
- Retry silently
- Implicitly downgrade state

---

# 7. Failure Matrix Determinism

Given:

Input Event → Current State

Output:

Transition + ReasonCode

Examples:

ATTACHED + TRANSPORT_DEAD → RECOVERING  
RECOVERING + REATTACH_VALID → ATTACHED  
RECOVERING + TTL_EXPIRED → TERMINATED  

No transition depends on randomness.

---

# 8. No Silent Identity Reset

Invariant:

session_id remains constant across transport changes.

Identity reset only occurs via:

- explicit TERMINATE
- explicit new HANDSHAKE

Implicit identity change is forbidden.

---

# 9. Cluster Consistency Model

For multi-node deployments:

Ownership model must guarantee:

- Sticky routing
OR
- Atomic CAS state store

Without authoritative ownership:

Reattach MUST be rejected.

This prevents:

- dual continuation
- state divergence

Consistency > availability.

---

# 10. Determinism Under Adversarial Conditions

Assume attacker can:

- drop packets
- delay packets
- replay messages
- force churn

System guarantees:

- No identity hijack without valid proof
- No replay-induced state mutation
- No unbounded oscillation (rate limits + cooldown)
- No silent split-brain

If invariants cannot be preserved:

Session terminates explicitly.

---

# 11. What This Proof Does NOT Claim

This outline does NOT prove:

- Cryptographic strength
- Resistance to endpoint compromise
- Anonymity guarantees
- Network-level censorship resistance

It proves behavioral determinism of session lifecycle.

---

# 12. Engineering Interpretation

This document demonstrates that:

- State transitions are explicit
- Recovery is bounded
- Ambiguity is rejected
- Versioning prevents rollback
- Replay is neutralized
- Identity continuity is controlled

The model prefers:

Explicit termination over implicit corruption.

---

# Final Principle

If correctness cannot be guaranteed,
the system must fail closed.

Determinism is stronger than survivability.

Session is the anchor.  
Transport is volatile.  
Behavior must be predictable.