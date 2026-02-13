# Production Readiness Criteria — Jumping VPN

This document defines the minimum criteria required
before Jumping VPN can be considered production-ready.

This is a gating document.

If these conditions are not satisfied,
the system must not be marketed as production-grade.

---

## 1. Control-Plane Correctness

The following guarantees must be validated under adversarial testing:

- No dual-active transport binding
- No silent identity reset
- No uncontrolled state rollback
- Deterministic rejection on ambiguity
- Explicit reason-coded transitions

Validation required:

- Automated invariant tests
- Failure injection tests
- Replay attack simulation
- Switch amplification attempt simulation

---

## 2. Replay & Freshness Protection

Production implementation must include:

- Cryptographically strong proof-of-possession
- Monotonic nonce tracking
- Bounded replay window
- Reattach freshness validation
- Deterministic replay rejection logging

Preview logic is insufficient.
Cryptographic implementation required.

---

## 3. Rate Limiting & Abuse Resistance

Must demonstrate:

- Per-session reattach rate limits
- Global control-plane rate limits
- Switch cooldown enforcement
- DoS resistance under reattach floods
- Bounded memory under abuse

Benchmarks must prove:

- No unbounded resource growth
- No control-plane amplification

---

## 4. Session Ownership Model

Cluster deployment requires:

- Explicit authoritative ownership model
  - Sticky routing OR
  - Atomic shared store (CAS/transactions)
- Versioned state transitions
- Split-brain rejection logic
- Clear ownership failover strategy

Ambiguous continuation is forbidden.

Consistency must be preferred over unsafe availability.

---

## 5. Data Plane Requirements

Before production:

- Authenticated encryption (AEAD)
- Forward secrecy
- Rekeying policy
- Key rotation schedule
- Secure handshake
- Downgrade protection
- Cryptographic audit

Preview repository does NOT include these.

---

## 6. Observability & Auditability

Production must include:

- Non-blocking logging
- Structured event export
- State transition timeline
- Security event logging
- Rate limit event logging
- Failure classification

Logging failure must not break correctness.

---

## 7. Failure Mode Testing

Must validate:

- Packet loss spikes
- NAT rebinding
- Path asymmetry
- Transport flapping
- Malicious churn
- Cluster node crash during reattach
- Session TTL expiration
- Transport-loss TTL expiration

All outcomes must be explicit and reason-coded.

---

## 8. Performance Validation

Before production claims:

- Benchmark plan executed
- Recovery latency measured (p50/p95/p99)
- Max sustained session count defined
- Memory usage under churn measured
- CPU profile under volatility measured

No marketing numbers without reproducible conditions.

---

## 9. Security Review & Audit

Required before production:

- External security review
- Cryptographic review
- Adversarial threat modeling
- Abuse-case review
- Documentation audit

Security claims must be independently validated.

---

## 10. Deployment Documentation

Production release must include:

- Clear installation guide
- Supported transport matrix
- Supported environments
- Known limitations
- Upgrade path documentation
- Key management instructions

---

## 11. Release Gating Checklist

Production-ready only if:

- All invariants validated under stress
- Replay model cryptographically hardened
- Rate limits proven under abuse
- Cluster ownership proven safe
- Benchmarks reproducible
- Security review completed
- Failure modes documented
- No open critical vulnerabilities

If any critical safety guarantee cannot be met,
the system must fail closed.

---

## 12. Non-Negotiable Principles

Production cannot violate:

- Single session identity anchor
- No dual-active transport binding
- Deterministic state transitions
- Bounded recovery window
- Explicit termination on ambiguity

If a guarantee cannot be upheld,
termination must occur.

---

## Final Principle

Production readiness is not feature completeness.

It is behavioral safety under volatility.

If correctness cannot be guaranteed,
the session must terminate explicitly.

Session is the anchor.  
Transport is volatile.