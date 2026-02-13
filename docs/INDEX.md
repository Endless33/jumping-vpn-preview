# Jumping VPN — Architecture Index

Status: Architectural Validation  
Purpose: Reviewer Navigation Map  

This index provides a structured entry point for engineers,
architects, and reviewers.

The repository is organized around deterministic behavior
under transport volatility.

---

# 1. Start Here

If you are reviewing this architecture for the first time:

1) README.md  
2) docs/architecture-overview.md  
3) docs/state-machine.md  
4) docs/formal-invariants-machine-readable.md  

These define the core model.

---

# 2. Behavioral Core

- docs/state-machine.md
- docs/invariants.md
- docs/formal-invariants-machine-readable.md
- docs/determinism-proof-outline.md
- docs/control-plane-protocol.md

Focus: deterministic session lifecycle.

---

# 3. Failure & Volatility Modeling

- docs/failure-matrix.md
- docs/fault-injection-strategy.md
- docs/resource-model.md
- docs/scalability-model.md
- docs/threat-evolution-scenarios.md
- docs/what-would-make-this-fail.md

Focus: behavior under stress.

---

# 4. Security & Safety

- docs/threat-model.md
- docs/security-boundaries.md
- docs/attack-surface-map.md
- docs/security-review-checklist.md
- docs/consistency-model.md

Focus: invariant preservation.

---

# 5. Operational & Deployment

- docs/deployment-model.md
- docs/operational-playbook.md
- docs/production-readiness-criteria.md
- docs/pilot-evaluation-template.md
- docs/real-world-evaluation-plan.md

Focus: real-world viability.

---

# 6. Implementation Outline

- docs/reference-implementation-outline.md
- core/
- poc/
- docs/api-contract.md
- docs/integration-guide.md

Focus: module boundaries and minimal prototype.

---

# 7. Benchmark & Evidence

- docs/benchmark-plan.md
- docs/evidence-log.md

Focus: measurable validation.

---

# 8. Open Questions

- Distributed session ownership
- Cluster synchronization model
- QUIC transport experiments
- Formal verification feasibility
- High-churn 10k+ sessions performance validation

These are active exploration areas — not omissions.

---

# 9. Architectural Position

Jumping VPN is:

- Session-centric
- Transport-agnostic
- Deterministic
- Bounded
- Auditable

It is not:

- An anonymity network
- A censorship bypass claim
- A finished product release

---

# 10. Reviewer Guidance

If you are evaluating this system:

Focus on:

- Invariant preservation
- Bounded recovery
- Version monotonicity
- Single-active transport enforcement
- Deterministic rejection logic

If any invariant cannot be enforced,
the architecture must be reconsidered.

---

# Final Orientation

Session is the anchor.  
Transport is volatile.  
Determinism defines correctness.

This repository documents that constraint model.