# Jumping VPN — Formal Specification Outline (Preview)

Status: Draft  
Intended audience: protocol engineers, reviewers, system architects  
Scope: Session lifecycle and transport volatility behavior  

This document outlines a formal-style specification for Jumping VPN’s
session-centric control model.

It defines normative requirements using RFC-style terminology.

---

# 1. Terminology

The key words:

MUST  
MUST NOT  
SHOULD  
SHOULD NOT  
MAY  

are to be interpreted as described in RFC 2119.

---

# 2. System Model

Jumping VPN defines a session-layer control model independent of transport.

The system consists of:

- Session identity (persistent within bounds)
- Transport binding (replaceable)
- Deterministic state machine
- Policy-constrained recovery model

The session is the identity anchor.

---

# 3. Session Object

A session MUST include:

- session_id (stable identifier)
- state (enumerated)
- state_version (monotonic counter)
- active_transport (nullable)
- policy (bounded configuration)
- ttl parameters
- replay protection context

The session_id MUST NOT change across transport reattachment.

---

# 4. State Model

The following states are defined:

- BIRTH
- ATTACHED
- VOLATILE
- DEGRADED
- RECOVERING
- TERMINATED

State transitions MUST be:

- explicit
- reason-coded
- versioned
- auditable

Silent transitions are forbidden.

---

# 5. State Version Semantics

Every successful state mutation:

MUST increment state_version by exactly +1.

A mutation attempt with stale state_version:

MUST be rejected.

Rollback of state_version is forbidden.

---

# 6. Transport Binding Rules

At any time:

A session MUST have at most one ACTIVE transport.

During reattachment:

- Previous transport MUST be deactivated
- New transport MUST be validated
- Binding MUST be atomic
- state_version MUST increment

Dual-active binding is forbidden.

---

# 7. Transport Failure Semantics

Transport death is defined as:

No viable delivery within bounded observation window.

Upon detection:

ATTACHED → RECOVERING

Transition MUST:

- be explicit
- include reason_code
- increment state_version

---

# 8. Reattach Procedure

A REATTACH_REQUEST MUST include:

- session_id
- state_version
- proof-of-possession
- freshness marker (nonce)
- candidate transport metadata

Server MUST validate:

- session existence
- TTL validity
- proof-of-possession
- nonce freshness
- ownership authority
- state_version match

Failure MUST result in explicit rejection.

No silent acceptance.

---

# 9. Recovery Bound

Recovery MUST be bounded by:

- max_recovery_window_ms
- max_switches_per_window
- cooldown constraints

If recovery exceeds defined bounds:

Session MUST transition to:

DEGRADED or TERMINATED

No infinite retry loops are permitted.

---

# 10. Replay Protection

Client nonce MUST be monotonic.

Server MUST maintain replay window.

If nonce reuse is detected:

Request MUST be rejected.

Replay rejection MUST NOT mutate session state.

---

# 11. TTL Semantics

Two TTL values MUST exist:

1. session_ttl
2. transport_loss_ttl

If session_ttl expires:

Session MUST terminate.

If transport_loss_ttl expires during recovery:

Session MUST terminate.

Termination MUST be explicit.

---

# 12. Cluster Ownership

In multi-node deployments:

A session MUST have authoritative ownership.

Acceptable models:

- Sticky routing (SessionID → node)
- Atomic shared store (CAS/transactional update)

If ownership ambiguity is detected:

Reattach MUST be rejected.

Consistency is preferred over availability.

---

# 13. Failure Behavior

Under the following conditions:

- state_version mismatch
- dual-active conflict
- invalid proof
- nonce replay
- TTL expiry
- ownership ambiguity

The system MUST:

Reject deterministically  
Emit reason-coded error  
Avoid silent mutation  

---

# 14. Observability Requirements

All critical transitions MUST emit:

- event_type
- session_id
- state_version
- reason_code
- timestamp

Logging failure MUST NOT block state transitions.

---

# 15. Non-Goals

This specification does NOT define:

- data-plane encryption format
- packet framing
- multiplexing layer
- anonymity guarantees
- censorship bypass techniques

It defines behavioral determinism only.

---

# 16. Security Boundary

The protocol assumes:

An attacker MAY:

- observe transport metadata
- disrupt connectivity
- inject replay attempts

The protocol MUST guarantee:

- identity continuity within policy bounds
- no silent reset
- no ambiguous dual continuation
- deterministic rejection under ambiguity

---

# 17. Determinism Principle

Given identical:

- prior state
- input message
- policy configuration
- time constraints

The system MUST produce identical:

- state transition
- output decision
- rejection reason

Randomness MUST NOT influence state transitions.

---

# 18. Termination Rule

If correctness cannot be guaranteed:

The session MUST terminate explicitly.

Survivability MUST NOT override safety invariants.

---

# 19. Versioning

Future revisions MUST:

- preserve core invariants
- maintain backward compatibility where feasible
- explicitly version new message types
- avoid altering determinism guarantees

---

# 20. Final Statement

Jumping VPN formalizes volatility at the session layer.

Transport instability is modeled behavior.

Identity continuity is bounded and deterministic.

Session is the anchor.  
Transport is volatile.  
Correctness is non-negotiable.