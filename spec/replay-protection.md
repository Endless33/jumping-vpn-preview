# Jumping VPN — Replay Protection (Abstract Requirements)

Status: Normative Security Requirement (Public Preview)

This document defines anti-replay requirements for
reattach and control-plane messages.

Cryptographic primitives and wire formats are intentionally abstracted.

---

## 1. Threat

An attacker may capture a valid control-plane message (e.g., REATTACH_REQUEST)
and attempt to replay it later to:

- hijack a session binding
- force state churn
- bypass bounded recovery rules
- desynchronize client/server state

Replay must not succeed.

---

## 2. Scope

Replay protection applies to at minimum:

- REATTACH_REQUEST
- REATTACH_ACK / REATTACH_DENY
- any message that mutates session state
- any message that changes active transport binding

---

## 3. Required Properties (Normative)

### R1 — Freshness
Every state-mutating message MUST include a freshness marker:

- nonce, or
- strictly increasing counter, or
- timestamp with bounded acceptance

### R2 — Bounded Acceptance Window
Freshness markers MUST be valid only within a bounded window:

- time window (e.g., max age)
AND/OR
- sequence window (e.g., sliding counter window)

### R3 — Replay Cache / Window Tracking
The receiver MUST track previously seen freshness markers
within the acceptance window and reject duplicates.

### R4 — Session Binding
Freshness validation MUST be bound to:

- SessionID
- cryptographic proof of possession (abstract)
- current session state version (recommended)

Replay from a different transport MUST still fail.

### R5 — Deterministic Failure Response
On replay detection, the system MUST:

- reject the request
- emit a security event (observability contract)
- NOT change active transport binding
- optionally apply rate limits or quarantine policy

---

## 4. Receiver Behavior

On receiving a state-mutating message:

1) Lookup session by SessionID  
2) Validate proof-of-possession (abstract)  
3) Validate freshness marker:
   - within allowed time window
   - not previously seen
4) If freshness invalid:
   - deny
   - emit event: `SecurityReplayDetected`
   - return without state mutation

---

## 5. Suggested Mechanisms (Non-Normative)

Implementations may use:

- monotonic counter + sliding window
- nonce + LRU cache with TTL
- timestamp + nonce + window tracking

Choice depends on environment and performance constraints.

---

## 6. Observability Requirements

Replay detection MUST emit:

- event_type: `SecurityReplayDetected`
- session_id
- ts_ms
- reason_code: `replay_detected`
- freshness_marker_type
- optional: transport_id, node_id

---

## 7. Abuse Consideration: Replay Flood

If attacker floods replay attempts:

- rate limits MUST apply
- session MUST remain stable
- no uncontrolled switching allowed
- deny decisions must be logged (bounded)

---

## Final Statement

Transport volatility increases reattach frequency.

Reattach frequency increases replay risk.

Replay protection is mandatory for any secure
session-centric transport rebinding model.