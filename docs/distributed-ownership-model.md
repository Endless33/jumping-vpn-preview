# Distributed Ownership Model (Preview)

Status: Architectural Design  
Scope: Cluster-safe session ownership under transport volatility  

This document defines how session ownership is handled
in a distributed / multi-node deployment.

Core rule:

A session must have exactly one authoritative owner at any time.

No ambiguity.
No dual-active continuation.

---

# 1. Problem Statement

In a clustered deployment:

- Multiple gateway nodes may receive REATTACH_REQUEST.
- Network partitions may occur.
- Concurrent reattach attempts may happen.
- Sticky routing may fail.

Without strict ownership enforcement,
dual-active session binding becomes possible.

This violates core invariants.

---

# 2. Ownership Invariant

For any given session_id:

There must exist at most one active authoritative node.

Formally:

∀ session_id:
count(active_owner_nodes) ≤ 1

If ambiguity is detected:
the session must reject continuation.

Correctness > availability.

---

# 3. Ownership Strategies

Three candidate models:

---

## 3.1 Sticky Routing (SessionID → Node)

Mechanism:

- Load balancer hashes SessionID
- All control-plane traffic routed to the same node
- No shared session store required

Pros:

- Low latency
- Simpler state model
- No distributed consensus

Cons:

- LB must be consistent
- Fails if routing layer misbehaves
- Node failure requires reassignment logic

---

## 3.2 Centralized Authoritative Store

Mechanism:

- Shared session store (Redis / SQL / etc.)
- Each state transition uses atomic CAS (compare-and-swap)
- state_version increments on success

Ownership rule:

Only node that successfully CAS-updates ownership
becomes authoritative.

Pros:

- Strong correctness
- No dual-active binding
- Explicit ownership semantics

Cons:

- External dependency
- Latency overhead
- Requires atomic guarantees

---

## 3.3 Lease-Based Ownership

Mechanism:

- Ownership granted with short TTL lease
- Node must periodically renew lease
- Expired lease allows safe reassignment

Requirements:

- Monotonic lease IDs
- Strict version checks
- Lease expiration must be deterministic

Pros:

- Scalable
- Partition-tolerant (bounded)

Cons:

- Requires careful timing bounds
- Lease race conditions must be modeled formally

---

# 4. Ownership Transfer Protocol (Abstract)

Case: Node A crashes during RECOVERING.

1. Lease expires OR heartbeat fails
2. Node B attempts CAS acquire
3. If CAS succeeds → ownership transfers
4. state_version increments
5. All future reattach must reference new version

No implicit transfer allowed.

---

# 5. Split-Brain Handling

If two nodes believe they own a session:

This is a violation condition.

Required action:

- Reject further reattach
- Emit SECURITY_EVENT
- Optionally terminate session

Ambiguous continuation is forbidden.

---

# 6. State Version Enforcement

Every ownership mutation must:

- Check current state_version
- Increment version on success
- Reject stale version writes

No node may:

- Write without CAS
- Accept reattach on stale version
- Override ownership without version match

Version monotonicity prevents rollback.

---

# 7. Ownership Under Network Partition

Partition scenarios:

1. Partition between gateway and store
2. Partition between two gateways
3. Partial cluster split

Policy:

- Prefer fail-closed
- Reject ambiguous reattach
- Do not allow speculative continuation

Availability must never override correctness.

---

# 8. Failure Matrix

Condition | Action
----------|-------
Node crash | Lease expiry → reassign
Store unavailable | Reject reattach (fail closed)
Concurrent CAS | Only one succeeds
Replay reattach | Reject without mutation
Ambiguous ownership | Reject or terminate

---

# 9. Observability Requirements

Every ownership event must emit:

- SESSION_OWNER_ACQUIRED
- SESSION_OWNER_TRANSFERRED
- SESSION_OWNER_REJECTED
- SESSION_OWNER_CONFLICT

Audit must allow:

- Reconstruction of ownership timeline
- Detection of anomaly
- Postmortem analysis

---

# 10. Hard Safety Rules

The distributed model must guarantee:

- No dual-active binding
- No silent ownership transfer
- No implicit failover
- Deterministic resolution of contention
- Explicit rejection on ambiguity

---

# 11. Future Work

Formal modeling (TLA+ recommended) should include:

- Concurrent reattach attempts
- Lease expiration races
- Partition recovery
- Version rollback prevention
- CAS conflict resolution

Correctness must be proven, not assumed.

---

# Final Principle

A distributed system that cannot prove ownership correctness
must prefer termination over ambiguity.

Session is the anchor.  
Transport is volatile.  
Ownership must be singular.