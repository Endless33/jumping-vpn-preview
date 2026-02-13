# Jumping VPN — Architecture Overview (Readable Version)

Session is the anchor.  
Transport is volatile.

This document describes the structural model of Jumping VPN
in a reviewer-friendly format.

---

## 1) High-Level Structure

Client Agent
- Session Context (session_id, keys, policy)
- Transport Adapters (UDP / TCP / QUIC)
- Volatility detection
- Reattach initiation

↓

Server Gateway
- Session Table (authoritative ownership)
- TTL enforcement
- State version control (CAS)
- Transport binding validation

↓

Observability Layer (Non-Blocking)
- STATE_CHANGE events
- TRANSPORT_SWITCH events
- SECURITY_EVENT logs
- Export to SIEM / monitoring

---

## 2) Session vs Transport Separation

Session (Identity Anchor)
- session_id (stable)
- cryptographic context (abstracted)
- policy snapshot
- state machine

Transport (Replaceable Attachment)
- ip:port
- protocol
- route / NAT mapping
- quality metrics (loss / latency / jitter)

Transport death does NOT imply session death  
(within TTL and policy bounds).

---

## 3) State Model

States:

BIRTH  
ATTACHED  
VOLATILE  
DEGRADED  
RECOVERING  
TERMINATED  

Rules:

- Transitions are explicit
- Every mutation increments state_version
- Ambiguity fails closed
- Dual-active transport is forbidden

---

## 4) Reattach Flow (Simplified)

1) Transport failure detected  
2) Session enters RECOVERING  
3) Client sends REATTACH_REQUEST  
4) Server validates:
   - session exists
   - TTL valid
   - proof-of-possession valid
   - nonce fresh
   - state_version matches
   - no dual-active conflict
5) Server binds new transport  
6) Session returns to ATTACHED  

If validation fails → explicit REJECT or TERMINATE.

No silent resets.

---

## 5) Cluster Ownership (Conceptual)

Two safe models:

A) Sticky routing  
SessionID maps to a single authoritative node.

B) Shared atomic store  
CAS-based state_version prevents dual binding.

Consistency is preferred over ambiguous continuation.

---

## Final Principle

Control-plane correctness is more important than transport survival.

If correctness cannot be guaranteed,
the session must terminate explicitly.

Session is the anchor.  
Transport is volatile.