# Jumping VPN — FAQ (Architectural & Technical)

This document answers common technical and architectural questions
regarding the public preview of Jumping VPN and its underlying concepts.

This repository contains architectural intent and staged documentation.
It does not contain the full hardened implementation.

---

## 1. What problem is Jumping VPN trying to solve?

Modern networks are volatile:

- Mobile IPs change unexpectedly
- Packet loss spikes occur frequently
- NAT bindings expire
- Cross-border routing degrades
- Paths flap under load

Traditional VPNs often treat these events as failures,
triggering renegotiation or session resets.

Jumping VPN models volatility as a first-class protocol state,
allowing deterministic recovery without destroying session identity.

---

## 2. How is this different from WireGuard?

WireGuard optimizes for simplicity and performance
under relatively stable transport assumptions.

Jumping VPN separates:

- Session identity
- Transport lifetime

Transport failure does not imply session termination.

The architectural distinction is session persistence
across transport volatility.

This is not a modification of WireGuard.
It is a different state model.

---

## 3. Is this multi-path routing?

No.

Multi-path focuses on simultaneous path usage.
Jumping VPN focuses on transport volatility management.

The goal is deterministic session continuity
when transports degrade, disappear, or compete.

Volatility is modeled explicitly in state transitions.

---

## 4. Does this replace existing VPN protocols?

Not necessarily.

Jumping VPN represents a behavioral model.
It can coexist with or be layered alongside existing VPN technologies.

The focus is transport abstraction and session lifecycle control,
not encryption reinvention.

---

## 5. Is this production-ready?

No.

This repository represents:

- Architectural modeling
- State transition design
- Conceptual lifecycle behavior
- Controlled demo logic

Security hardening, formal audit, and production implementation
are staged development goals.

---

## 6. What cryptographic primitives are used?

This public repository does not expose
final cryptographic implementation details.

The design principles include:

- Session-bound identity
- Replay resistance
- Deterministic reattachment validation
- Key lifecycle constraints

Cryptographic implementation is subject to future audit.

---

## 7. How does Jumping VPN prevent session hijacking during reattachment?

Reattachment must be cryptographically bound to session identity.

Transport origin alone is never trusted.

Reattachment requires proof of possession of session-bound keys
and must satisfy bounded policy constraints.

Full implementation details are not exposed in this preview.

---

## 8. How are oscillating transports handled?

Transport switching is policy-bounded.

Mechanisms may include:

- Switch rate limits
- Stability scoring
- Cooldown intervals
- Explicit dampening logic

Adaptation must be explainable and reversible.

Uncontrolled oscillation is treated as instability,
not resilience.

---

## 9. What is the failure model?

Failure is classified into states such as:

- ATTACHED
- VOLATILE
- DEGRADED
- RECOVERING
- TERMINATED

Hard failure and soft degradation are treated differently.

The protocol prioritizes deterministic convergence
over silent retry loops.

---

## 10. Is this an anonymity system?

No.

Jumping VPN is focused on transport volatility
and session continuity.

It does not claim to replace Tor or anonymity networks.

Privacy characteristics depend on deployment context.

---

## 11. What does the demo represent?

The mock session demo:

- Simulates lifecycle transitions
- Demonstrates state evolution
- Shows deterministic recovery behavior

It does not perform real routing or encryption.

It is a conceptual behavioral illustration.

---

## 12. Why is the full source code not published?

This repository is a staged architectural preview.

Full implementation release is aligned with:

- Security review
- Hardened core completion
- Controlled development milestones

The public goal is transparency of direction,
not premature exposure of incomplete components.

---

## 13. Who is this project intended for?

Jumping VPN may be relevant to:

- Infrastructure teams managing volatile mobile environments
- Fintech platforms experiencing failover instability
- Security architects modeling deterministic recovery
- Engineers exploring transport abstraction layers

---

## 14. Is this a commercial product?

Not in its current state.

This repository documents architectural intent
and staged development.

Future deployment models may include:

- Enterprise licensing
- Strategic partnerships
- Controlled pilot integrations

No public SaaS is offered at this stage.

---

## 15. How can technical discussions begin?

For architectural or technical discussions,
you may reach out via:

📧 riabovasvitalijus@gmail.com

Please include context about your infrastructure
or volatility challenges.

---

## Final Note

Jumping VPN is not positioned as a silver bullet.

It is an attempt to model transport instability
as a structured, auditable, and deterministic behavior layer.

The session remains the anchor.
Transports come and go.