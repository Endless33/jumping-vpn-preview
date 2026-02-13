# Protocol Rationale — Why Jumping VPN Exists

This document explains the architectural motivation
behind Jumping VPN.

It clarifies why this model exists,
what problem it addresses,
and how it differs from traditional VPN approaches.

---

# 1. The Problem Landscape

Most VPN protocols were designed for:

- Stable networks
- Predictable routing
- Fixed endpoints
- Long-lived transport bindings

Modern reality is different:

- Mobile handovers
- Carrier NAT churn
- Cross-border path instability
- Frequent packet loss spikes
- Dynamic routing changes
- Volatile last-mile connectivity

Traditional VPNs treat volatility as failure.

Jumping VPN treats volatility as state.

---

# 2. What Breaks in Traditional Models

When transport fails in many VPN systems:

- Session renegotiation occurs
- Identity may reset
- Clients re-authenticate
- State may partially collapse
- Failover is heuristic

The architectural assumption:

Transport = Identity anchor

When transport dies, identity often follows.

---

# 3. Architectural Inversion

Jumping VPN flips the model:

Session = Identity anchor  
Transport = Replaceable binding

Transport death does not imply session death.

Volatility is not exceptional.
It is modeled explicitly in the state machine.

---

# 4. Why Not Just Use QUIC?

QUIC supports connection migration.

However:

- QUIC operates at transport layer
- It does not define session-level invariants
- It does not define policy-bounded adaptation
- It does not formalize cluster ownership
- It does not define deterministic termination semantics

Jumping VPN operates above transport:

It defines:

- Explicit session state machine
- Hard safety invariants
- Policy-driven recovery bounds
- Auditable transitions
- Deterministic failure semantics

QUIC can be a transport candidate.
It is not the behavioral layer.

---

# 5. Why Not Just Use Multi-Hop?

Multi-hop improves path diversity,
but does not inherently solve:

- Session identity continuity
- Dual-active binding safety
- Deterministic reattach semantics
- Anti-flap control
- Explicit failure boundaries

Multi-hop without bounded policy
can amplify ambiguity.

Jumping VPN requires:

Single authoritative session identity
under bounded adaptation.

---

# 6. Core Differentiator

Jumping VPN is not defined by encryption.

It is defined by:

Behavior under stress.

Specifically:

- Explicit volatility modeling
- Deterministic reattachment
- No silent identity reset
- No dual-active ambiguity
- Bounded recovery window
- Policy-driven adaptation

It is a behavioral protocol model.

---

# 7. What This Is Not

Jumping VPN is not:

- A censorship bypass system
- An anonymity network
- A Tor replacement
- A stealth transport protocol
- A marketing wrapper around QUIC

It is a session-continuity architecture
for volatile transport environments.

---

# 8. Intended Use Cases

- Mobile-first fintech platforms
- Edge computing environments
- Cross-border enterprise systems
- Carrier-volatile regions
- High-mobility field deployments

Where:

Session continuity matters more than path persistence.

---

# 9. Engineering Position

Jumping VPN introduces:

A session-centric behavioral abstraction layer
over unstable transport substrates.

It defines correctness in terms of:

Deterministic identity continuity.

---

# 10. Final Rationale

Modern networks are volatile by default.

Protocols that assume stability
inherit fragility.

Jumping VPN assumes volatility
and encodes it explicitly into behavior.

It does not fight instability.
It models it.

---

Session is the anchor.  
Transport is volatile.  
Continuity must be deterministic.