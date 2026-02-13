# Benchmark Plan — Jumping VPN (Preview)

This document defines how performance and recovery behavior
should be measured for Jumping VPN.

No performance claims are made in this repository.
This is a structured evaluation plan.

---

## 1) Purpose

The goal of benchmarking is to measure:

- Recovery latency after transport death
- Session continuity correctness
- Switch stability under churn
- Control-plane resilience
- Resource cost per active session

The benchmark must validate behavioral guarantees,
not just throughput numbers.

---

## 2) Test Environment Requirements

All results must specify:

- CPU model
- Core count
- RAM size
- OS + kernel version
- Network emulation method (tc/netem, hardware emulator, etc.)
- Concurrent session count
- Transport type (UDP/TCP/QUIC)

Without full environment disclosure,
numbers are considered invalid.

---

## 3) Core Metrics

### 3.1 Recovery Metrics

- RecoveryLatencyMs  
  Time between `TRANSPORT_DEAD` and `ATTACHED` after reattach.

- RecoveryAttempts  
  Number of reattach attempts before success.

- RecoverySuccessRate  
  % of sessions that recover within policy bounds.

- BoundedRecoveryCompliance  
  % of recoveries completed within MaxRecoveryWindowMs.

---

### 3.2 Stability Metrics

- SwitchesPerMinutePerSession
- FlapSuppressionEffectiveness
- DEGRADEDEntryRate
- ExplicitTerminationRate

These measure whether switching remains bounded and deterministic.

---

### 3.3 Control-Plane Metrics

- ReattachValidationTimeMs
- ReattachRejectRate (invalid proof)
- ReplayDetectionAccuracy
- ControlPlaneCPUUsage

---

### 3.4 Data-Plane Impact

(Not cryptographic performance — behavioral impact only)

- PacketLossDuringRecovery (%)
- JitterIncreaseDuringSwitch (ms)
- SessionContinuityIntegrity (boolean check)

---

### 3.5 Resource Metrics

- MemoryPerSession (bytes)
- CPUPer1kSessions (%)
- SessionTableLookupLatency
- StateMutationLatency

All metrics must remain bounded and scale predictably.

---

## 4) Failure Profiles to Test

### 4.1 Transport Death
- Hard UDP socket close
- Port change (NAT churn)
- Route drop

Expected:
- No silent reset
- Deterministic recovery
- Single active binding invariant preserved

---

### 4.2 Packet Loss Spike
- 10%
- 30%
- 60%

Expected:
- VOLATILE → RECOVERING
- Bounded switching
- No uncontrolled loops

---

### 4.3 Latency Surge
- +200ms
- +500ms
- +1000ms

Expected:
- Policy-driven decision
- Optional DEGRADED mode
- No session ID mutation

---

### 4.4 Control-Plane Abuse

- Reattach flood (invalid proof)
- Replay attempt burst
- Ownership conflict attempt

Expected:
- Early rejection
- No state corruption
- No dual-active binding

---

## 5) Scale Targets (Evaluation Phases)

Phase 1:
- 100 sessions
- Controlled lab volatility

Phase 2:
- 1,000 sessions
- Synthetic churn

Phase 3:
- 10,000+ sessions
- Mixed volatility + abuse simulation

No claims until Phase 2 minimum.

---

## 6) Success Criteria

The benchmark is considered successful if:

- No dual-active transport binding occurs
- No silent identity reset occurs
- All state transitions are reason-coded
- Recovery remains within bounded window
- Resource usage scales predictably

If instability exceeds bounds:
- Explicit DEGRADED or TERMINATED must occur
- Never silent failure

---

## 7) Publication Rule

Performance numbers must include:

- full test conditions
- volatility profile
- policy configuration
- session count
- hardware specs

Unreproducible numbers are invalid.

---

Session is the anchor.  
Transport is volatile.