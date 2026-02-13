# Jumping VPN — Failure Matrix (Public Preview)

Status: Draft (architectural validation)

This document defines how the system behaves under different failure classes.

The purpose is to eliminate ambiguity:
Failure is modeled.  
Recovery is bounded.  
Termination is deterministic.

---

## 0. Failure Classes

Jumping VPN distinguishes:

1. Transport Failure
2. Degradation
3. Recovery Failure
4. Security Failure
5. Policy Violation
6. Hard System Failure

Each class produces deterministic state transitions.

---

# 1. Transport Failure

### Case 1.1 — Single Transport Death (Backup Available)

Condition:
- active transport marked DEAD
- candidate transport exists

Expected Behavior:
- ATTACHED → VOLATILE
- VOLATILE → RECOVERING
- RECOVERING → ATTACHED (after successful reattach)

Guarantees:
- Session is NOT terminated
- Identity remains intact
- No re-authentication required

Events:
- TransportDead
- SessionStateChange
- TransportSwitch
- SessionStateChange

Invariant Enforced:
I1 — Transport death ≠ session death

---

### Case 1.2 — Single Transport Death (No Backup)

Condition:
- active transport DEAD
- no candidates available

Behavior:
- ATTACHED → VOLATILE
- VOLATILE → DEGRADED
- If transportless_age_ms > TRANSPORT_LOST_TTL_MS → TERMINATED

Guarantee:
- No silent session reset
- Termination is explicit and reason-coded

---

# 2. Packet Loss Spike

### Case 2.1 — Temporary Loss Spike

Condition:
- loss_ratio(window) > LOSS_VOLATILE_THRESHOLD
- backup transport available

Behavior:
- ATTACHED → VOLATILE
- Switch initiated
- RECOVERING → ATTACHED

Guarantee:
- No renegotiation
- No session reset

---

### Case 2.2 — Sustained Loss Spike (No Stable Path)

Condition:
- All candidate transports exceed loss threshold

Behavior:
- ATTACHED → VOLATILE
- VOLATILE → DEGRADED
- Remains DEGRADED until:
    - stable candidate appears
    OR
    - TTL exceeded → TERMINATED

Guarantee:
- No oscillation beyond MAX_SWITCHES_PER_MIN
- Degradation is visible and logged

---

# 3. Transport Flapping

Condition:
- rapid alternating transport health
- switch_rate > MAX_SWITCHES_PER_MIN

Behavior:
- Switch attempts denied
- Enter or remain in DEGRADED
- Apply SWITCH_COOLDOWN_MS

Guarantee:
- Bounded adaptation
- No oscillation storm

Event:
- TransportSwitchDenied (reason: switch_rate_limited)

Invariant Enforced:
I3 — Bounded adaptation

---

# 4. Reattach Validation Failure

Condition:
- invalid proof
- expired session
- replay detected

Behavior:
- RECOVERING → DEGRADED
- If repeated failures exceed policy → TERMINATED

Guarantee:
- No unauthorized session takeover
- No silent fallback to new identity

Reason codes:
- reattach_validation_failed
- security_failure

Invariant Enforced:
I2 — No silent identity reset

---

# 5. Session TTL Expiry

Condition:
- session_age_ms > SESSION_MAX_LIFETIME_MS

Behavior:
- Any state → TERMINATED

Guarantee:
- Hard lifecycle boundary
- Predictable session rotation

---

# 6. Complete Network Blackout

Condition:
- No viable transports
- No candidate paths
- transportless_age_ms increases

Behavior:
- ATTACHED → VOLATILE → DEGRADED
- After TTL → TERMINATED

Guarantee:
- Session survives within TTL
- Termination is explicit

---

# 7. Policy-Enforced Switch Denial

Condition:
- switch_rate exceeded
- cooldown active
- policy restriction

Behavior:
- Remain in current state or DEGRADED
- Emit TransportSwitchDenied

Guarantee:
- Deterministic decision
- Fully auditable

---

# 8. Operator Termination

Condition:
- explicit administrative command

Behavior:
- Any state → TERMINATED

Guarantee:
- Clean state teardown
- SessionTerminated emitted

---

# Summary Table

| Failure Type                | Session Survives? | Explicit Transition? | Auditable? |
|-----------------------------|------------------|----------------------|------------|
| Single Transport Death      | Yes (if backup)  | Yes                  | Yes        |
| Loss Spike (temporary)      | Yes              | Yes                  | Yes        |
| Sustained Instability       | Yes (bounded)    | Yes                  | Yes        |
| Flapping                    | Yes              | Yes                  | Yes        |
| Validation Failure          | Depends policy   | Yes                  | Yes        |
| Session TTL Expired         | No               | Yes                  | Yes        |
| No Transport (TTL exceeded) | No               | Yes                  | Yes        |

---

## Final Statement

Jumping VPN does not collapse on transport failure.

It models:

- degradation
- bounded recovery
- deterministic termination

Failure is not an exception.
It is part of the state machine.