# Jumping VPN — Distributed Consistency Model

Status: Architectural Consistency Definition (Public Preview)

This document defines how session state consistency
is maintained in distributed deployments.

Jumping VPN is session-centric.
Session identity must never split.

---

# 1. Core Problem

In clustered environments:

- Multiple server nodes may exist.
- Transport reattach may hit different nodes.
- Network partitions may occur.

Without coordination,
split-brain session identity is possible.

This document defines constraints to prevent it.

---

# 2. Consistency Goals

The system must guarantee:

1. At most one active binding per session.
2. No concurrent valid reattach on separate nodes.
3. Deterministic termination over inconsistent continuation.
4. No silent state divergence.

---

# 3. Deployment Models

## 3.1 Single Node

Simplest model.

- Session table is local.
- Strong consistency guaranteed by process isolation.

No distributed concerns.

---

## 3.2 Sticky Routing

SessionID → Node mapping.

- Load balancer routes same session to same node.
- No shared session store required.

Risk:

- Node failure loses session unless replication exists.

---

## 3.3 Shared Session Store

All nodes access centralized store.

Requirements:

- Atomic session update
- Compare-and-swap semantics
- Versioned state transitions

Risk:

- Store availability becomes critical dependency.

---

## 3.4 Sharded Session Model

SessionID hashed to shard.

Each shard authoritative for its sessions.

Requires:

- Deterministic shard mapping
- Consistent hashing
- No cross-shard mutation

---

# 4. Reattach in Cluster

Reattach must follow:

1. Lookup session by ID.
2. Verify authoritative ownership.
3. Perform atomic state update.
4. Reject stale reattach attempts.

If state version mismatch:

→ Reattach denied.

---

# 5. Versioned State Updates

Each session record SHOULD include:

state_version: integer

On update:

- Read current version
- Apply transition if version matches
- Increment version
- Write atomically

If version mismatch:

→ Abort transition.

Prevents race conditions.

---

# 6. Network Partition Behavior

If cluster partition occurs:

Preferred strategy:

- Conservative termination over inconsistent continuation.

If authoritative node unreachable:

- Reattach MUST fail.
- Session MAY degrade.
- TTL eventually triggers termination.

Consistency > availability.

---

# 7. Split-Brain Prevention

Split-brain occurs if:

- Two nodes accept valid reattach
- Both mark different active transports

This must be prevented via:

- Central coordination
OR
- Sticky routing
OR
- Versioned atomic updates

Never allow dual active binding.

---

# 8. Failure Priority Rule

When inconsistency detected:

The system MUST prefer:

1. Explicit termination
over
2. Undefined dual-state continuation.

Deterministic failure is safer than silent corruption.

---

# 9. Observability Requirements

Clustered deployments MUST log:

- Node ID
- Session version
- State transitions
- Reattach attempts
- Conflict resolution events

Audit must reconstruct:

- Which node accepted binding
- When
- Under which version

---

# 10. Design Philosophy

Distributed systems fail at boundaries.

Jumping VPN must:

- Prefer explicit termination
- Avoid dual active identity
- Enforce atomic state mutation
- Reject ambiguous reattach

Session identity is sacred.

It must never fork.