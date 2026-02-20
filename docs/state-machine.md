# Jumping VPN — State Machine (Preview)

This document defines the **valid session states** and **allowed transitions**.

The goal is not to list features.
The goal is to make **continuity behavior explicit and reviewable**.

---

## 1) States

### BIRTH
Session object exists but is not yet attached to a transport.

### ATTACHED
Session has a validated active transport attachment.
Normal operation.

### VOLATILE
The active transport has entered instability:
loss spike / jitter spike / RTT jump / path degradation.

VOLATILE is not failure — it is a modeled state.

### RECOVERING
A transport switch has occurred or stability window is being evaluated.
The session is converging back to normal behavior.

### TERMINATED
Session is closed.
No further attachments accepted.

---

## 2) Transition table (canonical)

### 2.1 Creation / Attach

- `BIRTH → ATTACHED`
  - reason: `ATTACH_OK`
  - requires: validated attachment + continuity accepted

### 2.2 Volatility detection

- `ATTACHED → VOLATILE`
  - reason: `LOSS_SPIKE` / `JITTER_SPIKE` / `RTT_JUMP` / `PATH_DEGRADED`
  - requires: volatility signal from telemetry/health logic

### 2.3 Switch / Recovery entry

- `VOLATILE → RECOVERING`
  - reason: `TRANSPORT_SWITCHED` or `RECOVERY_WINDOW_ENTER`
  - requires: explicit switch OR entering stability evaluation

### 2.4 Return to stable

- `RECOVERING → ATTACHED`
  - reason: `RECOVERY_COMPLETE`
  - requires: stability window passed

### 2.5 Failure termination (explicit only)

- `ATTACHED → TERMINATED`
- `VOLATILE → TERMINATED`
- `RECOVERING → TERMINATED`
  - reason: `TTL_EXPIRED` / `POLICY_FAIL` / `FATAL_ERROR`

---

## 3) Forbidden transitions

These must never occur:

- `ATTACHED → BIRTH`
- `VOLATILE → BIRTH`
- `RECOVERING → BIRTH`
- `TERMINATED → *` (no resurrection)

Also forbidden:

- silent transition with no reason
- transition without `state_version++`

---

## 4) Event requirements (trace contract)

Every state change must emit:

- `event: "STATE_CHANGE"`
- `from`, `to`
- `reason`
- `state_version` (monotonic)

Transport switch must emit:

- `event: "TRANSPORT_SWITCH"`
- `from_path`, `to_path`
- `reason`

Volatility detection must emit:

- `event: "VOLATILITY_SIGNAL"`
- `reason`
- `observed` metrics (loss/jitter/rtt if available)

---

## 5) Minimal demo scenario (required)

A valid demo must show this chain:

1) Session created / attached  
2) Volatility signal occurs  
3) Enter VOLATILE  
4) Adaptation + switch  
5) Enter RECOVERING  
6) Return to ATTACHED  

With the key rule:

> session identity remains continuous across the switch.

---

## 6) Notes on extensibility

This preview state machine is minimal by design.

Future states may include:
- `DEGRADED`
- `REATTACHING`
- `MIGRATING`
- `SUSPENDED`

But the invariants remain:

- session identity is stable
- transport is replaceable
- recovery is deterministic
- termination is explicit and final

---

## Summary

Jumping VPN treats transport volatility as a normal condition.

The state machine exists to make that behavior:
- deterministic
- auditable
- reviewable