# API Contract — Jumping VPN (Preview)

This document defines the minimal API/contract surface
for integrating with Jumping VPN’s control-plane behavior.

This is a contract-first specification.

It is NOT a claim of a finished production API.

---

## 1) Contract Principles

The API must preserve:

- Deterministic state transitions
- Explicit rejection paths
- Monotonic state_version
- Bounded recovery behavior
- Single active transport binding

If correctness cannot be guaranteed:
terminate explicitly.

---

## 2) Data Types (Conceptual)

SessionID:
- stable identifier for session identity

StateVersion:
- monotonic integer
- increments on every successful transition

ReasonCode:
- deterministic classification for transitions/rejections

TransportCandidate:
- transport_id
- proto (udp/tcp/quic)
- remote_ip
- remote_port
- optional metadata

PolicySnapshot:
- session_ttl_ms
- transport_loss_ttl_ms
- max_recovery_window_ms
- max_switches_per_min
- cooldown_ms
- replay_window_size

---

## 3) Control-Plane Messages

All messages share this envelope:

{
  "ts_ms": 1700000000000,
  "message_type": "STRING",
  "session_id": "STRING",
  "state_version": 0,
  "payload": {}
}

No message may mutate state unless:
- state_version is valid
- replay freshness is valid
- ownership is authoritative (cluster mode)

---

## 4) API Surface (Behavioral)

### 4.1 Create Session

HANDSHAKE_INIT (Client → Server)

payload:
{
  "client_nonce": 1,
  "requested_policy": {}
}

HANDSHAKE_ACK (Server → Client)

payload:
{
  "assigned_session_id": "abc123",
  "policy_snapshot": {},
  "initial_state_version": 0
}

Outcome:
BIRTH → ATTACHED

---

### 4.2 Declare Transport Death

TRANSPORT_DEAD (Signal)

payload:
{
  "reason_code": "NO_DELIVERY_WINDOW"
}

Outcome:
ATTACHED → RECOVERING

Rule:
state_version must increment.

---

### 4.3 Reattach (Bind New Transport)

REATTACH_REQUEST (Client → Server)

payload:
{
  "nonce": 42,
  "proof": "PROOF_OF_POSSESSION",
  "candidate": {
    "transport_id": "uuid",
    "proto": "udp",
    "remote_ip": "x.x.x.x",
    "remote_port": 443,
    "metadata": {}
  }
}

Validation gates:
- session exists
- TTL valid
- proof valid (external crypto module)
- nonce fresh (anti-replay)
- no dual-active binding
- state_version matches expected
- ownership authoritative

Server responses:

REATTACH_ACK

payload:
{
  "new_state_version": 13,
  "reason_code": "REATTACH_SUCCESS"
}

Outcome:
RECOVERING → ATTACHED

or

REATTACH_REJECT

payload:
{
  "reason_code": "TTL_EXPIRED"
}

Outcome:
RECOVERING → DEGRADED
or RECOVERING → TERMINATED

Rule:
Rejection must be explicit and reason-coded.

---

### 4.4 Terminate Session

TERMINATE (Server or Client)

payload:
{
  "reason_code": "SESSION_TTL_EXPIRED"
}

Outcome:
ANY → TERMINATED

Termination is final.

---

## 5) Event Stream Contract (Observability)

Integrators may consume an event stream.

Events must be structured, reason-coded, and non-blocking.

Minimum events:

- SESSION_CREATED
- STATE_CHANGE
- TRANSPORT_SWITCH
- REATTACH_SUCCESS
- REATTACH_REJECT
- SECURITY_EVENT
- RATE_LIMIT_EVENT
- TTL_EXPIRED

Event emission must not affect correctness.

---

## 6) Deterministic Error Categories

The API must expose explicit error categories:

- INVALID_STATE_VERSION
- NONCE_REPLAY
- NONCE_STALE
- PROOF_INVALID
- SESSION_NOT_FOUND
- SESSION_TTL_EXPIRED
- TRANSPORT_LOSS_TTL_EXPIRED
- OWNERSHIP_AMBIGUOUS
- RATE_LIMITED
- POLICY_DENIED
- DUAL_BIND_FORBIDDEN

All errors must be reason-coded.

---

## 7) Backwards Compatibility Rules

Future versions must:

- Preserve envelope fields
- Add new fields as optional
- Introduce new message types explicitly
- Preserve invariant semantics

No breaking changes without version bump.

---

## 8) Non-Goals

This contract does NOT define:

- Encryption primitives
- Packet framing
- Data-plane formats
- Kernel integration
- Anonymity or obfuscation guarantees

Scope is:
Deterministic control-plane behavior for session continuity.

---

## Final Principle

The API contract must make behavior predictable:

- explicit transitions
- explicit failures
- bounded recovery
- auditable decisions

Session is the anchor.
Transport is volatile.