# Protocol Evolution Plan — Jumping VPN

This document defines how Jumping VPN evolves
without breaking invariants or destabilizing deployments.

Evolution must be controlled.
Mutation must be bounded.

---

# 1. Core Rule

No protocol evolution may violate:

- Single active transport binding
- Deterministic state transitions
- Version monotonicity
- Explicit failure semantics
- Bounded recovery windows

If a proposed change weakens these,
it is rejected.

---

# 2. Evolution Stages

Protocol evolution occurs in structured stages:

Stage 1 — Behavioral Validation
Stage 2 — Controlled Extension
Stage 3 — Distributed Hardening
Stage 4 — Performance Refinement
Stage 5 — Cryptographic Hardening

This repository is currently:
Stage 1 → Stage 2 transition.

---

# 3. Stage 1 — Behavioral Validation (Current)

Focus:

- Formal state machine
- Explicit invariants
- Deterministic rejection rules
- Minimal PoC
- Replay protection modeling
- Anti-flap logic

Goal:

Prove the session-centric volatility model is internally coherent.

No optimization.
No premature scaling.
No feature expansion.

---

# 4. Stage 2 — Controlled Extension

Possible extensions:

- Multi-hop (bounded)
- QUIC transport adapter
- Policy engine refinement
- Versioned state serialization
- Structured telemetry export

All extensions must:

- Preserve safety invariants
- Be policy-bounded
- Be measurable

---

# 5. Stage 3 — Distributed Hardening

Focus:

- Authoritative session ownership
- CAS-based state mutation
- Split-brain resolution rules
- Explicit cluster rejection logic

Cluster support must:

Prefer rejection over ambiguity.

---

# 6. Stage 4 — Performance Refinement

Focus:

- Replay window optimization
- Session table memory bounding
- Control-plane rate limiting tuning
- Recovery latency optimization

Performance must remain:

Deterministic.
Policy-driven.
Auditable.

---

# 7. Stage 5 — Cryptographic Hardening

Focus:

- Production-grade key lifecycle
- Rekey-on-policy triggers
- Strong proof-of-possession design
- Freshness validation hardening

Cryptography must:

Bind session identity strictly.
Prevent replay.
Prevent hijack.

---

# 8. Backward Compatibility Rules

If future revisions modify:

- Control-plane message schema
- State transitions
- Replay window semantics

Then:

- Versioning required
- Explicit migration path required
- Old sessions must terminate safely
- No implicit silent upgrades

---

# 9. Mutation Governance

All mutations must be:

- Documented
- Reasoned
- Versioned
- Tested against invariants

No feature is added for novelty.

All features must answer:

Does this preserve deterministic recovery?

---

# 10. Deprecation Model

Deprecated behaviors must:

- Be explicitly documented
- Be version-gated
- Be removed in staged manner
- Never silently change semantics

---

# 11. Stability Threshold

Jumping VPN enters stability phase when:

- State machine frozen
- Invariants formally reviewed
- Threat assumptions validated
- Benchmark plan executed
- Recovery behavior verified under churn

Until then:

Architecture is evolving.
Invariants are not negotiable.

---

# 12. Philosophy

The protocol does not evolve to chase trends.

It evolves to:

- Reduce ambiguity
- Reduce undefined behavior
- Reduce uncontrolled volatility
- Increase deterministic reasoning

---

# Final Principle

Evolution must never break the anchor.

Session identity is stable.
Transport behavior mutates.

The anchor must not move.