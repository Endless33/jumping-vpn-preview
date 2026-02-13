# Jumping VPN — Review Index

Welcome.

This repository is an architectural preview of Jumping VPN —
a session-centric model for deterministic recovery under transport volatility.

This document provides a structured entry point
for engineers, architects, and reviewers.

---

## 1. What This Is

Jumping VPN models transport instability as a first-class state.

Core thesis:

- Session is the anchor.
- Transport is replaceable.
- Recovery is bounded.
- Transitions are explicit.
- Failures are deterministic.

This repository focuses on behavioral correctness —
not marketing claims.

---

## 2. What This Is NOT

This is not:

- A production VPN release
- A hardened cryptographic implementation
- A full routing stack
- An anonymity network
- A censorship bypass system

It is an architectural validation repository.

---

## 3. Recommended Reading Order

For a complete review:

### Step 1 — Architectural Overview
- `README.md`
- `docs/architecture-overview.md`

### Step 2 — Behavioral Model
- `docs/state-machine.md`
- `docs/invariants.md`
- `docs/control-plane-protocol.md`
- `docs/api-contract.md`

### Step 3 — Security Model
- `docs/threat-model.md`
- `docs/security-boundaries.md`
- `docs/security-review-checklist.md`
- `docs/production-readiness-criteria.md`

### Step 4 — Operational Model
- `docs/benchmark-plan.md`
- `docs/test-scenarios.md`
- `docs/evidence-log.md`
- `docs/integration-guide.md`

### Step 5 — Minimal Behavioral PoC
- `poc/real_udp_prototype.py`
- `poc/README_udp.md`

### Step 6 — Core Skeleton
- `core/common/`
- `core/session/`
- `core/server/`
- `core/client/`
- `core/security/`
- `core/metrics/`

---

## 4. What To Evaluate

When reviewing this architecture, focus on:

- Deterministic state transitions
- Monotonic versioning
- Dual-active prevention
- Replay rejection
- Rate limiting bounds
- Recovery window enforcement
- TTL semantics
- Explicit termination behavior

If ambiguity exists,
the system must reject or terminate.

---

## 5. Key Safety Invariants

The following must never be violated:

- Single active transport per session
- No silent identity reset
- No uncontrolled state rollback
- No implicit state transitions
- No ambiguous ownership

All transitions must be reason-coded and auditable.

---

## 6. Open Engineering Areas

The repository openly documents areas under exploration:

- Cluster ownership model
- Formal verification feasibility
- High-churn scalability
- QUIC-based transport experiments
- Benchmark reproducibility

These are not hidden gaps.
They are active research directions.

---

## 7. Production Status

Jumping VPN is currently in:

Architectural Validation Phase.

The repository contains:

- Formal behavioral model
- Control-plane contract
- Security boundaries
- Review checklist
- Benchmark plan
- Evidence log template
- Minimal UDP behavioral PoC
- Production-readiness gating criteria

It does NOT contain:

- Hardened crypto
- Full data-plane implementation
- Production deployment package

---

## 8. Review Philosophy

This architecture invites:

- Adversarial questioning
- Invariant stress testing
- Failure injection analysis
- Abuse-case review

Claims without evidence are invalid.

Evidence without reproducibility is insufficient.

---

## 9. Contact

For technical discussion or review:

riabovasvitalijus@gmail.com

---

## Final Principle

Modern networks are volatile.

A protocol must not collapse under expected instability.

Session is the anchor.  
Transport is volatile.