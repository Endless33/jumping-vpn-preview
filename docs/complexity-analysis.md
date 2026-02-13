# Complexity Analysis — Jumping VPN (Preview)

This document outlines the expected implementation and operational complexity
of the Jumping VPN architecture.

The purpose is to make tradeoffs explicit.

This is not a performance benchmark.
It is a structural complexity review.

---

## 1) System Components

The production-oriented architecture consists of:

- Client Agent
- Server Gateway
- Session Ownership Layer
- Policy Engine
- Anti-Replay Module
- Rate Limiter
- Observability Layer

Each component has bounded responsibility.

---

## 2) State Machine Complexity

### States

- BIRTH
- ATTACHED
- VOLATILE
- DEGRADED
- RECOVERING
- TERMINATED

State count: O(1)

Transitions are explicit and reason-coded.

There is no dynamic state explosion.

---

### Transition Complexity

Each transition:

- Validates invariants
- Validates policy bounds
- Increments state_version
- Emits observability event

Cost per transition: O(1)

No unbounded recursion.
No implicit loops.

---

## 3) Session Table Complexity

### Per-Session Memory

Expected per-session state:

- session_id
- state
- state_version
- active_transport
- TTL timestamps
- anti-replay window
- switch counters

All bounded.

Replay window is sliding and capped.

Memory per session: O(1)

---

### Lookup Complexity

Session retrieval:

- Hash map lookup
- Keyed by session_id

Expected complexity: O(1)

No full-table scans required for control-plane operations.

---

## 4) Anti-Replay Window

Replay protection model:

- Monotonic client nonce
- Bounded window storage
- Reject stale / reused nonces

Operations:

- insert
- membership check
- eviction

All O(1) using hash structures.

Window size must be bounded by configuration.

---

## 5) Rate Limiting

Switch and reattach rate limits:

- Token bucket or sliding window
- Per-session counters
- Optional per-IP guard

Operations:

- increment
- check
- reset

O(1) per evaluation.

---

## 6) Reattach Validation Cost

Server-side validation:

- Session existence check → O(1)
- TTL check → O(1)
- Version check → O(1)
- Anti-replay check → O(1)
- Proof validation → dependent on crypto primitive
- Ownership CAS → O(1) with atomic store

Total complexity per reattach: O(1) + crypto verification

No graph traversal.
No global coordination required (if sticky routing used).

---

## 7) Cluster Complexity

Two main models:

### Sticky Routing

- SessionID → Node mapping
- No cross-node coordination during reattach

Complexity: minimal

Tradeoff:
Requires deterministic routing layer.

---

### Shared Atomic Store

- Versioned session records
- CAS-based ownership transfer
- Requires consistency guarantees

Complexity increases:

- External dependency (KV store)
- Network RTT to shared store
- Failure-handling logic

Still bounded per operation.

---

## 8) Control-Plane vs Data-Plane Separation

Control-plane:

- Low-frequency events
- State transitions
- Recovery logic

Data-plane:

- High-throughput encrypted packets
- Not defined in this preview

Complexity isolation is intentional.

Control-plane correctness does not scale with packet volume.

---

## 9) Worst-Case Behavior

Worst-case scenario:

- High churn
- Reattach floods
- Malicious nonce replay attempts
- Rapid transport oscillation

Mitigations:

- Rate limiting
- Cooldown windows
- Replay window bounds
- Early rejection
- Deterministic termination

System degrades safely.
It does not enter unbounded loops.

---

## 10) Performance Scaling Considerations

At 10k+ sessions:

- Memory remains linear O(n)
- Per-session operations remain O(1)
- Replay window bounded
- Switch counters bounded

No algorithmic amplification factors identified.

Real-world performance depends on:

- Crypto cost
- Store latency (if clustered)
- Network RTT
- Logging overhead (non-blocking)

---

## 11) Operational Complexity

The architecture increases:

- Implementation complexity (state machine + invariants)
- Policy definition responsibility
- Observability requirements

It decreases:

- Hidden recovery behavior
- Ambiguous migration logic
- Implicit transport coupling

This is a deliberate tradeoff.

Determinism requires structure.

---

## 12) Summary

Algorithmic Complexity:
- Per-session: O(1)
- Lookup: O(1)
- Reattach: O(1) + crypto
- Replay window: O(1)
- Rate limiting: O(1)

Systemic Complexity:
- Moderate (due to invariant enforcement)
- Higher than naive VPN designs
- Lower than distributed consensus systems

Jumping VPN trades simplicity of implementation
for clarity of behavior.

Correctness is prioritized over convenience.

---

Session is the anchor.  
Transport is volatile.