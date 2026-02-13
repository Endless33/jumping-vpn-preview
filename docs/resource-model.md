# Resource Model — Jumping VPN

Status: Architectural Validation  
Scope: Control-plane + session-layer resource modeling  

This document describes the expected resource characteristics
of a production-grade Jumping VPN implementation.

It focuses on:

- Per-session state cost
- Memory bounds
- CPU characteristics
- Replay window storage
- Switch-rate tracking
- Cluster overhead

The goal is bounded, predictable resource behavior.

---

# 1. Design Constraint

The control-plane must scale linearly with the number of sessions.

No per-packet heavy control-plane work.
No unbounded memory structures.
No hidden growth vectors.

Bounded structures only.

---

# 2. Per-Session State Model

Each session minimally contains:

- SessionID (string / UUID)
- state (enum)
- state_version (int)
- active_transport (struct)
- candidate_transports (bounded list)
- policy snapshot (struct)
- replay window (bounded)
- last_switch_timestamp
- switch_counter (per window)
- TTL timestamps

---

# 3. Memory Footprint Estimation

## 3.1 Baseline Per Session

Estimated control-plane state:

Session metadata: ~128 bytes  
Transport info: ~128 bytes  
Policy struct: ~128 bytes  
Replay window (bounded set): ~512 bytes  
Switch tracking / timestamps: ~128 bytes  

Approximate total:

~1–2 KB per active session (control-plane only)

This excludes data-plane encryption buffers.

---

## 3.2 Replay Window Bound

Replay window must be:

- Fixed size
- Sliding
- Time-bounded

Example:

Replay window size: 64–256 entries  
Memory cost per entry: ~16–32 bytes  

Total: ~1–8 KB worst-case per session if misconfigured.

Must be capped.

---

# 4. CPU Characteristics

## 4.1 Normal Operation

CPU cost primarily occurs during:

- Initial handshake
- Reattach validation
- State transitions
- Policy evaluation
- Logging

No control-plane cost per packet during stable ATTACHED state.

---

## 4.2 Reattach Path Cost

Operations:

- Proof-of-possession verification
- Replay window check
- Version check
- Session table CAS update
- Logging event

All O(1) operations per reattach attempt.

No linear scans allowed.

---

# 5. Session Table Scalability

Expected lookup pattern:

SessionID → direct map lookup (hash map / KV store)

Time complexity:

O(1) average

Clustered model:

SessionID → ownership mapping → node routing

Must avoid:

- broadcast-based resolution
- multi-node scanning

---

# 6. Switch Rate Tracking

Per session:

- counter
- sliding window start timestamp

Memory cost: constant

Switch logic must not depend on global counters.

---

# 7. Cluster Model Overhead

Two supported strategies:

## 7.1 Sticky Routing

Pros:
- No distributed lock needed
- Low latency

Cons:
- Node failure migration required

## 7.2 Shared Store (CAS-based)

Pros:
- Explicit authority
- Safe reattach under redistribution

Cons:
- Write amplification
- External store dependency

Session store must support:

- atomic compare-and-swap
- version increment
- TTL expiration

---

# 8. Worst-Case Volatility Scenario

High churn example:

10,000 sessions  
10% enter RECOVERING simultaneously  
Average 2 reattach attempts  

Control-plane events:

~2,000 reattach validations  
All O(1) operations  

System must avoid:

- global locks
- per-session blocking IO
- synchronized logging flush

---

# 9. Logging Overhead

Observability must be:

- Non-blocking
- Buffered
- Drop-tolerant

Logging failure must not:

- stall state transition
- delay CAS
- prevent termination

Telemetry degradation must not break correctness.

---

# 10. Boundedness Guarantees

The implementation must guarantee:

- Replay window bounded
- Candidate transport list bounded
- Switch attempts bounded
- Recovery time bounded
- Session TTL bounded

Unbounded growth = design failure.

---

# 11. High-Level Capacity Estimate (Control-Plane Only)

Example target:

10k sessions  
2 KB per session  

Control-plane memory:
~20 MB

This is feasible on modest hardware.

Data-plane encryption buffers excluded from this model.

---

# 12. Future Work

To be measured empirically:

- CPU per reattach under load
- CAS contention under cluster race
- Replay window performance under attack
- Switch-rate enforcement accuracy

See:

docs/benchmark-plan.md  
docs/evidence-log.md  

---

# Engineering Principle

Resilience is useless if it collapses under scale.

Resource cost must be:

Predictable  
Bounded  
Linear  

Session is the anchor.  
Transport is volatile.  
Resource growth must never be.