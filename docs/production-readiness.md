# Production Readiness Plan — Jumping VPN

This document outlines the concrete steps required
to move from architectural validation to production-grade deployment.

This repository does NOT claim production readiness.

It defines what production would require.

---

## 1. Cryptographic Hardening

Required before production:

- Replace placeholder proof-of-possession with real asymmetric crypto
- Key lifecycle management (rotation, expiration, revocation)
- Secure randomness source validation
- Constant-time comparison for sensitive operations
- Formal anti-replay window implementation

Target: externally reviewable crypto module.

---

## 2. Transport Abstraction Layer

Required:

- UDP adapter (baseline)
- TCP fallback adapter
- QUIC transport experiment
- Pluggable transport interface
- Transport health telemetry hooks

Transport must remain replaceable.

---

## 3. Cluster-Safe Session Ownership

Production requires one of:

Option A:
Sticky routing (SessionID → node)

Option B:
Atomic shared store (CAS + versioning)

Must guarantee:

- No dual-active binding
- No ownership ambiguity
- Deterministic rejection on conflict

---

## 4. Observability Integration

Production requires:

- Structured JSON logs
- Export to SIEM
- Correlation ID per session
- Switch reason codes
- Recovery latency metrics

Observability must not block correctness.

---

## 5. Benchmarking & Load Testing

Before production:

- Controlled packet-loss simulation
- NAT churn simulation
- 10k+ concurrent session tests
- Reattach flood resilience testing
- Switch-rate abuse simulation

Benchmarks must be reproducible.

---

## 6. Security Review

Required:

- External audit of control-plane logic
- Replay protection verification
- State-machine correctness review
- Abuse-case modeling
- Formal threat boundary validation

No marketing claims before external review.

---

## 7. Pilot Deployment Requirements

Production pilot must define:

- Target environment (mobile / fintech / edge)
- Failure model (loss %, jitter, churn)
- Acceptable recovery window
- Maximum switch rate
- Audit visibility requirements

Success criteria must be measurable.

---

## Engineering Principle

Correctness > Liveness  
Consistency > Availability  
Determinism > Convenience  

If correctness cannot be guaranteed,
the session must terminate explicitly.

Session is the anchor.  
Transport is volatile.