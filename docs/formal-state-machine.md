# Formal State Machine — Jumping VPN (Preview)

This document defines the session state machine in a formal, RFC-style form.

The purpose is behavioral clarity:
exact transitions, triggers, and deterministic outcomes.

---

# 1. State Set

Let `S` be the set of session states:

- `BIRTH`
- `ATTACHED`
- `VOLATILE`
- `DEGRADED`
- `RECOVERING`
- `TERMINATED`

`TERMINATED` is absorbing (no transitions out).

---

# 2. Inputs (Events)

Let `E` be the set of observable inputs:

- `ATTACH_OK`
- `TRANSPORT_DEAD`
- `VOLATILITY_SIGNAL`
- `RECOVERY_SIGNAL`
- `REATTACH_OK`
- `REATTACH_FAIL`
- `POLICY_LIMIT_EXCEEDED`
- `SESSION_TTL_EXPIRED`
- `SECURITY_VIOLATION`

---

# 3. Policy Parameters

Let policy define bounds:

- `MaxRecoveryWindowMs`
- `MaxSwitchesPerMinute`
- `TransportLossTtlMs`
- `SessionTtlMs`
- `VolatilityThresholds` (loss/latency/jitter floors)

Policy evaluation is deterministic.

---

# 4. Transition Function

Define a deterministic transition function:

`δ(state, event) -> (new_state, reason_code, actions[])`

All transitions must emit:

- `STATE_CHANGE` (except self-transitions)
- `reason_code`

---

# 5. Transition Table

## BIRTH

- δ(`BIRTH`, `ATTACH_OK`) -> `ATTACHED`, `initial_attach_success`, [`emit_audit`]
- δ(`BIRTH`, `SESSION_TTL_EXPIRED`) -> `TERMINATED`, `ttl_expired`, [`terminate`]
- δ(`BIRTH`, `SECURITY_VIOLATION`) -> `TERMINATED`, `security_violation`, [`terminate`]

## ATTACHED

- δ(`ATTACHED`, `VOLATILITY_SIGNAL`) -> `VOLATILE`, `volatility_detected`, [`evaluate_candidates`]
- δ(`ATTACHED`, `TRANSPORT_DEAD`) -> `RECOVERING`, `transport_dead`, [`start_recovery_timer`, `reattach_attempt`]
- δ(`ATTACHED`, `SESSION_TTL_EXPIRED`) -> `TERMINATED`, `ttl_expired`, [`terminate`]
- δ(`ATTACHED`, `SECURITY_VIOLATION`) -> `TERMINATED`, `security_violation`, [`terminate`]

## VOLATILE

- δ(`VOLATILE`, `RECOVERY_SIGNAL`) -> `RECOVERING`, `recovery_window_open`, [`reattach_attempt`]
- δ(`VOLATILE`, `TRANSPORT_DEAD`) -> `RECOVERING`, `transport_dead`, [`start_recovery_timer`, `reattach_attempt`]
- δ(`VOLATILE`, `POLICY_LIMIT_EXCEEDED`) -> `DEGRADED`, `anti_flap_triggered`, [`apply_dampening`]
- δ(`VOLATILE`, `SESSION_TTL_EXPIRED`) -> `TERMINATED`, `ttl_expired`, [`terminate`]
- δ(`VOLATILE`, `SECURITY_VIOLATION`) -> `TERMINATED`, `security_violation`, [`terminate`]

## DEGRADED

- δ(`DEGRADED`, `RECOVERY_SIGNAL`) -> `RECOVERING`, `recovery_window_open`, [`reattach_attempt`]
- δ(`DEGRADED`, `POLICY_LIMIT_EXCEEDED`) -> `TERMINATED`, `policy_exceeded`, [`terminate`]
- δ(`DEGRADED`, `SESSION_TTL_EXPIRED`) -> `TERMINATED`, `ttl_expired`, [`terminate`]
- δ(`DEGRADED`, `SECURITY_VIOLATION`) -> `TERMINATED`, `security_violation`, [`terminate`]

## RECOVERING

- δ(`RECOVERING`, `REATTACH_OK`) -> `ATTACHED`, `reattach_success`, [`emit_audit`, `reset_recovery_timer`]
- δ(`RECOVERING`, `REATTACH_FAIL`) -> `VOLATILE`, `reattach_failed`, [`evaluate_candidates`]
- δ(`RECOVERING`, `POLICY_LIMIT_EXCEEDED`) -> `DEGRADED`, `anti_flap_triggered`, [`apply_dampening`]
- δ(`RECOVERING`, `SESSION_TTL_EXPIRED`) -> `TERMINATED`, `ttl_expired`, [`terminate`]
- δ(`RECOVERING`, `SECURITY_VIOLATION`) -> `TERMINATED`, `security_violation`, [`terminate`]

## TERMINATED

- δ(`TERMINATED`, *) -> `TERMINATED`, `terminated`, [`no_op`]

---

# 6. Determinism Requirements

- No transition is implicit.
- Every transition is reason-coded.
- Policy evaluation must be reproducible.
- No unbounded retry loops.

---

# 7. Invariants (Machine Form)

I1: `TERMINATED` is absorbing.  
I2: `|ActiveTransport(session)| ≤ 1` at all times.  
I3: `SessionID` is stable across reattach within `SessionTtlMs`.  
I4: If `MaxRecoveryWindowMs` expires -> `TERMINATED`.  
I5: If `MaxSwitchesPerMinute` exceeded -> `DEGRADED` or `TERMINATED`.

---

# 8. Observability Hooks

On each state change emit:

- `STATE_CHANGE`
- `reason_code`
- optional `AUDIT_EVENT`

The protocol must be auditable by design.

---

Session is the anchor.  
Transport is volatile.