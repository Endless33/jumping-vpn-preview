# Jumping VPN — Development Roadmap

This roadmap outlines the staged development plan
for Jumping VPN from architectural validation
to controlled enterprise readiness.

Dates are indicative and may adjust based on validation outcomes.

---

## Phase 0 — Architectural Validation (Current)

Status: In Progress

Focus:
- Session-centric state modeling
- Transport abstraction design
- Deterministic recovery guarantees
- Failure classification framework

Deliverables:
- Mutation Logs
- Architecture documentation
- FAQ and One-Pager
- Conceptual demo

Outcome:
Clear architectural direction
and defined behavioral guarantees.

---

## Phase 1 — Core Session Engine (Months 1–3)

Focus:
- Session lifecycle implementation
- Transport binding abstraction
- Explicit state transitions
- Policy-bounded reattachment logic

Deliverables:
- Session state machine implementation
- Transport interface (UDP baseline)
- Reattachment validation logic
- Local volatility simulator

Validation:
- Session continuity across transport loss
- No uncontrolled renegotiation
- Deterministic state convergence

---

## Phase 2 — Volatility Handling & Observability (Months 4–6)

Focus:
- Degradation modeling
- Anti-oscillation controls
- Observability hooks

Deliverables:
- VOLATILE / DEGRADED state handling
- Transport scoring and dampening logic
- Structured event logs
- Metrics export (state changes, switches)

Validation:
- Stable behavior under packet loss
- Bounded switch rate
- Explainable recovery paths

---

## Phase 3 — Security Hardening & Review (Months 7–9)

Focus:
- Session integrity
- Replay resistance
- Reattachment security

Deliverables:
- Session-bound key lifecycle
- Replay protection enforcement
- Independent security review (planned)
- Threat model refinement

Validation:
- Reattachment rejection under invalid proof
- No session fixation
- Deterministic failure under attack simulation

---

## Phase 4 — Controlled Pilot Deployments (Months 10–12)

Focus:
- Real-world validation
- Performance benchmarking
- Integration readiness

Deliverables:
- Pilot deployments in controlled environments
- Performance metrics (latency, overhead)
- Integration documentation
- Deployment patterns

Validation:
- Measured reattachment latency
- Session survival rate under volatility
- Operational observability feedback

---

## Phase 5 — Enterprise Readiness (Post-Pilot)

Focus:
- Stability
- Documentation
- Support model

Deliverables:
- Versioned release candidate
- Deployment guides
- Support & maintenance model
- Enterprise licensing discussions

---

## Roadmap Principle

Each phase must demonstrate:
- Predictable behavior
- Measurable outcomes
- Clear failure boundaries

Progression is validation-driven,
not feature-driven.