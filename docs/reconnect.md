# Jumping VPN — Reconnect Semantics (Preview)

This document defines the reconnect behavior for a session‑centric transport model.
Reconnect is deterministic, bounded, and identity‑preserving.

Session is the anchor.  
Transport is replaceable.

---

## State Machine (Reconnect Path)

`
ATTACHED
  │
  │ volatility detected
  ▼
VOLATILE
  │
  │ scoring update / candidate evaluation
  ▼
DEGRADED
  │
  │ switch allowed by policy
  ▼
REATTACHING
  │
  │ new transport validated
  ▼
RECOVERING
  │
  │ metrics stabilize
  ▼
ATTACHED
`

---

## Core Rules

### 1. Session identity is immutable
- `session_id` never changes
- no silent renegotiation
- no implicit re-auth

### 2. Transport is an attachment
- may die
- may be replaced
- may be re-evaluated

### 3. Reconnect is explicit
Every reconnect attempt emits:

- `REATTACH_REQUEST`
- `REATTACH_PROOF`
- `TRANSPORT_SWITCH`
- `AUDIT_EVENT`

### 4. No dual-active binding
At no point may two transports be active for the same session.

### 5. State transitions are monotonic
`state_version` increments on every transition.

---

## Timers

### `volatility_timeout_ms`
How long instability must persist before entering `VOLATILE`.

### `reattach_grace_ms`
Maximum time allowed for a transport to reattach before failover.

### `recovery_window_ms`
Time window for metrics to stabilize after switch.

---

## Reattach Sequence

1. Detect volatility  
2. Enter `VOLATILE`  
3. Score all candidates  
4. Select best path  
5. Emit `REATTACH_REQUEST`  
6. Validate new transport  
7. Emit `TRANSPORT_SWITCH`  
8. Enter `RECOVERING`  
9. Stabilize metrics  
10. Return to `ATTACHED`

---

## Fail Conditions

Reconnect fails if:

- no candidate transport exists  
- `reattach_grace_ms` expires  
- identity proof fails  
- dual-active binding detected  
- metrics diverge beyond policy bounds  

Failure leads to:

`TERMINATED(reason="REATTACH_FAILED")`

---

## Pass Conditions

Reconnect succeeds if:

- session_id remains constant  
- new transport validated  
- metrics stabilize  
- no identity reset  
- no dual-active binding  
- state returns to `ATTACHED`  

---

## Output Events (JSONL)

Reconnect emits:

- `VOLATILITY_SIGNAL`
- `MULTIPATH_SCORE_UPDATE`
- `REATTACH_REQUEST`
- `REATTACH_PROOF`
- `TRANSPORT_SWITCH`
- `RECOVERY_SIGNAL`
- `STATE_CHANGE`
- `AUDIT_EVENT`

These follow the format defined in `DEMO_OUTPUT_FORMAT.md`.

---

## Summary

Reconnect is:

- deterministic  
- bounded  
- auditable  
- identity-preserving  

Transport volatility is expected.  
Session continuity is guaranteed within policy.