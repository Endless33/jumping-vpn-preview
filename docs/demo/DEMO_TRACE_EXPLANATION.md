# Jumping VPN — Demo Trace Explanation (How to Read It)

This document explains how to read the public demo trace and what it proves.

The trace is **JSONL**:
- one JSON object per line
- each line is a protocol event
- replay/validation reads the file line-by-line

File:
- `DEMO_TRACE.jsonl`

Validator:
- `demo_engine/replay.py`

---

## What the trace is (and is not)

### It IS
- an auditable sequence of protocol events
- a deterministic behavioral contract snapshot
- a review artifact for engineers

### It is NOT
- a full production VPN traffic capture
- a cryptographic proof of encryption correctness
- a benchmark

The purpose is architectural: **prove session continuity under transport volatility**.

---

## Core claim proven by the trace

> The session survives transport volatility without renegotiation or identity reset.

This is shown by:

- explicit volatility detection
- explicit switch event
- explicit recovery back to ATTACHED
- continuous session identity across the timeline

---

## Event types you will see

### 1) SESSION_CREATED
Creates the session identity anchor.

Typical fields:
- `session_id`
- initial `state`
- `state_version`

**What to check**
- session_id remains the same across all later events

---

### 2) PATH_SELECTED / PATH_EVALUATED (optional depending on trace)
Shows which transport path is active/preferred.

Typical fields:
- `active_path` or `preferred_path`
- `score` (rtt/jitter/loss)
- policy gates (cooldown/rate limit)

**What to check**
- a path selection exists before volatility/switch

---

### 3) TELEMETRY_TICK (optional)
Periodic measurements.

Typical fields:
- `rtt_ms`
- `jitter_ms`
- `loss_pct`
- `cwnd`
- `pacing`
- `in_flight`

**What to check**
- baseline is stable before volatility spike

---

### 4) VOLATILITY_SIGNAL
Transport became unstable.

Typical fields:
- `reason`: LOSS_SPIKE / JITTER_SPIKE / RTT_JUMP / PATH_DEGRADED
- `observed`: measured metrics

**What to check**
- volatility is explicit (not inferred)
- it happens before state changes/switch

---

### 5) STATE_CHANGE
Explicit session lifecycle transition.

Required fields:
- `from`
- `to`
- `reason`
- `state_version` (must increase)

**What to check**
- `ATTACHED → VOLATILE` occurs after volatility signal
- later `RECOVERING → ATTACHED` occurs after stability window

---

### 6) FLOW_CONTROL_UPDATE / PACING_UPDATE (optional)
Adaptation response to volatility.

Typical fields:
- `cwnd` changes
- `pacing` changes
- `reason`: LOSS_REACTION / RTT_REACTION

**What to check**
- adaptation is reason-coded and bounded
- state is not reset

---

### 7) TRANSPORT_SWITCH
The key proof event.

Required fields:
- `from_path`
- `to_path`
- `reason`

**What to check**
- switch is explicit
- session_id remains identical
- no termination
- no renegotiation event appears

---

### 8) AUDIT_EVENT (optional but recommended)
Auditable safety assertions.

Examples:
- `NO_DUAL_ACTIVE_BINDING`
- `NO_IDENTITY_RESET`

**What to check**
- audit checks PASS around switching

---

### 9) RECOVERY_COMPLETE / final STATE_CHANGE
Shows return to stable.

**What to check**
- session ends in ATTACHED
- no identity reset happened
- session_id stays constant

---

## What a reviewer should conclude

If the validator passes:

1) The trace contains the required sequence of events  
2) The session stays continuous across volatility and switching  
3) The state machine behavior is explicit and auditable  

This is the architectural milestone:
**transport volatility is survivable without breaking session continuity**.

---

## Quick validation

Run:

```bash
python demo_engine/replay.py DEMO_TRACE.jsonl

Expected result:

prints a short checklist of required events
ends with a success line (trace validated)
If validation fails:

the trace is missing required events
event ordering violated invariants
state continuity is broken

---

## 2) `jumping-vpn-preview/docs/ONBOARDING.md`

```md
# Jumping VPN — Onboarding (Fastest Review Path)

This is the fastest way to understand and validate the Jumping VPN preview repository.

If you only have 5 minutes, follow this page.

---

## 1) What this repository proves

Jumping VPN is a **session-anchored transport model**:

- identity ≠ IP
- identity ≠ socket
- identity = session anchor

Transport is a replaceable attachment.

This repo proves (architecturally) that:

> session continuity can survive transport volatility deterministically.

---

## 2) Start here (reading order)

1) `START_HERE.md`  
2) `docs/INVARIANTS.md`  
3) `docs/STATE_MACHINE.md`  
4) `DEMO_TRACE.jsonl`  
5) `docs/DEMO_TRACE_EXPLANATION.md`  

---

## 3) Validate the public demo trace

### Requirements
- Python 3.10+

### Command
From repo root:

```bash
python demo_engine/replay.py DEMO_TRACE.jsonl

Expected output (example)

You should see a short list like:

SESSION_CREATED OK

VOLATILITY_SIGNAL OK

TRANSPORT_SWITCH OK

STATE_CHANGE OK

RECOVERY_COMPLETE OK

and then:
Trace validated successfully. Session continuity preserved.

4) Where outputs are
This repo includes:

DEMO_TRACE.jsonl → the public review trace
If you run any local demo scripts (if present in your fork), outputs typically land in:

DEMO_OUTPUT.jsonl (generated trace)

DEMO_PACKAGE.zip (bundle)

DEMO_ECOSYSTEM/ (demo assets)

Not all repositories expose generation by default — the public guarantee here is the trace + validator.

5) What to review if you are an engineer

A) Safety and correctness

Do invariants prevent silent identity resets?

Are transitions explicit and reason-coded?

Is termination final?

B) Attack surface thinking
Replay/injection rejection before mutation

Zombie attachment pruning rules

Single-active attachment invariant

C) Determinism

Can the session trajectory be reconstructed from events?

6) What this is not (explicit)

This preview is not claiming:
production cryptographic implementation

OS-level TUN integration
full VPN feature parity

This is a protocol architecture and behavioral validation package.

Summary

If you want one sentence:

Jumping VPN keeps session identity stable while transport paths are allowed to degrade, switch, and disappear — deterministically.

Next steps (outside this preview) include:
live transport adapters
production cryptographic binding

TUN integration

