# Jumping VPN — Benchmark & Evaluation Plan

Status: Evaluation Methodology (Public Preview)

This document defines how Jumping VPN behavior
should be measured under controlled test conditions.

No performance numbers are claimed in this repository.
This document defines how they will be obtained.

---

# 1. Objectives

Measure:

- Transport failover latency
- Session continuity behavior
- Switch frequency under volatility
- Recovery determinism
- Resource overhead during volatility
- Replay handling stability

Benchmarking focuses on behavior, not marketing metrics.

---

# 2. Test Scenarios

## 2.1 Clean Failover

Condition:
- Primary transport terminated manually
- Backup transport available

Measure:
- Time to detect transport death
- Time to switch
- Time to ATTACHED state restoration
- Whether session identity preserved

Expected:
- No renegotiation
- No session reset
- Explicit TransportSwitch event

---

## 2.2 Packet Loss Spike

Condition:
- 20–40% packet loss injected
- Increased latency

Measure:
- Transition ATTACHED → VOLATILE
- Switch trigger timing
- Recovery time
- Number of switch attempts
- DEGRADED entry threshold

---

## 2.3 NAT Rebinding Simulation

Condition:
- Client IP changes
- NAT mapping expires

Measure:
- Reattach success rate
- Reattach latency
- Replay rejection accuracy
- False positive rate

---

## 2.4 Switch Rate Stress

Condition:
- Induced flapping environment
- Repeated short-term packet drops

Measure:
- Switch attempts per minute
- Switch denials due to rate limit
- State stability
- Oscillation prevention effectiveness

---

## 2.5 Replay Flood Test

Condition:
- Repeated reattach with identical freshness markers

Measure:
- Replay detection latency
- CPU overhead
- Replay cache stability
- Session integrity preservation

---

# 3. Metrics Definition

All metrics must be recorded in structured JSON.

Required fields:

- ts_ms
- session_id
- state
- transport_id
- event_type
- latency_ms (if applicable)
- switch_count
- replay_detected_count

---

# 4. Measurement Environment (Abstract)

Benchmarks should specify:

- Network emulator (tc/netem or equivalent)
- Packet loss rate
- Latency distribution
- Jitter range
- Hardware profile
- CPU cores
- Memory constraints

Environment must be documented for reproducibility.

---

# 5. Evaluation Criteria

Success criteria include:

- No silent session reset during failover
- No dual-active transport binding
- Switch bounded by policy
- Replay attempts rejected deterministically
- RECOVERING state bounded in time

Failure conditions must be logged.

---

# 6. Reporting Format

Benchmark results should include:

- Test scenario name
- Network conditions
- Observed transitions
- Time to recovery
- Policy configuration used
- Notes on anomalies

Results must avoid:

- cherry-picked samples
- unbounded averages
- undefined environment claims

---

# 7. Non-Goals

This benchmark plan does NOT:

- claim production throughput
- compare against specific vendors
- provide marketing claims
- assert universal superiority

It defines behavioral evaluation methodology.

---

# Final Statement

Jumping VPN is evaluated on:

- deterministic recovery
- bounded adaptation
- explicit state transitions
- identity integrity under volatility

Benchmarks validate behavior —
not hype.