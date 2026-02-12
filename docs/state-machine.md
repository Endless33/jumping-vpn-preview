# Jumping VPN — State Machine (Public Preview)

This document describes the session lifecycle state machine
and its allowed transitions.

It is intentionally protocol-level (behavioral),
not an implementation dump.

---

## 1. States

The session is the primary object.
Transports are bindings that can change over time.

### Session States

- **BIRTH**
  - Session created with identity and policy context.
  - No transport is required at this stage.

- **ATTACHED**
  - At least one working transport is bound to the session.
  - Data flow is possible.

- **VOLATILE**
  - Instability detected (loss spike, jitter, intermittent drops).
  - Continuity preserved, but transport quality is degraded.

- **DEGRADED**
  - Partial failure persists beyond thresholds.
  - Session remains alive under controlled constraints.

- **RECOVERING**
  - The system is actively binding a new transport to the existing session.
  - Reattachment is policy-bounded and auditable.

- **TERMINATED**
  - Session ended (lifetime exceeded or unrecoverable failure).
  - A new session requires a full initialization cycle.

---

## 2. High-Level Diagram

[BIRTH] | v [ATTACHED] <--------------------+ |                            | | instability detected        | v                            | [VOLATILE]                      | | prolonged instability       | v                            | [DEGRADED]                      | | reattach attempt            | v                            | [RECOVERING] --------------------+ | | no viable transports / policy exhausted / lifetime exceeded v [TERMINATED]

---

## 3. Allowed Transitions

### BIRTH → ATTACHED
Trigger:
- Initial transport successfully attached.

Required:
- Session identity exists.
- Policy context available.

---

### ATTACHED → VOLATILE
Trigger:
- Packet loss threshold exceeded
- Latency/jitter threshold exceeded
- Transport dead detected

Required:
- Explicit reason code
- Event emission

---

### VOLATILE → RECOVERING
Trigger:
- Policy decides to switch transport
- Active transport dies
- Volatility persists beyond threshold

Required:
- Switch must be explicit and auditable
- Switch rate must be within bounds

---

### VOLATILE → ATTACHED
Trigger:
- Transport stabilizes within recovery window

Required:
- Stability observed for a bounded period
- Event emission

---

### VOLATILE → DEGRADED
Trigger:
- Instability persists beyond degrade threshold

Required:
- Degraded mode constraints applied
- Event emission

---

### DEGRADED → RECOVERING
Trigger:
- Candidate transport is available
- Policy authorizes reattach attempt

Required:
- Rate limits and dampening apply

---

### RECOVERING → ATTACHED
Trigger:
- Reattachment succeeds
- Transport binding validated

Required:
- Emit `TransportSwitch` and `SessionStateChange`
- Reset volatility counters under bounded logic

---

### RECOVERING → DEGRADED
Trigger:
- Reattachment fails but session is still within grace window

Required:
- Log failure reason
- Apply cooldown / dampening if needed

---

### * → TERMINATED
Triggers (examples):
- No viable transports for duration > inactivity timeout
- Session lifetime exceeded
- Policy exhaustion / unrecoverable security failure

Required:
- Termination must be explicit
- Deterministic reason code
- No silent state disappearance

---

## 4. Forbidden Transitions (Safety)

The following are forbidden by design:

- **BIRTH → VOLATILE**
  - Volatility assumes at least one transport exists.

- **BIRTH → DEGRADED**
  - Degradation is a transport-quality concept.

- **TERMINATED → any state**
  - Terminated is final; a new session must be created.

- **ATTACHED → TERMINATED (without bounded failure condition)**
  - Termination must be justified by explicit, bounded rules.

---

## 5. Core Invariants

### I1 — Transport death ≠ Session death
Loss of a transport must not automatically terminate the session
if a candidate transport exists within policy constraints.

### I2 — Adaptation must be bounded
Switching is limited by:
- rate limits
- cooldowns
- stability scoring
- policy constraints

Unbounded switching is treated as failure.

### I3 — Reattachment must be auditable
Every switch attempt produces:
- timestamp
- reason code
- from/to transport identifiers
- outcome

### I4 — Failure boundaries are deterministic
If recovery cannot occur within bounded constraints,
the session terminates cleanly with explicit reason.

### I5 — No silent renegotiation
"Hidden" re-authentication or implicit identity reset is forbidden.
State transitions must explain behavior.

---

## 6. Reason Codes (Suggested)

Non-exhaustive reason code set:

- `loss_threshold_exceeded`
- `latency_threshold_exceeded`
- `transport_dead`
- `switch_rate_limited`
- `no_candidate_transports`
- `session_lifetime_exceeded`
- `inactivity_timeout`
- `reattach_validation_failed`

Reason codes must be stable and machine-readable.

---

## 7. Observability Events (Suggested)

Events emitted by the state machine:

- `SessionStateChange`
- `TransportAttached`
- `TransportSwitch`
- `TransportSwitchDenied`
- `TransportSwitchFailed`
- `DegradedModeEntered`
- `SessionTerminated`

Events must include:
- session_id
- previous_state
- new_state
- reason_code
- timestamp

---

## Summary

Jumping VPN treats volatility as a modeled state machine,
with bounded adaptation and deterministic failure boundaries.

The session remains the anchor.
Transports come and go.