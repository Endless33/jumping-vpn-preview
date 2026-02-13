# Scalability Model — Session Continuity Under High Churn (Preview)

This document describes how Jumping VPN scales
under high session counts and high transport volatility.

The focus is control-plane scalability,
not data-plane throughput.

---

# 1. Design Goal

Maintain deterministic session continuity under:

- 10k+ concurrent sessions
- high packet loss environments
- frequent transport churn
- reattach bursts
- NAT rebinding
- mobile network volatility

The control-plane must scale without:

- unbounded memory growth
- O(n) lookup bottlenecks
- uncontrolled switching storms
- state corruption

---

# 2. Scalability Principles

Jumping VPN is designed around:

- Bounded per-session state
- O(1) lookup structures
- Versioned mutation
- Stateless transport adapters
- Deterministic rate limiting

The system scales by isolating sessions,
not by sharing mutable global state.

---

# 3. Per-Session State Boundaries

Each session maintains only:

- SessionID
- State (enum)
- state_version (int)
- Active transport reference
- Replay window (bounded)
- Switch counter (rolling window)
- TTL timers
- Policy snapshot

No session stores unbounded history.

Audit logs are externalized.

---

# 4. Time & Space Complexity Targets

## Lookup Complexity

Session lookup:

O(1) average
via hash map keyed by SessionID

Ownership validation:

O(1) per reattach

Replay window validation:

O(1) using bounded sliding window

---

## Memory Complexity

Memory grows linearly with session count:

O(n_sessions)

Bounded by:

- max sessions allowed
- TTL eviction
- idle cleanup policy

No global broadcast state.

---

# 5. High-Churn Behavior

High churn scenario:

- Frequent transport death
- Frequent reattach
- Flapping networks

Protection mechanisms:

- Rate-limited switching
- Cooldown windows
- Recovery window bounds
- Hard TTL enforcement
- Replay window pruning

If churn exceeds policy bounds:

Session enters DEGRADED
or
Session TERMINATED

Scalability is preserved by bounding recovery.

---

# 6. Reattach Storm Handling

Worst case:
Many clients attempt reattach simultaneously.

Mitigations:

- Per-session rate limiter
- Global rate limiter
- Early rejection for unknown sessions
- Proof validation before heavy mutation
- Stateless rejection path

Server must:

- Reject fast
- Avoid expensive state mutation before validation
- Avoid lock contention

---

# 7. Locking Strategy (Conceptual)

Per-session locking only.

Never global lock for all sessions.

Possible models:

- Fine-grained mutex per session
- Version-based CAS (lock-free optimistic)
- Sharded session table

Avoid:

- Global control-plane mutex
- Cross-session blocking operations

Isolation enables horizontal scaling.

---

# 8. Cluster Scaling Model

Two primary models:

## Sticky Routing

SessionID → consistent-hash load balancer

Benefits:
- No cross-node sync
- High throughput
- Simpler consistency

Tradeoff:
- Rebalancing complexity

---

## Shared Atomic Store

Distributed store (e.g., Redis + CAS, etcd, custom store)

Requires:

- Versioned writes
- Ownership record
- Conflict rejection

Cost:
- Higher latency
- More operational complexity

Guarantee:
- Single authoritative owner

---

# 9. Control-Plane Throughput Constraints

Control-plane work per event must be bounded.

Operations per reattach:

- Session lookup
- TTL validation
- Replay window validation
- Version match
- Ownership check
- State transition
- Audit emit

All must remain O(1) relative to total sessions.

---

# 10. Scaling Anti-Replay

Replay windows must:

- Be bounded in size
- Evict oldest entries
- Use fixed-size structure

Memory must not scale with total nonce history.

Suggested model:

Sliding window with bounded buffer.

---

# 11. Observability Scalability

Logging must be:

- Asynchronous
- Non-blocking
- Backpressure-aware

Logging failure must not block control-plane.

Export mechanisms:

- Buffered channel
- Async flush
- Rate limiting

Telemetry must degrade safely.

---

# 12. Failure Isolation

A single unstable session must not:

- Block others
- Lock global structures
- Cause cascading failure

Isolation rule:

Sessions are independent units of mutation.

No cross-session side effects allowed.

---

# 13. Theoretical Scaling Bound

Scalability is limited by:

- Session count
- Reattach frequency
- Policy thresholds
- Control-plane CPU budget

It is not limited by:

- Transport churn alone
- Logging rate
- Candidate path count (bounded)

The architecture ensures bounded work per mutation.

---

# 14. What Is Not Claimed

This document does NOT claim:

- Proven 100k+ production performance
- Measured throughput numbers
- Kernel-level optimization
- Zero-copy packet handling
- Data-plane performance metrics

Scalability model focuses on control-plane determinism.

Benchmarks are defined separately.

---

# 15. Production Scaling Requirements

Before claiming production readiness:

- Load tests at 10k+ sessions
- Reattach storm simulation
- Partition testing
- Memory leak verification
- Replay window stress test
- Rate limiter abuse test

Scalability must be measured, not assumed.

---

# Final Principle

Scale by bounding behavior.

If recovery is unbounded,
scalability collapses.

If identity safety is unbounded,
correctness collapses.

Jumping VPN bounds both.

Session is the anchor.  
Transport is volatile.