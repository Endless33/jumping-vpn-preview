# Jumping VPN — Session Table Model

Status: Normative State Storage Model (Public Preview)

This document defines the internal logical structure
of the Session Table used by Jumping VPN.

It describes:

- Session state structure
- Transport bindings
- Lifecycle constraints
- Consistency requirements

Cryptographic details are abstracted.

---

# 1. Session Table Purpose

The Session Table is the authoritative source of truth
for all active sessions.

It must:

- Maintain bounded state
- Enforce lifecycle constraints
- Prevent split-brain
- Guarantee deterministic transitions

---

# 2. Session Record Structure (Logical)

Each session record contains:

{
  session_id,
  state,
  created_at_ms,
  last_state_change_ms,
  session_ttl_ms,
  active_transport,
  candidate_transports[],
  switch_counter_window,
  recovery_deadline_ms,
  degradation_flag,
  security_context_ref,
  policy_ref
}

---

# 3. Field Semantics

## session_id
Unique identifier.
Must be unguessable.
Lookup key for session retrieval.

---

## state
Current FSM state.
Must conform to formal-state-machine.md.

---

## active_transport
Single active transport binding.

Invariant:
ATTACHED implies active_transport != null.

---

## candidate_transports[]
Bounded list of possible transport bindings.

Constraint:
Size MUST be bounded by policy.

---

## switch_counter_window
Tracks switch rate for MAX_SWITCHES_PER_MIN enforcement.

Must:

- Be sliding window
- Reset deterministically
- Prevent unbounded growth

---

## recovery_deadline_ms
Defines RECOVERY_WINDOW_MS boundary.

If current_time > recovery_deadline_ms:
RECOVERING → DEGRADED or TERMINATED.

---

## degradation_flag
Indicates degraded state due to:

- Switch rate limit
- Sustained instability
- Recovery exhaustion

---

## security_context_ref
Reference to cryptographic material.
Actual keys not stored directly in session logic layer.

---

## policy_ref
Pointer to policy configuration.

Defines:

- TTL
- thresholds
- switch limits
- allowed transport types

---

# 4. Session Lifecycle Constraints

## 4.1 Bounded Growth

The Session Table must:

- Remove TERMINATED sessions
- Evict expired sessions
- Prevent unbounded accumulation

---

## 4.2 Atomic State Updates

All transitions must be:

- Atomic
- Versioned (optional but recommended)
- Logged

Partial updates forbidden.

---

## 4.3 No Dual Active Binding

Invariant:

At any time,
a session MUST have:

- Zero active transports (VOLATILE/DEGRADED)
- OR exactly one active transport (ATTACHED)

Never more than one.

---

# 5. Split-Brain Prevention

In clustered deployment:

Session lookup must ensure:

- Single authoritative owner
OR
- Consistent shared storage

Reattach must validate against latest state version.

Stale state must be rejected.

---

# 6. Expiration & Cleanup

A session must be removed if:

- state == TERMINATED
- session_ttl_ms exceeded
- transportless TTL exceeded

Cleanup must:

- Release memory
- Invalidate security context
- Emit termination log

---

# 7. Horizontal Scaling Considerations

If deployed across nodes:

Options:

- Sticky routing
- Shared distributed store
- Session shard by session_id hash

Requirement:

No two nodes may accept valid reattach
for same session concurrently.

---

# 8. Consistency Model

Session consistency must be:

- Strong within single node
- Bounded eventual consistency in cluster

Under cluster partition:

- Conservative termination preferred over split identity.

---

# 9. Failure Safety

Session Table must ensure:

- Corrupted entry cannot remain ATTACHED silently
- Invalid transitions rejected
- Memory exhaustion mitigated

---

# 10. Design Principle

The Session Table is not a cache.

It is the identity anchor.

Transport volatility must never
corrupt session identity state.