# Jumping VPN — Behavioral Specification (Public Preview)

Status: Draft (architectural validation)

This document defines the **behavioral contract** of Jumping VPN:
states, transitions, triggers, invariants, and observable events.

This preview does not disclose hardened cryptographic internals.
Where cryptographic validation is referenced, it is defined as an abstract requirement.

---

## 0. Definitions

- **Session**: Long-lived logical identity and policy context.
- **Transport**: Ephemeral binding (IP:port + protocol) attached to a session.
- **Reattach**: Binding a new transport to an existing session without session reset.
- **Volatility**: Expected transport instability (loss/jitter/NAT changes/path death).

---

## 1. State Machine

### 1.1 Session States

- `BIRTH`
- `ATTACHED`
- `VOLATILE`
- `DEGRADED`
- `RECOVERING`
- `TERMINATED`

`TERMINATED` is final.

### 1.2 Allowed Transitions

| From       | To          | Trigger Class | Required Event |
|-----------|-------------|---------------|----------------|
| BIRTH     | ATTACHED    | attach_ok     | SessionStateChange, TransportAttached |
| ATTACHED  | VOLATILE    | instability   | SessionStateChange |
| VOLATILE  | RECOVERING  | switch_start  | SessionStateChange |
| RECOVERING| ATTACHED    | reattach_ok   | TransportSwitch, SessionStateChange |
| VOLATILE  | DEGRADED    | degrade       | SessionStateChange |
| DEGRADED  | RECOVERING  | switch_start  | SessionStateChange |
| RECOVERING| DEGRADED    | reattach_fail | SessionStateChange |
| *         | TERMINATED  | terminal      | SessionTerminated, SessionStateChange |

Forbidden transitions are defined in `docs/state-machine.md`.

---

## 2. Triggers & Conditions (Normative)

### 2.1 Instability Detection (ATTACHED → VOLATILE)

A session MUST transition from `ATTACHED` to `VOLATILE` if any of the following are true:

- `loss_ratio(window) > LOSS_VOLATILE_THRESHOLD`
- `consecutive_drops >= MAX_CONSECUTIVE_DROPS`
- `heartbeat_age_ms > HEARTBEAT_VOLATILE_MS`
- active transport is marked `DEAD`

The transition MUST include a stable reason code:
- `loss_threshold_exceeded`
- `consecutive_drop_exceeded`
- `heartbeat_timeout`
- `transport_dead`

### 2.2 Degradation (VOLATILE → DEGRADED)

A session MUST transition from `VOLATILE` to `DEGRADED` if:

- `volatile_duration_ms > VOLATILE_TO_DEGRADED_MS`
  OR
- `switch_rate > MAX_SWITCHES_PER_MIN` (rate-limit condition)

Reason codes:
- `volatile_persisted`
- `switch_rate_limited`

### 2.3 Recovery Initiation (VOLATILE|DEGRADED → RECOVERING)

A session MAY enter `RECOVERING` if:

- at least one candidate transport is available
- switch rate is within policy bounds
- policy permits switching for the given trigger

The transition MUST be explicit and emit `SessionStateChange` with:
- `reason_code`
- `from_transport`
- `candidate_set_size`

Reason codes:
- `loss_recovery`
- `dead_transport_recovery`
- `policy_forced_recovery`

### 2.4 Successful Reattach (RECOVERING → ATTACHED)

A session MUST transition from `RECOVERING` to `ATTACHED` if:

- `ReattachValidation(session_id, proof, freshness)` returns VALID
- candidate transport becomes the active binding

It MUST emit:
- `TransportSwitch` (with `explicit=true`, `auditable=true`)
- `SessionStateChange`

Reason codes:
- `reattach_success`

### 2.5 Failed Reattach (RECOVERING → DEGRADED)

A session MUST transition from `RECOVERING` to `DEGRADED` if:

- validation fails (`bad_proof`, `replay`, `expired_session`)
- no candidates remain after attempting
- policy denies further attempts within the recovery window

Reason codes:
- `reattach_validation_failed`
- `no_candidate_transports`
- `policy_denied`

### 2.6 Termination (* → TERMINATED)

A session MUST terminate if any of the following become true:

- `session_age_ms > SESSION_MAX_LIFETIME_MS`
- `no_active_transport AND transportless_age_ms > TRANSPORT_LOST_TTL_MS`
- repeated security validation failures exceed policy
- explicit operator termination

It MUST emit:
- `SessionTerminated`
- `SessionStateChange`

Reason codes:
- `session_lifetime_exceeded`
- `transport_ttl_exceeded`
- `security_failure`
- `operator_terminated`

---

## 3. Invariants (Normative)

### I1 — Transport death ≠ session death (within bounds)
If at least one candidate transport exists AND session is within TTL,
then transport death MUST NOT directly cause `TERMINATED`.

### I2 — No silent identity reset
A session MUST NOT be replaced or renegotiated implicitly.
Any reset MUST be explicit and reason-coded.

### I3 — Bounded adaptation
Switching MUST be bounded by:
- `MAX_SWITCHES_PER_MIN`
- cooldown/dampening policy
- recovery window constraints

### I4 — Observability
Every state transition MUST be logged as `SessionStateChange`
with reason code and timestamp.

### I5 — Deterministic failure boundaries
If recovery cannot occur within bounded constraints,
termination MUST occur explicitly with stable reason code.

---

## 4. Observable Events (Normative)

All events MUST include:
- `ts_ms`
- `session_id`
- `event_type`
- `reason_code` (where applicable)

### Required Event Types

- `SessionStateChange`
- `TransportAttached`
- `TransportSwitch`
- `TransportSwitchDenied`
- `TransportSwitchFailed`
- `SessionTerminated`

---

## 5. Reason Codes (Stable Set)

Recommended stable reason code set:

- `attached_to_transport`
- `loss_threshold_exceeded`
- `consecutive_drop_exceeded`
- `heartbeat_timeout`
- `transport_dead`
- `loss_recovery`
- `dead_transport_recovery`
- `policy_forced_recovery`
- `reattach_success`
- `reattach_validation_failed`
- `no_candidate_transports`
- `switch_rate_limited`
- `volatile_persisted`
- `session_lifetime_exceeded`
- `transport_ttl_exceeded`
- `security_failure`
- `operator_terminated`

---

## Summary

This behavioral spec defines Jumping VPN by:

- explicit states
- deterministic transitions
- bounded adaptation rules
- auditable recovery and termination