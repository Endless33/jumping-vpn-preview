# Jumping VPN — Whitepaper Outline (Draft)

Status: Structural Outline  
Purpose: Define the structure of a formal whitepaper based on current repository state  

This document describes how the architectural preview can evolve
into a formal technical whitepaper.

It does not claim academic publication readiness.
It defines structure, scope, and content boundaries.

---

# 1. Abstract

Short summary (1 page max):

- Problem: Transport volatility causes session collapse
- Observation: Many VPN systems bind identity to transport
- Proposal: Session-centric deterministic recovery model
- Contribution:
  - Formal state machine
  - Explicit invariants
  - Bounded adaptation policy
  - Deterministic recovery semantics
  - Auditable transitions

---

# 2. Problem Statement

## 2.1 Modern Network Volatility

- Packet loss spikes
- NAT churn
- Mobile network switching
- Cross-border instability
- Asymmetric routing
- Path flapping

## 2.2 Failure of Traditional Assumptions

Most VPNs assume:
- Stable path
- Stable endpoint
- Implicit renegotiation acceptable

Observed issue:
Transport failure frequently triggers:
- Session reset
- Identity renegotiation
- Re-authentication
- Silent corruption risk

---

# 3. Core Thesis

Session identity must not be transport-bound.

We separate:

- Session identity (logical continuity)
- Transport binding (physical path)

Transport becomes replaceable.
Session remains the anchor.

---

# 4. Formal Model

## 4.1 State Machine

States:
- BIRTH
- ATTACHED
- VOLATILE
- RECOVERING
- DEGRADED
- TERMINATED

Transitions:
- Explicit
- Versioned
- Reason-coded
- Deterministic

## 4.2 Version Semantics

- state_version is monotonic
- CAS-based mutation
- No rollback allowed
- Stale updates rejected

## 4.3 Invariants

- Single active transport
- No dual-active binding
- No silent identity reset
- Bounded recovery window
- Deterministic rejection on ambiguity

---

# 5. Control Plane Model

## 5.1 Message Envelope

Defines:
- ts_ms
- session_id
- state_version
- message_type
- payload

## 5.2 Core Messages

- HANDSHAKE_INIT
- HANDSHAKE_ACK
- TRANSPORT_DEAD
- REATTACH_REQUEST
- REATTACH_ACK
- REATTACH_REJECT
- TERMINATE

## 5.3 Deterministic Rejection Rules

Explicit rejection required for:
- Version mismatch
- Replay detection
- TTL expiry
- Dual binding attempt
- Ownership ambiguity

---

# 6. Recovery Semantics

## 6.1 Bounded Recovery Window

Recovery must complete within policy-defined bounds.
Otherwise:
TERMINATED (explicit).

## 6.2 Anti-Flap Protection

- Switch rate limits
- Cooldown windows
- Hysteresis
- Multi-signal gating

## 6.3 Degraded Mode

Allows limited continuity
without uncontrolled switching.

---

# 7. Threat Model

Assumptions:

- On-path attacker can observe and disrupt
- Replay attempts possible
- Transport churn can be maliciously induced
- Control-plane abuse possible

Non-goals:

- Endpoint compromise defense
- Tor-level anonymity
- Obfuscation layer
- Anti-forensics guarantees

---

# 8. Safety & Security Properties

- Identity continuity under transport death
- No dual-active session binding
- Replay protection enforced
- Version-safe mutation
- Explicit termination on failure

---

# 9. Implementation Outline

Reference modules:

- Client agent
- Gateway
- Session store
- Policy engine
- Anti-replay window
- Rate limiter
- Recovery metrics

Implementation boundaries are defined.
Crypto primitives are out-of-scope in preview.

---

# 10. Evaluation Plan

## 10.1 Deterministic Test Cases

- Invariant tests
- Replay tests
- Churn tests
- TTL expiration tests
- Concurrency tests

## 10.2 Benchmark Plan

Metrics:
- Recovery latency
- Switch rate
- Termination rate
- CPU overhead
- Memory footprint

## 10.3 Pilot Template

Defined in:
docs/pilot-evaluation-template.md

---

# 11. Comparison with Existing Systems

Not equivalent to:

- Traditional OpenVPN behavior
- Standard WireGuard reconnection
- Basic QUIC migration

The distinction lies in:
formal session-layer determinism
and bounded behavioral guarantees.

---

# 12. Limitations

- Not production crypto
- Not formally verified
- No real-world benchmark data yet
- No distributed cluster implementation yet

These are staged roadmap items.

---

# 13. Open Research Questions

- Distributed ownership consensus
- Formal verification model (TLA+/Ivy/Coq)
- Multi-hop behavior under strict invariants
- Performance under 10k+ session churn
- QUIC transport integration

---

# 14. Conclusion

Transport volatility is not an anomaly.

It is the baseline condition of modern networks.

Correctness must dominate continuity.

If correctness cannot be guaranteed,
the system must fail explicitly.

Session is the anchor.  
Transport is volatile.  
Determinism is non-negotiable.