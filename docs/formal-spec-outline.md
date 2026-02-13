# Jumping VPN — Formal Behavioral Specification (Outline)

Status: Draft  
Version: 0.1-preview  
Scope: Session continuity under transport volatility

This document outlines a formal behavioral contract
for Jumping VPN.

It is structured in RFC-style sections for clarity and review.

---

# 1. Terminology

The following terms are normative:

- MUST
- MUST NOT
- SHOULD
- SHOULD NOT
- MAY

These are to be interpreted as described in RFC 2119.

---

# 2. System Model

The system consists of:

- A Client Agent
- A Server Gateway
- An optional Cluster Ownership Layer
- A Policy Engine

The system operates over one or more volatile transport paths.

---

# 3. Core Abstractions

## 3.1 Session

A Session is defined as:

- A stable identity anchor (SessionID)
- A cryptographic context
- A policy context
- A versioned state

A Session MUST exist independently of any single transport.

---

## 3.2 Transport

A Transport is:

- A temporary binding
- A delivery channel
- A replaceable attachment

Transport MAY change without mutating session identity.

---

# 4. State Machine

The following states are defined:

- BIRTH
- ATTACHED
- VOLATILE
- DEGRADED
- RECOVERING
- TERMINATED

All transitions MUST be:

- Explicit
- Deterministic
- Reason-coded
- Logged (non-blocking)

No implicit state transitions are allowed.

---

# 5. Invariants

The following invariants MUST hold:

1. At most one active transport binding per session.
2. SessionID MUST NOT change across transport reattach.
3. No dual-active binding is permitted.
4. Recovery MUST be bounded by policy.
5. All critical transitions MUST be auditable.
6. Ambiguous ownership MUST result in rejection.

Violation of invariants MUST result in termination
or deterministic rejection.

---

# 6. Transport Death Detection

Transport is considered DEAD when:

- No successful delivery occurs within TransportLossTTL
- OR health metrics exceed policy-defined thresholds

Transport death MUST trigger:

- RECOVERING state
- Explicit REATTACH flow

Silent fallback is forbidden.

---

# 7. Reattach Procedure

The client MUST send:

- SessionID
- Proof-of-possession
- Freshness marker
- Optional metadata

The server MUST:

- Validate ownership
- Validate proof-of-possession
- Validate freshness window
- Enforce rate limits
- Enforce TTL constraints

If validation succeeds:

- Bind new transport
- Emit TransportSwitch event
- Transition to ATTACHED

If validation fails:

- Emit explicit failure event
- Remain in bounded state
- Terminate if policy requires

---

# 8. Policy Constraints

Policy MUST define:

- MaxRecoveryWindowMs
- MaxSwitchesPerMinute
- TransportLossTTL
- SessionTTL
- Quality thresholds (loss/latency/jitter)

Policy MUST be deterministic and reproducible.

---

# 9. Anti-Replay Requirements

Reattach MUST enforce:

- Freshness validation
- Replay window tracking
- Deterministic rejection of stale proofs

Replay attempts MUST NOT mutate session state.

---

# 10. Cluster Ownership

If deployed in a cluster:

The system MUST implement one of:

- Sticky routing (SessionID → node)
- Atomic shared store with versioned CAS

Split-brain MUST result in reattach denial.

Dual-active identity is forbidden.

---

# 11. Failure Semantics

If recovery exceeds policy bounds:

Session MUST enter:

- DEGRADED
OR
- TERMINATED

Undefined states are forbidden.

Silence is forbidden.

---

# 12. Observability Requirements

The system MUST emit:

- STATE_CHANGE
- TRANSPORT_SWITCH
- SECURITY_EVENT (if applicable)

Observability MUST NOT block correctness.

Logging failure MUST NOT alter state.

---

# 13. Non-Goals (Normative)

The protocol does NOT guarantee:

- Global anonymity
- Endpoint compromise protection
- Censorship bypass guarantees
- Side-channel resistance
- Data-plane cryptographic specification (in this draft)

---

# 14. Security Philosophy

Security is defined as:

- Bounded behavior
- Deterministic transitions
- Explicit ownership
- Invariant preservation

Heuristic-only adaptation is forbidden.

---

# 15. Future Extensions (Non-Normative)

- Multi-hop chains under invariant preservation
- QUIC transport integration
- Formal verification feasibility
- High-churn benchmarking
- Distributed ownership scaling

These extensions MUST preserve core invariants.

---

Session is the anchor.  
Transport is volatile.  
Behavior must be deterministic.