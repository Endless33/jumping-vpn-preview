# What Would a Production Build Look Like? — Jumping VPN

Status: Conceptual  
Scope: Production-oriented architecture outline  
This document does NOT claim a production implementation exists.

It describes what a hardened, production-grade version would require.

---

# 1. Production Goals

A production build must provide:

- Deterministic session continuity
- Bounded recovery behavior
- Cluster-safe ownership model
- Hardened replay protection
- Auditable state transitions
- Measurable performance

Not optional.

---

# 2. Production Architecture Overview

## 2.1 Control Plane (Authoritative Layer)

Responsibilities:

- Session lifecycle management
- State machine enforcement
- Versioned transitions (CAS/atomic update)
- TTL enforcement
- Reattach validation
- Replay window management
- Rate limiting

Must be:

- Deterministic
- Transaction-safe
- Observable
- Fail-closed

---

## 2.2 Data Plane (Encrypted Channel)

Would require:

- Authenticated encryption (AEAD)
- Key rotation policy
- Per-session key context
- Rekey on transport change (if required)
- Forward secrecy

Not defined in preview repository.

---

## 2.3 Session Ownership Model

Production must define one of:

Option A:
Sticky routing (SessionID → node)

Option B:
Distributed atomic store with:
- Version counter
- CAS semantics
- Ownership lock
- Split-brain detection

Consistency must be preferred over availability.

---

## 2.4 Replay Protection

Production build must:

- Use cryptographically secure nonce validation
- Maintain bounded replay window
- Expire old nonces deterministically
- Log rejected attempts

Replay logic must be O(1)-ish per session.

---

## 2.5 Rate Limiting & Abuse Control

Must include:

- Per-session reattach limits
- Global control-plane limits
- Backoff policies
- Abuse detection hooks

Control-plane flooding must not cause:

- Unbounded switching
- State corruption
- Memory growth

---

## 2.6 Observability Layer

Production must emit:

- Session lifecycle events
- Transport switch events
- Recovery latency metrics
- Replay rejection counters
- Policy-triggered transitions

Logging must be:

Non-blocking  
Resilient  
Exportable to SIEM  

Failure of logging must not break correctness.

---

# 3. Hardening Requirements

A real production release must include:

- Memory bounds per session
- Session table eviction policy
- Formal invariant tests
- Fuzz testing of control-plane
- Replay edge-case testing
- Churn simulation harness
- Version conflict simulation

---

# 4. Scalability Targets

To claim production readiness:

- 10k+ concurrent sessions
- Bounded per-session memory
- Bounded CPU per mutation
- No linear growth on replay window
- Stable behavior under churn

Benchmarks must be reproducible.

---

# 5. Security Hardening

Production must include:

- Hardened cryptographic primitives
- Secure key storage
- Zero-trust network assumptions
- Secure control-plane framing
- Constant-time validation where applicable

None of these are claimed in preview repository.

---

# 6. Failure Guarantees in Production

Production build must guarantee:

- No dual-active transport binding
- No silent identity reset
- Deterministic termination on ambiguity
- Bounded recovery window
- Version-safe state transitions

If any invariant cannot be preserved,
the session must terminate explicitly.

---

# 7. Deployment Modes

Potential deployment models:

- Edge gateway cluster
- Enterprise perimeter appliance
- Cloud-hosted control-plane
- Hybrid mobile-edge environment

All require:

Clear ownership model  
Policy tuning  
Recovery SLA definition  

---

# 8. What Production Is NOT

Production is not:

- “It works in a lab”
- “It survives one failover”
- “It reconnects most of the time”

Production is:

Deterministic under stress  
Measured under churn  
Auditable under load  

---

# 9. Production Readiness Checklist (High-Level)

Before release:

- Control-plane fuzz tested
- Replay logic audited
- Rate limiter stress tested
- Session table memory profiled
- Failover under packet loss benchmarked
- Cluster ownership tested under partition
- Security review completed
- External audit performed

---

# 10. Engineering Reality

A real production build is:

- Multi-quarter effort
- Security review heavy
- Integration-intensive
- Test-driven
- Infrastructure-aware

The preview repository describes the model.

Production would require:

Engineering team  
Test infrastructure  
Security review  
Deployment discipline  

---

# Final Statement

Jumping VPN preview defines:

Behavioral contract  
Deterministic state model  
Volatility handling rules  

A production build would:

Harden it  
Measure it  
Prove it  
Operate it safely  

Session is the anchor.  
Transport is volatile.  
Production requires discipline.