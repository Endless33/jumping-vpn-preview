# Jumping VPN — Architecture Overview (Public Preview)

This document provides a high-level map of the Jumping VPN architecture.
It describes responsibilities by layer and where key behavioral guarantees live.

This is a public preview and does not expose hardened implementation details.

---

## 1) Design Goal

Jumping VPN is built for environments where transport volatility is normal:

- mobile networks (Wi-Fi ↔ LTE)
- NAT rebinding and timeouts
- packet loss spikes and jitter
- path degradation and flapping

The primary goal is **session continuity** under volatility,
with **bounded adaptation** and **auditable behavior**.

---

## 2) System Layers

Jumping VPN can be understood as layered responsibilities:

### Layer A — Session Core (Source of Truth)
Responsibility:
- Create and maintain the session identity
- Own the session lifecycle state machine
- Enforce invariants (what must always remain true)

Key outputs:
- Session state transitions: `BIRTH → ATTACHED → ...`
- Deterministic termination boundaries

Artifacts:
- `docs/state-machine.md`
- `docs/invariants.md`

---

### Layer B — Transport Binding (Ephemeral)
Responsibility:
- Bind a concrete transport (IP:port + protocol) to an existing session
- Replace transports without resetting the session
- Track active vs candidate transports

Key outputs:
- Explicit transport switches (`TransportSwitch`)
- Bounded switching behavior (anti-flapping)

Artifacts:
- `docs/state-machine.md`
- `docs/test-scenarios.md`

---

### Layer C — Policy Engine (Bounded Adaptation)
Responsibility:
- Decide when switching is allowed
- Enforce rate limits, cooldowns, and thresholds
- Convert environment volatility into controlled behavior

Examples:
- maximum switch rate per minute
- degrade thresholds
- recovery windows
- allowed transport classes

Artifacts:
- `docs/roadmap.md`
- `docs/design-decisions.md`

---

### Layer D — Observability & Audit (Operator Grade)
Responsibility:
- Emit structured events for critical decisions
- Provide traceability for SOC/NOC review
- Make adaptation explainable

Expected event types:
- `SessionStateChange`
- `TransportSwitch`
- `TransportSwitchDenied`
- `SessionTerminated`

Artifacts:
- `docs/security-review-plan.md`
- `docs/threat-model.md`

---

### Layer E — Security Binding (Session Integrity)
Responsibility:
- Ensure reattachment is safe
- Prevent hijacking/fixation/replay during recovery
- Bind session identity to cryptographic proof (hardened layer)

Note:
This preview intentionally does not expose hardened cryptographic internals.

Artifacts:
- `docs/threat-model.md`
- `docs/security-review-plan.md`

---

## 3) Key Architectural Separations

### Session ≠ Transport
- Session is persistent identity and policy context.
- Transport is a replaceable binding.

Transport death does not imply session death (within bounds).

### Adaptation ≠ Chaos
- Switching is bounded by policy.
- Oscillation is prevented with dampening and rate limits.

### Recovery ≠ Renegotiation
- Recovery is an explicit state transition.
- No hidden identity reset is allowed.

---

## 4) Primary Behavioral Guarantees (High-Level)

Jumping VPN is defined by behavior over time:

- Session identity persists across transport changes (within TTL/policy bounds)
- Transport switching is explicit and reason-coded
- Adaptation is bounded (anti-flapping)
- Failure boundaries are deterministic
- Critical decisions are auditable

---

## 5) What This Repository Contains

This repository focuses on:

- Architectural documentation
- Threat model and limitations
- State machine definitions
- Test scenarios
- Minimal behavioral PoC(s)

It does not contain a production-hardened VPN implementation.

---

## Summary

Jumping VPN is a behavioral system for volatile networks:

- Session is the anchor
- Transport is disposable
- Volatility is modeled as state
- Adaptation is bounded and auditable