# Jumping VPN — Security Binding Requirements (Abstract)

Status: Normative Security Contract (Public Preview)

This document defines the mandatory validation semantics
for binding a new transport to an existing session.

Cryptographic primitives are abstracted.
Behavioral checks are normative.

---

## 1. Objective

A new transport may be bound to an existing session only if:

- the requester proves possession of valid session secrets
- the request is fresh (anti-replay)
- the session is within TTL boundaries
- policy permits the operation
- the binding is atomic and auditable

---

## 2. Reattach Validation Contract

### 2.1 Inputs (Logical)

A reattach request MUST include logically:

- SessionID
- Proof-of-possession (PoP)
- Freshness marker (nonce/counter/timestamp)
- Protocol version
- Transport metadata (candidate binding info)

Exact wire format is implementation-defined.

---

## 3. Mandatory Checks (Normative)

The server MUST perform the following checks in order:

### B1 — Session Existence
- Lookup SessionID in Session Table.
- If missing: deny.

Reason:
- `unknown_session`

---

### B2 — Session State Validity
Reattach is allowed only if:

- state ∈ {VOLATILE, DEGRADED, RECOVERING}
- state ≠ TERMINATED

If state is invalid: deny.

Reason:
- `invalid_state_for_reattach`

---

### B3 — Session TTL Validity
If `session_age_ms > SESSION_MAX_LIFETIME_MS`: deny.

Reason:
- `session_expired`

---

### B4 — Transportless TTL Validity
If `transportless_age_ms > TRANSPORT_LOST_TTL_MS`: deny.

Reason:
- `transport_ttl_exceeded`

---

### B5 — Proof-of-Possession (PoP)
Proof MUST validate against the session's security context.

If PoP invalid: deny.

Reason:
- `bad_proof`

---

### B6 — Freshness / Replay Protection
Freshness marker MUST be:

- within acceptance window
- not previously seen (replay cache/window)

If freshness invalid: deny.

Reason:
- `replay_detected` or `stale_request`

---

### B7 — Policy Authorization
Policy MUST permit:

- transport class (udp/quic/etc.)
- switching at this time (rate limits/cooldown)
- recovery window not exceeded

If denied: deny.

Reason:
- `policy_denied`

---

### B8 — Candidate Transport Sanity
Transport metadata MUST pass basic sanity:

- allowed protocol
- not blacklisted
- not violating configured constraints

If invalid: deny.

Reason:
- `invalid_transport_candidate`

---

## 4. Atomic Binding Rule (Normative)

If all checks pass:

- binding MUST be applied atomically:
  - active_transport updated
  - state transition RECOVERING → ATTACHED
  - state_version incremented
- TransportSwitch MUST be emitted

If atomicity cannot be guaranteed:
- deny and log
- do not partially mutate state

Reason:
- `atomicity_failed`

---

## 5. Cluster Consistency Rule (Normative)

In clustered deployments:

- reattach must validate against latest state_version
- stale state updates must be rejected
- dual acceptance must be prevented

If version mismatch:
- deny

Reason:
- `stale_state_version`

---

## 6. Failure Handling

On any denial:

- the session MUST NOT change active transport binding
- the denial MUST be logged
- security-related denials MUST emit a security event

Recommended behavior:

- RECOVERING → DEGRADED on repeated validation failures

---

## 7. Observability Requirements

Every reattach attempt MUST emit:

- `ReattachAttempt`

Every result MUST emit:

- `ReattachResult` with:
  - status: SUCCESS | DENIED
  - reason_code

Security-related denials must emit:

- `SecurityReplayDetected` (if replay)
- `SecurityValidationFailed` (if proof invalid)

---

## 8. Minimal Reason Code Set

Recommended stable reason codes:

- unknown_session
- invalid_state_for_reattach
- session_expired
- transport_ttl_exceeded
- bad_proof
- replay_detected
- stale_request
- policy_denied
- invalid_transport_candidate
- atomicity_failed
- stale_state_version

---

## Final Statement

Transport volatility increases reattach frequency.

Reattach frequency increases attack surface.

Security binding defines the boundary:

Without valid binding,
transport switching becomes hijackable.

Jumping VPN requires explicit, deterministic validation
for every transport reattachment.