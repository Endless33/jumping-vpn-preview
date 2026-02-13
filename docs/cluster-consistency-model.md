# Cluster Consistency Model — Jumping VPN (Preview)

This document defines how session ownership is handled in clustered deployments.

The goal:

Prevent dual-active session binding under transport reattach.

---

# 1. Problem Definition

In a clustered deployment:

- Multiple nodes may receive REATTACH_REQUEST
- Network partitions may occur
- State synchronization may lag

Without a strict ownership model,
split-brain continuation becomes possible.

This is forbidden.

---

# 2. Core Principle

Session ownership must be authoritative.

At any moment:

Only one node may be the session owner.

---

# 3. Ownership Models (Supported Patterns)

## Model A — Sticky Routing

- All packets for a session are routed to the same node
- Load balancer enforces consistent hashing
- No cross-node ambiguity

Pros:
- Simple
- Deterministic

Cons:
- Less flexible under failover

---

## Model B — Centralized State Store

- Session state stored in authoritative database
- Versioned CAS (Compare-And-Swap) updates
- Reattach requires atomic state update

Required properties:

- Monotonic version counter
- Strict write conflict detection
- No last-write-wins ambiguity

Pros:
- Scales horizontally
- Supports dynamic reassignment

Cons:
- Requires strong consistency guarantees

---

# 4. Split-Brain Handling

If two nodes attempt ownership:

- Only one atomic CAS succeeds
- The loser must reject reattach
- An AUDIT_EVENT must be emitted

Dual-active continuation is forbidden.

---

# 5. Failure Semantics

If cluster communication fails:

- Consistency is preferred over availability
- Ambiguous continuation is rejected
- Explicit TERMINATED is safer than dual-binding

---

# 6. Hard Guarantees

G1 — At most one active owner per session

G2 — Reattach is atomic

G3 — Split-brain results in rejection, not duplication

G4 — No undefined ownership state

---

# 7. Non-Goals

This document does not define:

- Specific database choice
- Specific consensus algorithm
- Exact replication strategy

It defines ownership invariants only.

---

# 8. Design Philosophy

Under ambiguity:

Terminate rather than duplicate.

Consistency over silent divergence.

---

Session continuity must not compromise correctness.