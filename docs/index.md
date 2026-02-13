# Jumping VPN — Documentation Index

This document provides a structured navigation map
for the Jumping VPN architectural preview.

Estimated full review time:
30–60 minutes.

---

# 1. Start Here

If you are reviewing for the first time:

1) architecture-overview.md  
2) state-machine.md  
3) invariants.md  

These define the core behavioral contract.

---

# 2. Concept & Rationale

- protocol-rationale.md  
- comparative-analysis.md  

These explain:

- Why Jumping VPN exists
- How it differs from WireGuard / IPsec / QUIC
- What problem it is solving

---

# 3. Formal Specification Layer

- formal-spec-outline.md  
- formal-properties.md  
- state-machine.md  
- invariants.md  

Defines:

- Explicit state transitions
- Hard invariants
- Deterministic guarantees
- Bounded recovery model

---

# 4. Security Model

- threat-model.md  
- security-model-deep-dive.md  
- attack-scenarios.md  

Covers:

- Adversary assumptions
- Replay handling
- Reattach safety
- Cluster ownership safety
- Abuse and DoS scenarios

---

# 5. Production Perspective

- reference-implementation-outline.md  
- production-readiness-checklist.md  
- production-readiness-gap.md  

Clarifies:

- What exists architecturally
- What is missing for production
- Honest boundary of current stage

---

# 6. Evaluation Framework

- integration-evaluation.md  
- benchmark-plan.md  
- test-scenarios.md  

Defines:

- How to evaluate determinism
- How to test volatility
- What measurable artifacts should exist
- How to compare against baseline VPNs

---

# 7. Whitepaper Draft

- whitepaper-draft.md  

Narrative version of the architecture,
suitable for higher-level technical review.

---

# 8. Mutation Logs

Located in:

docs/MutationLogs/

These document architectural evolution
and behavioral reasoning over time.

---

# 9. Proof of Concept

Located in:

poc/

Includes:

- real_udp_prototype.py
- demo.py
- supporting modules

Purpose:

Demonstrate behavioral claim:

Session survives transport death
without silent identity reset.

This is not production crypto.

---

# 10. Repository Scope Reminder

This repository represents:

Architectural validation.

It does not represent:

- Production-grade VPN release
- Hardened distributed system
- Performance-certified implementation
- Cryptographic audit

---

# 11. Review Philosophy

The architecture should be evaluated against:

- Deterministic behavior
- Explicit state transitions
- Bounded recovery
- No dual-active ambiguity
- No silent identity reset
- Clear failure semantics

If these hold,
the behavioral model is internally coherent.

---

Session is the anchor.  
Transport is volatile.  
Determinism is the goal.