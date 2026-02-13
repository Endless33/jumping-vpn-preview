# Consistency Model — Session Ownership & State Guarantees (Preview)

This document defines the consistency guarantees
of the Jumping VPN session model.

The system prioritizes:

- Identity correctness
- Deterministic state transitions
- Single-authority session ownership
- Bounded recovery

Consistency is preferred over availability when ambiguity appears.

---

# 1. Core Consistency Principle

A session must never exist in an ambiguous identity state.

At any moment:

- A session has exactly one authoritative owner.
- A session has at most one ACTIVE transport.
- State transitions are monotonic.
- Version rollback is forbidden.

If ownership cannot be determined safely,
the system must reject or terminate explicitly.

---

# 2. Session Ownership Model

Production deployments must implement one of the following:

## Option A — Sticky Routing

SessionID → fixed gateway mapping.

- Load balancer routes by SessionID hash.
- Only one gateway node handles that session.
- Ownership remains local and unambiguous.

Advantages:
- Simpler mental model
- No cross-node synchronization required

Tradeoff:
- Reduced horizontal flexibility without rebalancing

---

## Option B — Shared Authoritative Store

All gateway nodes use:

- Atomic compare-and-swap (CAS)
- Versioned session records
- Ownership flag with node_id
- Monotonic state_version

Ownership transfer requires:

1) Version match
2) Explicit mutation
3) Atomic update

If CAS fails → operation rejected.

Consistency > availability.

---

# 3. State Version Semantics

Each session has:

state_version: integer (monotonic)

Rules:

- Every successful state transition increments version.
- All control-plane mutations require matching version.
- Stale version updates are rejected.
- Version rollback is forbidden.

This prevents:

- Race conditions
- Concurrent reattach corruption
- Split-brain continuation
- State rollback under concurrency

---

# 4. Active Transport Invariant

Hard rule:

max_active_transports = 1

The system must reject:

- Dual-active binding
- Parallel reattach success
- Multi-transport identity continuity

Candidate transports may exist.
Only one may be ACTIVE.

This is a safety invariant.

---

# 5. Split-Brain Handling

If two nodes attempt to bind the same session concurrently:

- Only one may succeed (CAS-based resolution).
- The other must reject.
- Ambiguity must never be tolerated.

If authoritative ownership cannot be proven:

→ Reject
OR
→ TERMINATE (policy-defined)

Never continue in uncertain ownership.

---

# 6. Recovery Window Consistency

Recovery must be bounded by:

- TransportLossTtlMs
- MaxRecoveryWindowMs
- MaxSwitchesPerMinute

If bounds are exceeded:

→ DEGRADED
OR
→ TERMINATED

Consistency rule:

A session must not continue indefinitely
without meeting policy-defined safety constraints.

---

# 7. Deterministic Reattach Rule

Reattach succeeds only if:

- session exists
- TTL valid
- proof-of-possession valid
- nonce fresh
- state_version matches
- no dual-active conflict
- ownership authority validated

If any condition fails:

→ Explicit rejection
→ No state mutation

No partial acceptance.

---

# 8. Event Ordering Guarantees

Control-plane messages must obey:

- Monotonic state_version
- Explicit reason codes
- Deterministic mutation order

Out-of-order messages:

→ Rejected if version stale
→ Retried by client with updated version

State cannot move backward.

---

# 9. Observability Independence

Logging and telemetry failures must not:

- Block state transitions
- Affect session binding
- Influence recovery decisions

Observability degrades telemetry —
never correctness.

---

# 10. CAP Tradeoff Position

Jumping VPN prioritizes:

Consistency > Availability > Partition tolerance (under identity ambiguity)

Under partition:

- If ownership cannot be proven,
- If authoritative state cannot be validated,

The system must:

→ Reject reattach
OR
→ Terminate deterministically

Identity safety is higher priority than uptime illusion.

---

# 11. Hard Consistency Guarantees

The system guarantees:

- No dual identity
- No silent identity reset
- No concurrent active transports
- No version rollback
- No ambiguous ownership continuation
- Bounded recovery window
- Explicit termination

---

# 12. Non-Goals

This consistency model does NOT guarantee:

- Global strong consistency across all data-plane traffic
- Distributed transaction semantics beyond session control-plane
- Zero downtime under network partition

It guarantees identity integrity under volatility.

---

# Final Principle

Availability can be recovered.
Identity corruption cannot.

When ambiguity appears,
fail closed.

Session is the anchor.  
Transport is volatile.