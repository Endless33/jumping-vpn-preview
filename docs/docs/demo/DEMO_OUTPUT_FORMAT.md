# Jumping VPN — Demo Output Format (JSONL)

This document defines the expected JSONL structure for demo output.
It is a contract-first output format (not claiming an executed run).

---

## Envelope

Each line is a JSON object with:

- `ts_ms` (int) — Unix timestamp in ms  
- `event` (string) — event name  
- `session_id` (string)  
- `state` (optional string)  
- `state_version` (optional int, monotonic)  
- `reason` (optional string)  
- `metrics` (optional object)  
- `details` (optional object)

---

## Example Events (Format Only)

```json
{"ts_ms":0,"event":"SESSION_CREATED","session_id":"s_x","state":"ATTACHED","state_version":0}
{"ts_ms":1,"event":"TELEMETRY_TICK","session_id":"s_x","metrics":{"rtt_ms":24,"jitter_ms":3,"loss_pct":0.0,"cwnd":64,"pacing_pps":1200}}
{"ts_ms":2,"event":"VOLATILITY_SIGNAL","session_id":"s_x","reason":"LOSS_SPIKE","metrics":{"loss_pct":7.5,"rtt_ms":41,"jitter_ms":18}}
{"ts_ms":3,"event":"TRANSPORT_SWITCH","session_id":"s_x","reason":"PREFERRED_PATH_CHANGED","details":{"from":"udp:A","to":"udp:B"}}
{"ts_ms":4,"event":"AUDIT_EVENT","session_id":"s_x","details":{"check":"NO_IDENTITY_RESET","result":"PASS"}}
{"ts_ms":5,"event":"STATE_CHANGE","session_id":"s_x","details":{"from":"RECOVERING","to":"ATTACHED"}}

Notes:

- The demo output must be deterministic and auditable  
- Consumers must be able to verify:  
  - stable SessionID  
  - monotonic state_version  
  - explicit transitions  
  - explicit switch reasons  

This format is intentionally minimal and readable.
`

---

# ✅ **3. `docs/demo/STATUS.md`**

Скопируй полностью:

```md
# Demo Status

## What exists today (public preview)

- Architecture model + state machine + invariants  
- Threat model, non-goals, limitations  
- Behavioral PoCs (conceptual / minimal)  
- Telemetry event model  
- Multipath scoring model  
- Flow-control model (cwnd/pacing/in-flight)

## What is not public / not finalized

- Production-grade cryptography  
- Full TUN integration  
- Fully formalized reconnect semantics for all edge cases  
- Public, reproducible benchmark numbers  
- Deterministic transport-switch policy implementation

## What this demo package provides

- A measurable demo contract (steps + pass/fail)  
- A stable output format (JSONL event stream)  
- A reviewer-friendly validation checklist  
- A clear boundary between implemented and non-implemented parts

This repository is a window into the model.  
The demo contract defines what will be proven on real runtime output.

Session is the anchor. Transport is volatile.