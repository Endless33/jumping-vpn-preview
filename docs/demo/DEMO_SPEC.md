# Jumping VPN — Demo v1 (Contract)

This demo is a deterministic, measurable proof of the core claim:

**Session continuity survives transport volatility without renegotiation/reset,
within bounded policy.**

This is a behavioral demo contract.
It defines inputs, steps, and expected outputs.

---

## Goal

Show (in 20–30 seconds of runtime output):

1) A session is created and remains the identity anchor
2) Transport quality degrades (packet loss / jitter spike)
3) Flow-control reacts (cwnd/pacing adjusts)
4) A deterministic transport switch occurs (if a better candidate exists)
5) The session returns to ATTACHED (no identity reset)

---

## Test Conditions (Reproducible)

- Baseline: loss ~0%, stable RTT
- Volatility phase: loss spike to 5–10% for 3–5 seconds
- Candidate transport exists (Path B) with better score during volatility

---

## Demo Steps

### Step 0 — Baseline
Expected:
- `SESSION_CREATED`
- `PATH_SELECTED`
- `TELEMETRY_TICK` shows stable RTT/loss
- State: `ATTACHED`

### Step 1 — Volatility Signal
Inject loss/jitter spike.
Expected:
- `VOLATILITY_SIGNAL`
- `STATE_CHANGE: ATTACHED -> VOLATILE`
- `FLOW_CONTROL_UPDATE` (cwnd down / pacing adjusted)

### Step 2 — Candidate Scoring
Expected:
- `MULTIPATH_SCORE_UPDATE`
- Candidate ranking changes

### Step 3 — Deterministic Switch (bounded by policy)
Expected:
- `TRANSPORT_SWITCH`
- Audit events:
  - `NO_DUAL_ACTIVE_BINDING: PASS`
  - `NO_IDENTITY_RESET: PASS`

### Step 4 — Recovery
Expected:
- `RECOVERY_SIGNAL`
- `STATE_CHANGE: VOLATILE -> RECOVERING -> ATTACHED`

---

## Hard Pass/Fail Criteria

PASS if:
- SessionID stays constant across the entire run
- No `TERMINATED` occurs while a candidate transport is alive
- Switch is explicit + reason-coded
- State transitions are monotonic (versioned)

FAIL if:
- Identity resets / new session created during failover
- Dual-active binding occurs
- Silent renegotiation replaces session identity
- Non-deterministic oscillation occurs outside policy bounds

---

## Output Contract (JSONL)

The demo produces an event stream in JSONL (one event per line).
See: `DEMO_OUTPUT_FORMAT.md`

Session is the anchor. Transport is volatile.