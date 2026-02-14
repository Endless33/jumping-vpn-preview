# Jumping VPN — Demo Scenario (Behavior Timeline)

This document defines the expected behavior timeline for the demo run.
It is not an executed trace — it is a deterministic scenario contract.

The demo lasts ~20–30 seconds and produces a JSONL event stream.

---

## Phase 0 — Baseline (0–5s)

Transport is stable.  
Session is attached.

Expected events:

- `SESSION_CREATED`
- `PATH_SELECTED`
- periodic `TELEMETRY_TICK`

Expected metrics:

- `rtt_ms`: stable (20–40ms)
- `jitter_ms`: low (1–5ms)
- `loss_pct`: ~0%
- `cwnd`: stable
- `pacing_pps`: stable

State:

- `ATTACHED`
- `state_version = 0`

---

## Phase 1 — Volatility Injection (5–10s)

Simulated instability:

- packet loss spike (5–10%)
- jitter spike (10–30ms)
- RTT increase

Expected events:

- `VOLATILITY_SIGNAL`
- `STATE_CHANGE: ATTACHED -> VOLATILE`
- `FLOW_CONTROL_UPDATE` (cwnd down, pacing reduced)
- `TELEMETRY_TICK` with degraded metrics

Expected metrics:

- `loss_pct`: 5–10%
- `jitter_ms`: 15–30ms
- `rtt_ms`: +20–40ms from baseline

State:

- `VOLATILE`
- `state_version = 1`

---

## Phase 2 — Candidate Evaluation (10–15s)

Multipath scoring reacts to volatility.

Expected events:

- `MULTIPATH_SCORE_UPDATE`
- `MULTIPATH_SCORE_UPDATE` (ranking changes)
- `TELEMETRY_TICK` (still degraded)

Expected behavior:

- Path A score drops
- Path B score rises (better candidate)

State:

- `DEGRADED`
- `state_version = 2`

---

## Phase 3 — Deterministic Switch (15–20s)

Policy allows switch.

Expected events:

- `REATTACH_REQUEST`
- `REATTACH_PROOF`
- `TRANSPORT_SWITCH`
- `AUDIT_EVENT: NO_IDENTITY_RESET`
- `AUDIT_EVENT: NO_DUAL_ACTIVE_BINDING`
- `STATE_CHANGE: DEGRADED -> REATTACHING`

Expected details:

```json
{"from":"udp:A","to":"udp:B"}

State:

REATTACHING

state_version = 3

Phase 4 — Recovery (20–25s)

New transport stabilizes.

Expected events:

RECOVERY_SIGNAL

FLOW_CONTROL_UPDATE (cwnd/pacing recover)

TELEMETRY_TICK (metrics improving)

STATE_CHANGE: REATTACHING -> RECOVERING

Expected metrics:

loss_pct: returns to ~0%

jitter_ms: returns to baseline

rtt_ms: returns to baseline

cwnd: increases

pacing_pps: increases

State:

RECOVERING

state_version = 4

Phase 5 — Return to Stable (25–30s)

System returns to normal operation.

Expected events:

STATE_CHANGE: RECOVERING -> ATTACHED

TELEMETRY_TICK (stable metrics)

State:

ATTACHED

state_version = 5

Hard Pass Criteria

The run is a PASS if:

session_id remains constant

no identity reset

no dual-active binding

switch is explicit and reason-coded

state transitions are monotonic

metrics degrade and recover realistically

Hard Fail Criteria

The run is a FAIL if:

session_id changes

silent renegotiation occurs

transport switch happens without reason

oscillation occurs outside policy bounds

metrics diverge without recovery

state machine violates allowed transitions

Summary

This scenario defines:

the timeline

the expected events

the expected metrics

the expected state transitions

It is the behavioral contract for the demo.