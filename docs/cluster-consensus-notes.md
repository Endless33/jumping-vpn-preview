# Cluster Consensus Notes — Jumping VPN (Preview)

This document outlines the session ownership and consensus considerations
for clustered deployments of Jumping VPN.

The primary risk addressed here:

Split-brain session ownership and dual-active binding.

---

# 1. Core Cluster Requirement

Clustered deployments MUST guarantee:

- Single authoritative session owner
- No dual-active transport binding
- Deterministic conflict resolution
- Bounded reattach behavior

If these cannot be guaranteed,
the session must terminate explicitly.

---

# 2. Ownership Models

Two supported conceptual models:

## 2.1 Sticky Routing Model

SessionID → Node mapping

- Load balancer routes based on SessionID hash
- Each session is owned by exactly one node
- Reattach must hit the same node

Pros:
- Simpler
- Lower coordination overhead
- High performance

Cons:
- Requires deterministic routing layer
- Less flexible under node churn

---

## 2.2 Shared Atomic Session Store Model

Cluster nodes share authoritative session state:

- CAS (Compare-And-Swap) state updates
- Monotonic state_version enforcement
- Ownership token required for mutation

Rules:

1. Node must acquire ownership before binding transport.
2. Ownership transfer must increment version.
3. If CAS fails → reject reattach.

Pros:
- Horizontal scaling
- Failover resilience
- Node replacement possible

Cons:
- Coordination latency
- Store consistency required

---

# 3. Split-Brain Handling

Scenario:
Two nodes attempt to accept REATTACH_REQUEST simultaneously.

Required behavior:

- Only one CAS succeeds
- Losing node must:
  - Reject reattach
  - Emit ownership conflict event
  - Not mutate session state

Dual acceptance is forbidden.

If ambiguity persists → session TERMINATED.

---

# 4. Failure Modes in Cluster

| Failure | Required Outcome |
|----------|------------------|
| Node crash | Session ownership re-evaluated |
| Store unavailable | Reject reattach (fail closed) |
| Network partition | Reject ambiguous reattach |
| Version conflict | Deterministic reject |
| Ownership token mismatch | Reject + security event |

Correctness > availability.

---

# 5. Version Authority

State transitions require:

- state_version match
- atomic increment
- ownership confirmation

Version rollback is forbidden.

---

# 6. Cluster Safety Invariants

Across cluster:

1. Exactly one authoritative owner per session.
2. At most one active transport per session.
3. No state mutation without version increment.
4. Reattach cannot bypass ownership validation.
5. Ambiguity results in explicit termination.

---

# 7. Recovery After Node Loss

If session owner node crashes:

Two options:

A) Sticky routing:
   - Session unavailable until TTL expires.

B) Shared store:
   - New node attempts ownership acquisition.
   - If successful → RECOVERING.
   - If ambiguous → TERMINATED.

No implicit continuation allowed.

---

# 8. Consensus Philosophy

Jumping VPN prefers:

Consistency over availability.

If cluster cannot prove correctness,
it must refuse continuation.

---

# 9. Deterministic Conflict Rule

In any ownership ambiguity:

Reject > Terminate > Continue

Never:
Continue > Risk dual-active

---

# Final Principle

Cluster safety is stricter than transport survival.

Transport volatility is acceptable.
Ownership ambiguity is not.

Session is the anchor.
Transport is volatile.
Ownership must be singular.