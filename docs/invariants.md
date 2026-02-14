# Jumping VPN — Core Invariants

This document defines the non‑negotiable invariants of the Jumping VPN model.
These rules must hold across all implementations, demos, and runtime behaviors.

If an invariant is violated, the system is considered incorrect.

---

## 1. Identity Invariants

### 1.1 Session identity is immutable
- `session_id` never changes after creation.
- No silent renegotiation.
- No implicit re-authentication.

### 1.2 No dual-active binding
At no point may two transports be simultaneously active for the same session.

### 1.3 No identity reset during volatility
Transport death does not imply session death.

---

## 2. State Machine Invariants

### 2.1 State transitions are explicit
Every transition must be represented by a `STATE_CHANGE` event.

### 2.2 State transitions are monotonic
`state_version` increments by exactly +1 on every transition.

### 2.3 Illegal transitions are forbidden
Examples:
- `RECOVERING -> VOLATILE`
- `ATTACHED -> REATTACHING`
- `TERMINATED -> ATTACHED`

### 2.4 Terminal state is final
`TERMINATED` cannot transition to any other state.

---

## 3. Transport Invariants

### 3.1 Transport is replaceable
Transport may be detached, replaced, or reattached without affecting identity.

### 3.2 Transport switch is explicit
Every switch must emit:
- `REATTACH_REQUEST`
- `REATTACH_PROOF`
- `TRANSPORT_SWITCH`
- audit events

### 3.3 No implicit fallback
Transport cannot silently revert to a previous path.

---

## 4. Multipath Invariants

### 4.1 Candidate scoring is deterministic
Given the same metrics, the scoring function must produce the same ranking.

### 4.2 Switch requires reason code
Allowed reasons include:
- `PREFERRED_PATH_CHANGED`
- `LOSS_SPIKE`
- `LATENCY_DEGRADATION`
- `POLICY_TRIGGER`

### 4.3 No oscillation outside policy bounds
Transport cannot switch back and forth without explicit policy allowance.

---

## 5. Telemetry Invariants

### 5.1 Telemetry is periodic
`TELEMETRY_TICK` must appear at a stable interval.

### 5.2 Metrics must be realistic
- RTT cannot be negative.
- Loss cannot exceed 100%.
- Jitter cannot be negative.

### 5.3 Metrics must reflect state
- Volatility → degraded metrics.
- Recovery → improving metrics.

---

## 6. Flow Control Invariants

### 6.1 cwnd reacts to loss
Loss spike → cwnd decreases.

### 6.2 pacing reacts to congestion
Congestion → pacing decreases.

### 6.3 recovery restores flow control
Recovery → cwnd and pacing return toward baseline.

---

## 7. Audit Invariants

### 7.1 Every switch must be audited
Required checks:
- `NO_IDENTITY_RESET`
- `NO_DUAL_ACTIVE_BINDING`

### 7.2 Audit must be PASS or FAIL
No silent audit.

---

## 8. Demo Invariants

### 8.1 Demo output must be deterministic
Same input → same JSONL output.

### 8.2 SessionID must remain constant
Across the entire demo run.

### 8.3 State machine must follow the scenario
Baseline → Volatility → Degraded → Reattaching → Recovering → Attached.

---

## Summary

These invariants define the correctness boundary of Jumping VPN.
If an invariant is violated, the system is not behaving as designed.

Session is the anchor.  
Transport is volatile.