# Jumping VPN — Evaluation Criteria

Status: Architectural Validation Framework

This document defines how Jumping VPN should be evaluated
in real-world environments.

It avoids marketing metrics.
It defines behavioral verification criteria.

---

# 1. Core Evaluation Principle

Jumping VPN must be evaluated on:

- Deterministic behavior
- Bounded adaptation
- Explicit state transitions
- Identity continuity under volatility

Not on peak throughput.

---

# 2. Functional Evaluation Criteria

## 2.1 Session Continuity Under Transport Failure

Test:

- Kill active transport
- Ensure backup transport exists

Expected Result:

- No session reset
- No renegotiation
- No re-authentication
- Explicit TransportSwitch event logged

Pass Condition:

Session remains in ATTACHED state after recovery.

---

## 2.2 Packet Loss Spike Handling

Test:

- Introduce packet loss above LOSS_VOLATILE_THRESHOLD
- Maintain alternative path

Expected Result:

- ATTACHED → VOLATILE
- Switch triggered
- Recovery within RECOVERY_WINDOW_MS

Pass Condition:

No silent session termination.

---

## 2.3 Flapping Resistance

Test:

- Alternate transport stability rapidly

Expected Result:

- Switch rate bounded by MAX_SWITCHES_PER_MIN
- TransportSwitchDenied events emitted
- DEGRADED state entered when necessary

Pass Condition:

No oscillation storm.
No CPU spike from unbounded switching.

---

## 2.4 Recovery Window Enforcement

Test:

- Prevent successful reattach for duration > RECOVERY_WINDOW_MS

Expected Result:

- RECOVERING → DEGRADED
- If policy requires → TERMINATED

Pass Condition:

No infinite recovery loop.

---

# 3. Security Evaluation Criteria

## 3.1 Replay Protection

Test:

- Attempt replay of old reattach message

Expected Result:

- Reattach rejected
- No state corruption

---

## 3.2 Unauthorized Transport Binding

Test:

- Attempt transport binding without valid session keys

Expected Result:

- Binding rejected
- Session remains secure

---

## 3.3 Session Fixation Resistance

Test:

- Attempt reuse of old SessionID without key proof

Expected Result:

- Reattach rejected

---

# 4. Observability Evaluation Criteria

System must:

- Emit SessionStateChange on every transition
- Emit reason codes
- Emit TransportSwitch events
- Emit SessionTerminated explicitly

SOC must be able to reconstruct:

- Full session timeline
- Transport transitions
- Degradation events

---

# 5. Performance Bound Evaluation

Under volatility:

- Detection latency <= HEARTBEAT_VOLATILE_MS
- Recovery latency <= RECOVERY_WINDOW_MS
- Switch frequency <= MAX_SWITCHES_PER_MIN
- No memory growth beyond defined bounds

---

# 6. Failure Boundary Evaluation

Verify that:

- Transport death ≠ session death (within TTL)
- Transportless state does not exceed TRANSPORT_LOST_TTL_MS
- Session TTL is strictly enforced
- No silent identity renegotiation occurs

---

# 7. Negative Evaluation Conditions

The system fails evaluation if:

- Silent renegotiation occurs
- Session resets without explicit state change
- Recovery loops unbounded
- Switch rate unbounded
- Replay attack succeeds
- Unauthorized binding succeeds

---

# 8. Comparison Evaluation (Optional)

When comparing to traditional VPN:

Measure:

- Session drop frequency under induced volatility
- Recovery latency
- Need for re-authentication
- Operator visibility of failover events

---

# Final Evaluation Standard

Jumping VPN succeeds if:

- Session continuity is preserved under bounded volatility
- Adaptation is deterministic
- All transitions are explicit
- Failure boundaries are enforced

It does not need to be faster.

It needs to be predictable.