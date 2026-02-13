# Control Plane Protocol — Behavioral Contract (Preview)

This document defines the abstract control-plane protocol
used by Jumping VPN for session lifecycle management.

It specifies:

- Message types
- Required fields
- Transition triggers
- Deterministic outcomes
- Rejection rules

This is a behavioral contract.
It does not define packet encryption or framing.

---

# 1. Design Goals

The control-plane must guarantee:

- Explicit state transitions
- Bounded recovery
- Version-safe mutation
- Deterministic rejection on ambiguity
- Single active transport binding

The protocol must fail closed.

---

# 2. Message Envelope

All control-plane messages follow this envelope:

```json
{
  "ts_ms": 1700000000000,
  "message_type": "STRING",
  "session_id": "STRING",
  "state_version": 12,
  "payload": {}
}

Field definitions:
Field
Required
Description
ts_ms
yes
Unix timestamp (ms)
message_type
yes
Message classification
session_id
yes
Stable session identity
state_version
yes
Monotonic state version
payload
yes
Message-specific content
3. Core Message Types
3.1 HANDSHAKE_INIT
Client → Server
Purpose: Create new session.
Payload:

{
  "client_nonce": 1,
  "requested_policy": {}
}

Server response:
HANDSHAKE_ACK
SESSION_CREATED
3.2 HANDSHAKE_ACK
Server → Client
Payload:

{
  "assigned_session_id": "abc123",
  "policy_snapshot": {},
  "initial_state_version": 0
}

Transition

BIRTH → ATTACHED

3.3 TRANSPORT_DEAD (Signal)
Internal or Client-triggered.
Purpose: Declare current transport unusable.
Transition:

ATTACHED → RECOVERING

Must increment state_version.
3.4 REATTACH_REQUEST
Client → Server
Payload:

{
  "nonce": 42,
  "proof": "POP_SIGNATURE",
  "candidate": {
    "transport_id": "uuid",
    "remote_ip": "x.x.x.x",
    "remote_port": 443,
    "proto": "udp"
  }
}

Server must validate:
session exists
TTL not expired
proof-of-possession valid
nonce freshness valid
no dual-active conflict
version matches expected
Possible outcomes:
REATTACH_ACK
REATTACH_REJECT
3.5 REATTACH_ACK
Server → Client
Payload:

{
  "new_state_version": 13,
  "reason": "REATTACH_SUCCESS"
}

Transition:

RECOVERING → ATTACHED

3.6 REATTACH_REJECT
Server → Client
Payload:

{
  "reason": "TTL_EXPIRED"
}

Possible transitions:

RECOVERING → DEGRADED
RECOVERING → TERMINATED

Never silent continuation.
3.7 TERMINATE
Server or Client-triggered.
Payload:

{
  "reason": "SESSION_TTL_EXPIRED"
}

Transition:

ANY → TERMINATED

Termination is final.
4. Version Semantics
Every successful transition:
Must increment state_version
Must reject stale state_version updates
Must use CAS logic server-side
Version rollback is forbidden.
5. Deterministic Rejection Rules
Server MUST reject if:
state_version mismatch
proof-of-possession invalid
nonce replay detected
TTL expired
dual-active binding attempt
ownership ambiguity detected
Rejection must be explicit and reason-coded.
6. Replay Protection Model (Preview)
Monotonic client nonce
Server-side replay window
Reject stale nonce
Reject reused nonce
Freshness must be enforced before binding.
7. Failure Behavior
Transport-level failure: → RECOVERING
TTL expiration: → TERMINATED
Ambiguous ownership: → REJECT or TERMINATE
Never:
silently reset identity
downgrade state without transition
allow dual binding
8. Non-Goals
This control-plane protocol does NOT define:
Data-plane encryption
Framing format
Packet multiplexing
Kernel hooks
Obfuscation layer
It defines behavioral determinism only.
Final Principle
Control-plane correctness is more important than transport survival.
If correctness cannot be guaranteed, the session must terminate explicitly.
Session is the anchor. Transport is volatile.