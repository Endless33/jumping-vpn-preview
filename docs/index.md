# Jumping VPN — Documentation Portal

This directory contains the full architectural, behavioral, and demo‑level
documentation for the Jumping VPN protocol.

The documentation is divided into two major layers:

- **Core** — protocol architecture, invariants, state machine, security, rationale  
- **Demo** — contract‑first demonstration package with scenario, output format, and validation tools

---

# 1. Core Architecture (`docs/core/`)

Foundational documents describing how Jumping VPN works at the protocol level.

### Lifecycle & Behavior
- `state-machine.md`
- `invariants.md`
- `reconnect.md`
- `reason-codes.md`
- `control-plane-sequence.md`

### Security & Threat Modeling
- `security-boundary.md`
- `threat-model.md`
- `attack-scenarios.md`
- `security-review-plan.md`

### Performance & Evaluation
- `performance-model.md`
- `benchmark-plan.md`
- `integration-evaluation.md`

### Design Rationale
- `protocol-rationale.md`
- `design-decisions.md`
- `comparative-analysis.md`
- `comparison-model.md`
- `limitations.md`
- `non-goals.md`

### Use Cases & Scenarios
- `use-case-fintech-failover.md`
- `test-scenarios.md`

### Roadmap
- `roadmap.md`
- `production-readiness-checklist.md`
- `production-readiness-gap.md`

---

# 2. Demo Package (`docs/demo/`)

A contract‑first demonstration of Jumping VPN behavior.

### Specification & Behavior
- `DEMO_SPEC.md`
- `DEMO_SCENARIO.md`
- `DEMO_OUTPUT_FORMAT.md`

### Validation & Status
- `STATUS.md`
- `REVIEW_CHECKLIST.md`

### Expected Output
- `DEMO_TIMELINE.jsonl`

### Demo Index
- `README.md`

---

# 3. Mutation Logs (`docs/MutationLogs/`)

Chronological logs describing protocol evolution, conceptual mutations,
and architectural shifts.

---

# Summary

This documentation set defines:

- the protocol  
- the invariants  
- the reconnect model  
- the security boundary  
- the demo contract  
- the expected behavior  
- the roadmap  

Jumping VPN is identity‑anchored and transport‑volatile.