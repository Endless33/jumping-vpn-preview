# Consensus & Ownership Model — Jumping VPN (Preview)

This document defines how session ownership is established,
transferred, and protected in clustered deployments.

Single-session identity must never become dual-active.

Safety > Availability.

---

# 1. Core Ownership Principle

At any time:

A session MUST have exactly one authoritative owner.

Owner responsibilities:

- Validate reattach
- Enforce TTL
- Increment state_version
- Bind active transport
- Emit audit events

Dual ownership is forbidden.

---

# 2. Ownership Strategies

Two supported models:

## 2.1 Sticky Routing (Deterministic Mapping)

SessionID → Node

All traffic for a session is routed to one node.

Advantages:
- Simpler implementation
- No distributed CAS required

Tradeoff:
- Requires L4/L7 routing consistency

---

## 2.2 Shared Atomic Store (Clustered Model)

All nodes share a central authoritative session store.

Requirements:

- Compare-And-Swap (CAS)
- Monotonic version counter
- Transactional ownership update
- Strict write serialization

No last-write-wins.

---

# 3. Ownership Transfer

Ownership transfer allowed only via:

- Controlled migration
- Node shutdown drain
- Explicit failover procedure

Transfer steps:

1. Freeze session (no new transport binding)
2. Commit state_version increment
3. Transfer ownership marker
4. Resume ATTACHED state

No silent transfer.

---

# 4. Split-Brain Scenario

If two nodes attempt reattach:

Only one CAS succeeds.

The other must reject with:

REATTACH_REJECT (OWNERSHIP_CONFLICT)

Ambiguity is not tolerated.

---

# 5. Network Partition

If cluster partition occurs:

Option A:
Deny reattach until consensus restored.

Option B:
Terminate sessions deterministically.

Never:
Allow continuation on both sides.

---

# 6. Version Semantics in Cluster

Every state transition:

- Must increment state_version
- Must reject stale updates
- Must verify expected version

If:

incoming_version != stored_version

Reject.

No rollback allowed.

---

# 7. Failure Handling Rules

If store unavailable:

- Fail closed
- Reject reattach
- Do not mutate session

If partial write occurs:

- Abort transition
- Emit SECURITY_EVENT

Atomicity is mandatory.

---

# 8. Safety Invariants

The cluster must preserve:

- No dual-active binding
- Monotonic state_version
- Deterministic rejection
- Explicit termination on ambiguity

---

# 9. Operational Implications

Cluster design must:

- Prefer consistency over availability
- Log all ownership changes
- Provide audit visibility
- Enforce strict TTL expiration

---

# 10. What This Is Not

This document does NOT:

- Define a full distributed consensus algorithm
- Replace Raft/Paxos
- Guarantee availability under full partition

It defines ownership boundaries for session safety.

---

# Final Principle

Session identity cannot be forked.

If ownership cannot be proven,
continuation must be denied.

Continuity without authority is corruption.

Session is the anchor.
Transport is volatile.
Ownership is singular.