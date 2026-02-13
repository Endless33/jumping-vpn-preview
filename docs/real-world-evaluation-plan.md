# Real-World Evaluation Plan — Jumping VPN

Status: Architectural Validation  
Purpose: Controlled Pilot Evaluation  

This document defines how Jumping VPN should be evaluated
in real network environments.

The goal is not marketing validation.
The goal is behavioral verification under transport instability.

---

# 1. Evaluation Objectives

The pilot must validate:

- Deterministic recovery under transport loss
- Bounded recovery time
- No silent session reset
- No dual-active binding
- No identity mutation during failover
- Explicit state transitions
- Auditable event stream

Correctness is more important than uptime.

---

# 2. Target Environments

Recommended pilot scenarios:

- Mobile networks (4G/5G handover)
- Cross-border routing paths
- High-loss Wi-Fi environments
- Fintech session continuity workloads
- Edge deployments with NAT churn

Evaluation should simulate real volatility —
not lab-perfect networks.

---

# 3. Required Network Profiles

Pilot must document:

- Packet loss distribution
- Latency distribution
- Jitter distribution
- NAT mapping timeout behavior
- Route change frequency

Reproducibility requires:

Exact network conditions recorded.

---

# 4. Test Scenarios

## 4.1 Hard Transport Failure

Inject:

Immediate socket close.

Expected:

ATTACHED → RECOVERING → ATTACHED  
Recovery time ≤ MaxRecoveryWindowMs

No session reset.

---

## 4.2 Packet Loss Spike

Inject:

100% loss for N seconds.

Expected:

RECOVERING state
Bounded reattach attempts
Explicit recovery OR termination

No silent corruption.

---

## 4.3 Rapid Flapping

Inject:

Alternating alive/dead states.

Expected:

Switch rate limited
Cooldown enforced
No oscillation loop

---

## 4.4 NAT Churn

Simulate:

Client IP/port change mid-session.

Expected:

Valid reattach
No identity reset
Version incremented
Audit event emitted

---

## 4.5 TTL Expiry

Allow session TTL to expire.

Expected:

ANY → TERMINATED
Reason-coded
No further transitions allowed

---

# 5. Metrics to Collect

For each test:

- Recovery latency (ms)
- Number of reattach attempts
- Switch rate per minute
- State transition timeline
- Termination reason distribution
- Replay rejection count
- Resource usage (CPU, memory)

Metrics must be timestamped.

---

# 6. Success Criteria

A pilot is considered successful if:

- 0 silent identity resets
- 0 dual-active bindings
- 0 version rollbacks
- Recovery bounded and measurable
- All transitions reason-coded
- No infinite recovery loops
- No unbounded memory growth

If any violated → pilot failed.

---

# 7. Failure Handling Policy

If instability exceeds policy:

Expected behavior:

RECOVERING → DEGRADED or TERMINATED

Failure must be:

Explicit
Deterministic
Auditable

Never hidden.

---

# 8. Cluster Evaluation (Optional)

If deployed in cluster:

Test:

- Concurrent reattach race
- Ownership transfer
- CAS correctness
- Split-brain prevention

Consistency > availability.

---

# 9. Evidence Collection

Each pilot must produce:

- Full event stream log
- State transition trace
- Recovery latency distribution
- Failure injection report
- Resource utilization report
- Environment description

All claims must be reproducible.

---

# 10. Comparison Baseline

Optional but recommended:

Run same scenario with:

- Traditional VPN
- QUIC migration
- Static tunnel

Measure:

- Session reset rate
- Identity renegotiation frequency
- Recovery latency

Comparison must use identical network conditions.

---

# 11. Evaluation Deliverables

At end of pilot:

- Summary report
- Metrics appendix
- State timeline graphs
- Resource consumption profile
- Failure case analysis
- Policy recommendations

No marketing language.
Only measured behavior.

---

# 12. What This Plan Does NOT Claim

- No anonymity guarantee
- No censorship bypass guarantee
- No endpoint compromise protection
- No claim of universal superiority

Scope:

Deterministic session continuity under transport volatility.

---

# Final Principle

A protocol must be tested where it is weakest.

Transport instability is not rare.
It is the default condition.

If continuity survives volatility,
the architecture holds.

Session is the anchor.  
Transport is volatile.  
Behavior must be measurable.