# Observability Contract — Jumping VPN

Status: Formal Preview  
Scope: Behavioral transparency and audit guarantees  

This document defines the observability guarantees of Jumping VPN.

It specifies:

- What MUST be observable
- What MUST NOT affect correctness
- Event types
- Required audit fields
- Non-blocking logging rules
- Failure isolation boundaries

Observability is a transparency layer — not a control authority.

---

# 1. Design Principle

Observability must:

- Make every state transition inspectable
- Make every transport switch traceable
- Make policy enforcement visible
- Never block protocol correctness
- Never mutate session state

Logging failures degrade telemetry — not protocol behavior.

---

# 2. Required Event Categories

All production-grade deployments MUST emit structured events.

## 2.1 STATE_CHANGE

Triggered when session state changes.

Required fields:

- ts_ms
- session_id
- previous_state
- new_state
- reason_code
- state_version

Example:

{
  "event_type": "STATE_CHANGE",
  "session_id": "abc123",
  "previous_state": "RECOVERING",
  "new_state": "ATTACHED",
  "reason_code": "REATTACH_SUCCESS",
  "state_version": 13
}

---

## 2.2 TRANSPORT_SWITCH

Triggered when active transport binding changes.

Required fields:

- ts_ms
- session_id
- old_transport_id
- new_transport_id
- reason_code
- switch_latency_ms
- state_version

---

## 2.3 SECURITY_EVENT

Triggered when security violation or suspicious behavior occurs.

Examples:

- REPLAY_DETECTED
- INVALID_PROOF
- NONCE_REUSE
- DUAL_ACTIVE_ATTEMPT
- OWNERSHIP_CONFLICT

Required fields:

- ts_ms
- session_id
- violation_type
- reason_code
- state_version

Security events must never be silent.

---

## 2.4 POLICY_EVENT

Triggered when policy constraint activates.

Examples:

- SWITCH_RATE_LIMIT_EXCEEDED
- RECOVERY_WINDOW_EXCEEDED
- QUALITY_THRESHOLD_VIOLATED

Required fields:

- ts_ms
- session_id
- policy_name
- threshold_value
- observed_value
- state_version

---

## 2.5 TERMINATION_EVENT

Triggered when session enters TERMINATED.

Required fields:

- ts_ms
- session_id
- reason_code
- state_version
- total_lifetime_ms
- total_switches

Termination must always be logged.

---

# 3. Event Ordering Guarantees

Within a single node:

- Events MUST be emitted in state_version order.
- Version rollback is forbidden.
- Missing intermediate versions indicates data loss.

Cross-node ordering requires:

- Monotonic state_version enforcement
- Authoritative ownership model

---

# 4. Observability Must Be Non-Blocking

Rules:

- Logging MUST NOT block state transitions.
- Export failures MUST NOT revert state.
- Telemetry sinks MUST be asynchronous.

If observability pipeline fails:

- Protocol continues.
- A local degraded telemetry warning may be emitted.

Correctness > telemetry.

---

# 5. Session Timeline Requirements

A production system MUST be able to reconstruct:

- Session birth timestamp
- All state transitions
- All transport switches
- All security violations
- Final termination reason

If timeline reconstruction is impossible,
observability guarantees are violated.

---

# 6. Measurable Metrics

The observability layer MUST expose:

- Recovery latency (ms)
- Switch count per minute
- Time spent in VOLATILE
- Time spent in DEGRADED
- Transport loss events per session
- Termination rate

These metrics support:

- SLA analysis
- Pilot evaluation
- Abuse detection
- Stability modeling

---

# 7. Failure Isolation

Observability must never:

- Influence switch decisions
- Override policy engine
- Delay reattach processing
- Change state_version

Observability is read-only relative to state machine.

---

# 8. Privacy Boundaries

Observability must NOT log:

- Plaintext payload data
- User content
- Raw encryption keys
- Sensitive identity material

It logs behavior — not content.

---

# 9. Audit-Grade Guarantee

For every state transition:

There must exist:

- A deterministic trigger
- A reason_code
- A state_version increment
- A logged event

No silent transitions allowed.

---

# 10. Formal Invariant

For all sessions S:

For every transition T:
Exists exactly one STATE_CHANGE event with matching state_version.

No duplicate, no missing.

---

# Final Principle

If a session changes state,
someone must be able to prove why.

If a transport switches,
someone must be able to prove when.

If a session terminates,
someone must be able to prove the cause.

Behavior without visibility
is indistinguishable from error.

Session is the anchor.  
Transport is volatile.  
Transitions are observable.