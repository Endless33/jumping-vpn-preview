# Comparative Analysis — Jumping VPN vs Existing Models

This document compares Jumping VPN’s behavioral model
against common transport and VPN approaches.

The purpose is not marketing.
It is architectural contrast.

---

# 1. Comparison Scope

We compare:

- WireGuard
- IPsec (IKEv2)
- QUIC (connection migration)
- Jumping VPN (behavioral model)

The comparison focuses on:

- Identity model
- Transport binding behavior
- Volatility handling
- Deterministic guarantees
- Failure semantics
- Cluster safety assumptions

---

# 2. WireGuard

## Identity Model

- Static key-based peer identity
- Transport binding strongly tied to endpoint

## Transport Volatility Handling

- Supports roaming via endpoint update
- Relies on handshake + keepalive

## Behavior Under Transport Death

- Requires re-establishing handshake
- Session continuity depends on rekey and handshake logic
- Implicit transport rebinding

## Observability

- Minimal event-level state exposure
- Not designed for SOC-grade behavioral auditing

## Cluster Model

- No built-in session ownership abstraction
- Requires external load balancing / routing strategy

---

# 3. IPsec (IKEv2)

## Identity Model

- Security Associations (SA)
- Tied to negotiated tunnel

## Transport Volatility Handling

- MOBIKE supports address changes
- Still SA-bound model

## Behavior Under Transport Failure

- Re-negotiation often required
- Heavily dependent on timers and negotiation logic

## Determinism

- Complex state machine
- Many implementation variations

## Observability

- Depends on vendor implementation
- Often opaque at state-transition level

---

# 4. QUIC (Connection Migration)

## Identity Model

- Connection ID abstraction
- Transport-level migration support

## Transport Volatility Handling

- Designed for path migration
- Handles NAT rebinding

## Scope Limitation

- Operates at transport layer
- Does not define session-level invariants
- Does not define policy-bounded recovery semantics
- Does not address cluster ownership safety

QUIC solves path migration.
It does not define behavioral session doctrine.

---

# 5. Jumping VPN

## Identity Model

- Session identity is independent of transport
- Session is the anchor
- Transport is a replaceable binding

## Transport Volatility Handling

- Explicit volatility states
- Policy-bound adaptation
- Deterministic reattach semantics

## Behavior Under Transport Death

- Explicit RECOVERING state
- Reattach request with proof-of-possession
- Bounded recovery window
- Deterministic termination if bounds exceeded

## Hard Invariants

- Single active transport
- No silent identity reset
- Versioned state transitions
- Bounded switch rate
- Explicit termination semantics

## Cluster Model

- Requires authoritative ownership model
- Dual-active binding forbidden
- Consistency preferred over availability

---

# 6. Behavioral Contrast Summary

| Property                        | WireGuard | IPsec | QUIC | Jumping VPN |
|----------------------------------|-----------|--------|------|-------------|
| Transport Migration              | Partial   | Partial | Yes  | Yes         |
| Session-Level Invariants         | No        | Limited | No   | Yes         |
| Explicit Volatility States       | No        | No     | No   | Yes         |
| Bounded Recovery Window          | Implicit  | Timer-based | No | Yes |
| Anti-Flap Policy Model           | No        | No     | No   | Yes |
| Deterministic Termination Model  | Limited   | Complex | No | Yes |
| Cluster Ownership Doctrine       | External  | Vendor | No | Yes |
| SOC-Grade Auditability           | Minimal   | Vendor | No | Yes |

---

# 7. Architectural Positioning

Jumping VPN is not:

- A replacement for QUIC
- A replacement for WireGuard
- A drop-in IPsec competitor

It introduces:

A session-centric behavioral layer
that models volatility explicitly.

It can theoretically operate
above or alongside existing transports.

---

# 8. Design Tradeoff

Jumping VPN trades:

Simplicity of minimal transport model

for

Explicit behavioral determinism
and policy-bound adaptation.

It adds complexity at control layer
to reduce ambiguity at failure boundaries.

---

# 9. Honest Limitation

Jumping VPN does not claim:

- Better raw performance than WireGuard
- Better cryptographic minimalism than QUIC
- Lower complexity than traditional VPN stacks

Its value proposition is:

Deterministic session continuity
under volatile transport conditions.

---

# 10. Final Comparison Principle

Traditional VPNs assume stability
and recover from instability.

Jumping VPN assumes instability
and encodes it into its behavior.

That is the core distinction.

---

Session is the anchor.  
Transport is volatile.  
Determinism is the differentiator.