# Control Plane — Formal Specification (Preview)

Status: Formal Draft  
Scope: Deterministic session lifecycle control  

This document defines the formal behavioral contract of the Jumping VPN control plane.

It specifies:

- Message structure
- Validation requirements
- Deterministic transition triggers
- Rejection rules
- Version semantics
- Safety guarantees

This document does NOT define:
- Packet encryption
- Framing format
- Transport multiplexing
- Data-plane payload

The control plane governs session identity and transport binding only.

---

# 1. Control Plane Goals

The control plane MUST guarantee:

1. Explicit state transitions
2. Single active transport binding
3. Version-safe mutation
4. Deterministic rejection on ambiguity
5. Bounded recovery
6. Fail-closed behavior

Correctness is strictly preferred over availability.

---

# 2. Message Envelope

All control-plane messages MUST follow this envelope:

{
  "ts_ms": int64,
  "message_type": string,
  "session_id": string,
  "state_version": int,
  "payload": object
}

Field semantics:

- ts_ms:
  Unix timestamp (ms). Used for logging and freshness checks.

- message_type:
  Deterministic classification.

- session_id:
  Stable identity anchor.

- state_version:
  Monotonic version required for mutation safety.

- payload:
  Message-specific content.

Missing or malformed required fields → REJECT.

---

# 3. Message Types

## 3.1 HANDSHAKE_INIT

Direction: Client → Server  
Purpose: Create new session.

Payload:
{
  "client_nonce": int,
  "requested_policy": object (optional)
}

Server must:
- Validate structure
- Allocate SessionID
- Initialize state_version = 0
- Enter ATTACHED

Response:
HANDSHAKE_ACK

---

## 3.2 HANDSHAKE_ACK

Direction: Server → Client  

Payload:
{
  "assigned_session_id": string,
  "policy_snapshot": object,
  "initial_state_version": int
}

Transition:
BIRTH → ATTACHED

---

## 3.3 TRANSPORT_DEAD (Signal)

Direction: Internal or Client-triggered  
Purpose: Declare active transport unusable.

Transition:
ATTACHED → RECOVERING

Requirements:
- Increment state_version
- Emit audit event

---

## 3.4 REATTACH_REQUEST

Direction: Client → Server  

Payload:
{
  "nonce": int,
  "proof": string,
  "candidate": {
      "transport_id": string,
      "remote_ip": string,
      "remote_port": int,
      "proto": string
  }
}

Server MUST validate:

- session exists
- session not TERMINATED
- state_version matches expected
- TTL not expired
- nonce freshness valid
- proof-of-possession valid
- no dual-active conflict
- ownership authority valid

Possible outcomes:

REATTACH_ACK  
REATTACH_REJECT

No silent acceptance allowed.

---

## 3.5 REATTACH_ACK

Direction: Server → Client  

Payload:
{
  "new_state_version": int,
  "reason": "REATTACH_SUCCESS"
}

Transition:
RECOVERING → ATTACHED

Must increment version.

---

## 3.6 REATTACH_REJECT

Direction: Server → Client  

Payload:
{
  "reason": string
}

Possible transitions:

RECOVERING → DEGRADED  
RECOVERING → TERMINATED  

Policy-defined.

Rejection MUST be explicit and reason-coded.

---

## 3.7 TERMINATE

Direction: Either side  

Payload:
{
  "reason": string
}

Transition:
ANY → TERMINATED

TERMINATED is final.

---

# 4. Version Semantics

Let V be state_version.

Rules:

1. Successful transition:
   V_new = V_old + 1

2. Rejected mutation:
   V remains unchanged

3. If incoming state_version < current:
   REJECT (stale event)

4. If incoming state_version > current:
   REJECT (future state)

Version rollback is forbidden.

---

# 5. Deterministic Rejection Rules

Server MUST reject when:

- state_version mismatch
- session does not exist
- session already TERMINATED
- nonce replay detected
- proof-of-possession invalid
- TTL expired
- dual-active binding attempt
- ownership ambiguity detected

All rejections must:

- Include reason_code
- Emit audit event
- Leave state unchanged (unless policy mandates termination)

---

# 6. Replay Protection Model

Replay protection requires:

- Monotonic client nonce
- Server-side replay window
- Reject stale nonce
- Reject reused nonce
- Freshness validated before binding

Replay validation MUST occur before transport binding.

---

# 7. Safety Properties

The control plane must guarantee:

- No silent identity reset
- No implicit state transitions
- No dual-active binding
- No ambiguous continuation
- Deterministic outcome for each message

If correctness cannot be guaranteed:
Terminate explicitly.

---

# 8. Cluster Ownership Model

Production deployment requires:

- Sticky routing (SessionID → node)
OR
- Atomic shared store with versioned CAS updates

If ownership ambiguity detected:
REJECT or TERMINATE.

Never allow dual-active.

---

# 9. Failure Handling

Transport-level failure:
→ RECOVERING

TTL expiration:
→ TERMINATED

Ownership conflict:
→ REJECT or TERMINATE

Security violation:
→ TERMINATED

Ambiguity is forbidden.

---

# 10. Non-Goals

This control-plane spec does NOT define:

- Data-plane encryption
- Packet framing
- Obfuscation layer
- Kernel integration
- Traffic anonymization

It defines behavioral determinism only.

---

# 11. Formal Properties (Verification Targets)

Future formal modeling should verify:

- Deterministic transition mapping
- No dual-active reachable
- Version monotonicity
- Absorbing TERMINATED state
- Bounded recovery window

Suggested tools:

- TLA+
- Alloy
- PlusCal

---

# Final Principle

Control-plane correctness
is more important than transport survival.

If correctness cannot be proven,
the session must terminate explicitly.

Session is the anchor.  
Transport is volatile.