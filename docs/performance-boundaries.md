# Performance Boundaries — Jumping VPN

This document defines measurable performance expectations
for Jumping VPN under transport volatility.

It does NOT publish benchmark numbers.
It defines what must be measurable.

---

# 1. Philosophy

Performance is secondary to correctness.

However:

Recovery must be bounded.
State transitions must be fast enough to preserve continuity.
Churn must not cause systemic collapse.

All performance claims must be reproducible.

---

# 2. Core Measurable Dimensions

The system must track:

1) Recovery Latency
2) Switch Rate
3) Session Churn Handling
4) Control-Plane Overhead
5) Replay Protection Cost
6) Memory Bounds per Session

---

# 3. Recovery Latency

Definition:

Time between:
Transport death detection
→ Session returning to ATTACHED

Metric:

recovery_time_ms

Bounded by:

MaxRecoveryWindowMs (policy-defined)

Requirements:

- Must be deterministic.
- Must not exceed policy.
- Must not depend on logging availability.
- Must not block on external telemetry systems.

Recovery exceeding bounds must cause:
RECOVERING → TERMINATED

No indefinite recovery.

---

# 4. Switch Rate Boundaries

Switch frequency must be limited to prevent flapping.

Metric:

switches_per_minute

Constraint:

switches_per_minute <= MaxSwitchesPerMinute

If exceeded:

Session enters DEGRADED
or
Reject further switches until cooldown expires.

Switching must be intentional, not reactive noise.

---

# 5. Session Churn Handling

Definition:

High rate of session creation + termination.

Metrics:

sessions_created_per_second
sessions_terminated_per_second
active_sessions

Constraint:

Session store must maintain:

- O(1) lookup per session
- Bounded memory per session
- TTL-based eviction

Failure to allocate session state must fail closed,
not silently drop invariants.

---

# 6. Control-Plane Overhead

Control-plane must not dominate data-plane.

Measured by:

control_messages_per_second
reattach_requests_per_second
reject_rate

Constraints:

- Rate limiting enforced
- Early rejection of unknown sessions
- Version mismatch rejection before heavy validation

Abuse must not cause O(n²) behavior.

---

# 7. Replay Protection Cost

Replay window must be:

- Bounded memory
- O(1) lookup
- Constant-time validation

Metrics:

replay_window_size
replay_lookup_latency

Replay protection must not scale with packet history unbounded.

---

# 8. Memory Bound per Session

Each session must have bounded structures:

- Replay window
- Candidate transports
- State history (minimal)
- Rate limiter counters

Memory per session must not grow over time.

No append-only unbounded structures allowed.

---

# 9. High-Churn Scenario (10k+ Sessions)

Under high churn:

System must maintain:

- Deterministic eviction
- Bounded recovery windows
- No dual-active binding
- No rollback

Measured dimensions:

- state_transition_latency
- session_lookup_latency
- eviction_time_ms

---

# 10. Degraded Mode Behavior

In DEGRADED state:

- Switch attempts limited
- Candidate exploration constrained
- Stability preferred over adaptation

Performance under DEGRADED must remain stable.

No oscillation loops.

---

# 11. Cluster Performance

If clustered:

- Session ownership lookup must be atomic.
- CAS updates must remain bounded in latency.
- Ownership resolution must not exceed recovery window.

Cluster inconsistency must prefer rejection over delay.

---

# 12. Catastrophic Transport Collapse Scenario

If all transports collapse:

System must:

- Enter RECOVERING immediately
- Respect recovery window
- Terminate deterministically if no candidate

Recovery must not cause:

- Memory leaks
- Unbounded retry loops
- State version rollback

---

# 13. What Is Not Claimed

This document does NOT claim:

- Maximum throughput numbers
- Specific latency benchmarks
- Kernel-level performance optimization
- Line-rate encryption performance

Those require reproducible infrastructure.

---

# 14. Review Requirement

Any performance claim must include:

- Network profile (loss/latency/jitter)
- Session count
- Hardware profile
- Transport type
- Switch frequency
- Replay window size
- TTL settings

Without those, numbers are invalid.

---

# Final Principle

Performance without correctness is irrelevant.

Correctness without bounded performance is unstable.

Jumping VPN requires both.

Session is the anchor.
Transport is volatile.