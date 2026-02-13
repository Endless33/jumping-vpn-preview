# Control Plane Protocol — Behavioral Contract (Preview)

This document defines the abstract control-plane protocol used by Jumping VPN.

It specifies:

- Message types
- Required fields
- Transition triggers
- Deterministic outcomes
- Rejection rules

This is a behavioral contract.
It does NOT define encryption, framing, or packet formats.

---

## 1. Design Goals

The control-plane must guarantee:

- Explicit state transitions
- Bounded recovery
- Version-safe mutation
- Deterministic rejection
- Single active transport binding

The protocol must fail closed.

---

## 2. Message Envelope

All messages follow this structure:

{
  "ts_ms": 1700000000000,
  "message_type": "STRING",
  "session_id": "STRING",
  "state_version": 12,
  "payload": {}
}

Field meanings:

ts_ms — Unix timestamp (ms)  
message_type — classification  
session_id — stable identity  
state_version — monotonic counter  
payload — message-specific content  

---

## 3. Core Messages

### HANDSHAKE_INIT

Client → Server  
Purpose: create session

Payload:

{
  "client_nonce": 1,
  "requested_policy": {}
}

Server replies:

HANDSHAKE_ACK  
SESSION_CREATED  

Transition:

BIRTH → ATTACHED

---

### TRANSPORT_DEAD

Signal: transport unusable

Transition:

ATTACHED → RECOVERING

Must increment state_version.

---

### REATTACH_REQUEST

Client → Server

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

Server validates:

- session exists
- TTL valid
- proof valid
- nonce fresh
- no dual-active conflict
- state_version matches

Possible responses:

REATTACH_ACK  
REATTACH_REJECT  

---

### REATTACH_ACK

RECOVERING → ATTACHED

Must bind transport atomically.

---

### REATTACH_REJECT

RECOVERING → DEGRADED  
or  
RECOVERING → TERMINATED  

Rejection must be explicit.

---

### TERMINATE

ANY → TERMINATED

Termination is final.

---

## 4. Version Semantics

Every successful transition:

- increments state_version
- rejects stale versions
- prevents rollback

Rollback is forbidden.

---

## 5. Deterministic Rejection

Server must reject if:

- state_version mismatch
- invalid proof
- nonce replay
- TTL expired
- dual-active binding attempt
- ownership ambiguity

Rejection must be reason-coded.

---

## 6. Replay Protection

- Monotonic client nonce
- Server replay window
- Reject reused nonce
- Freshness validated before binding

---

## 7. Failure Rules

Transport failure → RECOVERING  
TTL expired → TERMINATED  
Ambiguity → REJECT or TERMINATE  

Never:

- silently reset identity
- mutate without transition
- allow dual binding

---

Final principle:

Control-plane correctness is more important than transport survival.

Session is the anchor.  
Transport is volatile.