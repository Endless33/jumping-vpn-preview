# Jumping VPN — Observability Contract

Status: Normative Logging & Event Specification (Public Preview)

This document defines the required event structure
for all observable behavior in Jumping VPN.

All implementations claiming compatibility
must conform to this contract.

---

# 1. Design Principles

Observability must be:

- Deterministic
- Explicit
- Structured
- Machine-readable
- Audit-friendly

No silent transitions allowed.

---

# 2. Event Format (JSONL Model)

Each event MUST be emitted as a single JSON object.

Required base structure:

{
  "ts_ms": 1700000000000,
  "event_type": "SessionStateChange",
  "session_id": "abc123",
  "previous_state": "VOLATILE",
  "new_state": "RECOVERING",
  "reason_code": "loss_threshold_exceeded",
  "node_id": "server-01",
  "policy_version": "v1.0",
  "transport_id": "udp-443-01"
}

---

# 3. Required Event Types

## 3.1 SessionStateChange

Emitted on every FSM transition.

Fields:

- previous_state
- new_state
- reason_code

MUST be emitted for all transitions.

---

## 3.2 TransportSwitch

Emitted when new transport becomes active.

Fields:

{
  "previous_transport": "udp-443-01",
  "new_transport": "udp-8443-02",
  "candidate_count": 2,
  "loss_ratio": 0.23,
  "latency_estimate_ms": 82,
  "explicit": true
}

---

## 3.3 TransportSwitchDenied

Emitted when switch rejected.

Reason codes:

- switch_rate_limited
- cooldown_active
- no_valid_candidate
- policy_denied

---

## 3.4 SessionTerminated

Emitted when session reaches TERMINATED.

Fields:

- reason_code
- session_age_ms
- transportless_age_ms

---

## 3.5 ReattachAttempt

Emitted at reattach initiation.

Fields:

- candidate_transport
- recovery_deadline_ms

---

## 3.6 ReattachResult

Emitted after validation.

Fields:

- status: SUCCESS | DENIED
- reason_code

---

# 4. Required Base Fields

All events MUST include:

- ts_ms
- event_type
- session_id
- node_id
- policy_version

Optional:

- cluster_id
- deployment_env
- client_id (if allowed by policy)

---

# 5. Reason Code Stability

Reason codes MUST:

- Be stable across versions
- Be documented
- Not change meaning silently
- Be human-readable

Example:

"loss_threshold_exceeded"
NOT:
"error_42"

---

# 6. Logging Guarantees

The system MUST NOT:

- Suppress transitions
- Merge multiple transitions into one
- Emit synthetic transitions
- Omit reason codes

Every state mutation MUST produce one event.

---

# 7. SIEM Integration Model

Events must be compatible with:

- JSONL streaming
- Log aggregation pipelines
- SIEM ingestion
- Distributed tracing

No binary-only logging.

---

# 8. Security Logging Requirements

Security-related events MUST be logged:

- reattach_validation_failed
- replay_detected
- unauthorized_transport_attempt
- switch_rate_limited
- policy_denied

Security events MUST be distinguishable.

---

# 9. Deterministic Replayability

Given a sequence of events,
an auditor MUST be able to reconstruct:

- Full session lifecycle
- All transport switches
- Degradation phases
- Termination reason

Event stream must be sufficient for timeline reconstruction.

---

# 10. Design Philosophy

Observability is not debugging.

It is a behavioral contract.

If volatility occurs,
it must be visible.

If adaptation occurs,
it must be explainable.

If termination occurs,
it must be justified.