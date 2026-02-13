# Performance Model — Jumping VPN (Architectural Estimate)

This document describes the expected performance characteristics
of a production-oriented Jumping VPN implementation.

No benchmark numbers are claimed here.
This is a complexity and resource model.

---

# 1) Design Philosophy

Performance must be:

- Bounded
- Predictable
- Proportional to session count
- Independent of transport volatility spikes

Control-plane must not scale per-packet.
It scales per-session event.

---

# 2) Control Plane Complexity

## 2.1 Session Table Operations

Lookup by session_id:
Expected complexity: O(1) (hash map)

State update:
O(1)

Version increment:
O(1)

Ownership CAS (clustered):
O(1) expected (atomic store op)

---

## 2.2 Transport Switch Operation

Switch event includes:

- validation
- ownership check
- version increment
- active_transport update
- audit emit

Expected complexity per switch:
O(1)

Switch cost must not depend on total session count.

---

## 2.3 Replay Window Tracking

Replay window tracking per session:

Structure:
- bounded sliding window
- sequence tracking or timestamp bucket

Memory per session:
O(W)

Where W = replay window size (bounded by policy)

Replay verification:
O(1) expected

---

# 3) Data Plane Expectations

Data-plane encryption and packet forwarding:

Must not require global locks.
Must not depend on session table iteration.

Per-packet work:

- session lookup (O(1))
- key usage (O(1))
- replay check (O(1))
- forward

Target:
Constant-time per packet under steady state.

---

# 4) Memory Model

Let:

N = number of active sessions
W = replay window size
C = average candidate transports per session (bounded)

Memory ≈

N * (
    session_struct +
    replay_window(W) +
    candidate_set(C)
)

All components must be bounded by policy.

No unbounded growth allowed.

---

# 5) Volatility Spike Handling

Worst case scenario:

Many transports fail simultaneously.

Behavioral requirements:

- Switch attempts bounded by policy
- Control-plane rate limiting enforced
- Recovery windows finite
- No per-packet control-plane escalation

Even under churn:

CPU must scale with number of sessions affected,
not with total packet rate.

---

# 6) Anti-Flap Cost Control

Switch rate limit:

MaxSwitchesPerMinute (policy-bound)

Switch attempt rejected early if:

switch_count > limit

This ensures:

Switch cost is capped per session.

---

# 7) Cluster Scaling Model

Two deployment models:

## 7.1 Sticky Routing Model

SessionID -> Node mapping

Pros:
- Minimal coordination
- O(1) session ownership lookup

Cons:
- Load distribution tied to hashing

---

## 7.2 Shared State Store (CAS)

Atomic versioned ownership update.

Expected cost:
O(1) per transition

Critical requirement:
Low-latency store
Bounded session state

---

# 8) 10k+ Session Scenario

Assume:

N = 10,000 sessions
W = bounded replay window
C <= 3 candidate transports

Expected properties:

- Session lookup remains O(1)
- Replay verification O(1)
- Switch rate bounded
- No global lock required

Control-plane must remain proportional to number of active sessions,
not number of packets.

---

# 9) Failure Isolation

If observability pipeline fails:

- Logging must degrade
- Session correctness must not degrade

Observability must be non-blocking.

---

# 10) Performance Non-Claims

This document does NOT claim:

- Throughput numbers
- Latency numbers
- Memory footprint metrics
- Crypto benchmark results

Those require reproducible test environments.

---

# 11) Benchmark Readiness

Before publishing numbers:

Must define:

- network profile (loss, jitter, churn)
- hardware spec
- OS
- concurrency model
- transport protocol

Only reproducible benchmarks are valid.

---

# 12) Engineering Goal

Target characteristics:

- O(1) session lookup
- O(1) switch
- O(1) replay validation
- Bounded memory per session
- No unbounded adaptation loops

Determinism before performance.
Predictability before optimization.

---

Session is the anchor.
Transport is volatile.
Performance must be bounded.