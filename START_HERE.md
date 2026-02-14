# START HERE — Jumping VPN Protocol Review Entry Point

This repository contains the architectural model and prototype of the Jumping VPN protocol.

This file is the fastest way to understand what this project is, what problem it solves, and where to look first.

---

# What this is

Jumping VPN is a transport-layer protocol designed to preserve session continuity under volatile network conditions.

Core property:

> Session identity remains stable while transports can change.

This allows the protocol to survive:

- packet loss spikes
- jitter instability
- NAT rebinding
- path degradation
- transport failure

without renegotiation or session reset.

The protocol explicitly models:

- session identity as the anchor
- transport as a replaceable attachment
- deterministic state transitions
- auditable transport switching

---

# What this is NOT

This repository is NOT:

- a production-ready VPN
- a finished cryptographic implementation
- a commercial product

This is:

- architectural model
- protocol specification draft
- transport behavior prototype
- review package for engineers and researchers

---

# Core idea in one sentence

Traditional VPNs bind identity to transport.

Jumping VPN binds identity to session.

Transport becomes replaceable.

Session survives.

---

# What problem this solves

Real networks are unstable.

Transport paths degrade, fluctuate, or fail.

Traditional systems often:

- reset connections
- renegotiate identity
- interrupt traffic

Jumping VPN introduces:

- deterministic session continuity
- explicit transport switching
- bounded recovery semantics

---

# Review path (recommended reading order)

If you are reviewing this protocol, read in this order:

---

## 1. Core invariants

Start here:

docs/invariants.md

Defines the fundamental safety and identity guarantees.

These invariants are the foundation of the protocol.

---

## 2. State machine

docs/state-machine.md

Defines all valid states and transitions.

Key states:

- ATTACHED
- VOLATILE
- RECOVERING
- TERMINATED

Transitions are explicit and reason-coded.

---

## 3. Transport vs Session model

docs/session-vs-transport.md

Explains identity anchoring and replaceable transport attachments.

This is the conceptual core of the protocol.

---

## 4. Control-plane reattach flow

docs/control-plane.md

Explains how transport switching happens safely without identity reset.

Includes validation, anti-replay, and ownership checks.

---

## 5. Threat model and security boundaries

docs/security-boundaries.md

Defines what the protocol protects against and what is out of scope.

Includes:

- replay protection model
- identity ownership rules
- attachment validation

---

# Prototype code

Prototype implementation is located in:

poc/

This is NOT production-ready code.

It demonstrates:

- frame protocol structure
- transport abstraction
- telemetry emission
- transport volatility handling

The prototype exists to validate behavioral model, not production deployment.

---

# Observable behavior

Protocol behavior is designed to be observable.

Key observable properties:

- explicit state transitions
- transport switch events
- recovery windows
- identity continuity

This enables:

- debugging
- auditing
- verification

---

# What makes this different

This protocol treats transport volatility as a normal condition, not an error.

Instead of failing, it transitions state and recovers.

Session identity persists.

Transport changes are controlled, bounded, and auditable.

---

# Current status

This repository represents:

- architectural specification
- behavioral model
- prototype transport engine
- review-ready documentation

Not yet included:

- production cryptography
- TUN integration
- production hardening
- full benchmark suite

---

# Why this repository exists

This repository exists for technical review.

It allows engineers to evaluate:

- protocol safety model
- identity semantics
- recovery determinism
- transport abstraction correctness

---

# Author intent

This is an engineering research and protocol design project.

The goal is to explore deterministic session continuity under volatile transport conditions.

---

# Review welcome

Engineers are encouraged to review:

- invariants correctness
- state machine safety
- transport replacement logic
- attack surface

---

# Summary

Jumping VPN is a protocol model where:

Session is stable.  
Transport is replaceable.  
Recovery is explicit.  
Identity persists.

Start reading from docs/invariants.md