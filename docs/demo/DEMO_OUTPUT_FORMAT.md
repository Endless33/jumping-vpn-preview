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