# Benchmark Plan — Jumping VPN (Architectural Validation)

This document defines how Jumping VPN will be evaluated
under transport volatility conditions.

It is a methodology document.
It does not claim existing performance numbers.

---

## 1. Objective

Validate deterministic session continuity under transport instability.

Primary questions:

- Does the session survive transport death?
- Is recovery bounded?
- Are state transitions explicit and auditable?
- Are switching decisions rate-limited and stable?
- Is identity continuity preserved?

This benchmark plan focuses on **behavioral correctness first,
performance second.**

---

## 2. Scope

This benchmark plan evaluates:

- Control-plane behavior
- Transport death handling
- Reattach latency
- Recovery determinism
- Anti-flap behavior
- Replay handling correctness

This plan does NOT benchmark:

- Encryption throughput
- Kernel-level networking performance
- Hardware offload behavior
- Wire-speed optimization

---

## 3. Test Environment Definition

Every benchmark run must define:

### 3.1 Network Profile

- Packet loss (%)
- Latency (ms)
- Jitter (ms)
- Burst loss pattern
- NAT churn frequency
- Path drop simulation timing

Example profile:

loss = 5% latency = 120ms jitter = 40ms burst_loss = 500ms every 10s nat_rotation = every 60s

---

### 3.2 Session Parameters

- Session TTL
- Transport-loss TTL
- MaxRecoveryWindowMs
- MaxSwitchesPerMinute
- Replay window size
- Cooldown duration

All policy parameters must be logged.

---

## 4. Core Metrics

### 4.1 Recovery Metrics

- `transport_death_events`
- `successful_reattach_count`
- `failed_reattach_count`
- `average_recovery_latency_ms`
- `p95_recovery_latency_ms`
- `max_recovery_latency_ms`

Recovery latency is measured from:

TRANSPORT_DEAD → ATTACHED (post-reattach)

---

### 4.2 Stability Metrics

- `switch_count_per_minute`
- `cooldown_trigger_count`
- `degenerate_loop_detected`
- `oscillation_detected`

System must not exceed:

- configured max switch rate
- bounded recovery attempts

---

### 4.3 Safety Metrics

- `dual_binding_detected` (must be 0)
- `replay_rejected_count`
- `state_version_conflict_count`
- `ambiguous_ownership_detected` (must be 0)
- `silent_reset_detected` (must be 0)

Any non-zero value for invariant violations invalidates test.

---

### 4.4 Degradation Metrics

- `degraded_state_entries`
- `degraded_duration_ms`
- `forced_termination_count`
- `ttl_expiration_count`

Degradation must be explicit.
Termination must be reason-coded.

---

## 5. Failure Injection Scenarios

### Scenario A — Single Transport Death

Trigger:
- Immediate socket drop

Expected:
- RECOVERING state
- REATTACH_REQUEST
- ATTACHED
- No identity reset

---

### Scenario B — Packet Loss Spike

Trigger:
- 30% packet loss for 3 seconds

Expected:
- VOLATILE state
- Possibly DEGRADED
- Bounded switching
- No uncontrolled oscillation

---

### Scenario C — NAT Rebinding

Trigger:
- Client source port change mid-session

Expected:
- Reattach validation
- Fresh binding
- No dual-active transport

---

### Scenario D — Reattach Flood Attempt

Trigger:
- 100 reattach attempts per second

Expected:
- Rate limiter engages
- No uncontrolled switch amplification
- Session integrity preserved

---

### Scenario E — Cluster Split Attempt

Trigger:
- Simulated dual-node reattach acceptance attempt

Expected:
- Single authoritative owner
- One acceptance
- Other rejected deterministically

---

## 6. Scale Targets (Planned)

Future evaluation goals:

- 1k concurrent sessions
- 10k concurrent sessions
- Sustained churn simulation
- High volatility scenario (mobile profile)

No performance claims will be published
without reproducible test conditions.

---

## 7. Evidence Requirements

Every published benchmark must include:

- Full network profile
- Full policy configuration
- Version hash of implementation
- Raw event logs
- Reproducible scripts
- Clear success/failure criteria

No synthetic “marketing numbers.”

---

## 8. Pass Criteria

The benchmark passes if:

- No invariant violation occurs
- No dual-active binding occurs
- No silent session reset occurs
- Recovery latency remains within defined bounds
- Switching stays within configured rate limits

If correctness cannot be guaranteed,
termination must be explicit.

---

## 9. Publication Policy

Results will only be published when:

- Test conditions are reproducible
- Metrics are complete
- Failure cases are documented
- No cherry-picked results are shown

Transparency > marketing.

---

## Final Principle

Benchmarking volatility is not about speed.

It is about bounded correctness under instability.

Session is the anchor.
Transport is volatile.