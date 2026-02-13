# Security Boundary Definition — Jumping VPN (Preview)

This document defines the explicit security boundaries of Jumping VPN.

It clarifies what the protocol guarantees —
and what is outside its responsibility.

---

# 1. Responsibility Layer

Jumping VPN operates at the session and transport-binding layer.

It is responsible for:

- Session identity persistence
- Deterministic transport switching
- Bounded recovery behavior
- Explicit state transitions
- Audit visibility of adaptation

It does NOT operate at:

- Application payload security (handled by TLS or higher layers)
- Endpoint OS security
- User authentication systems
- Physical infrastructure security

---

# 2. Trust Boundaries

## Trusted Components

- Session state machine
- Cryptographic binding logic
- Policy enforcement layer
- Cluster ownership resolution

## Semi-Trusted Components

- Transport paths (assumed volatile)
- Network infrastructure
- Load balancers

## Untrusted Components

- Internet transit
- Adversarial network actors
- Packet manipulation
- Traffic shaping or disruption

---

# 3. Explicit Threat Assumptions

The protocol assumes:

- Transport can fail at any time
- Packet loss spikes are normal
- Paths can degrade unpredictably
- NAT rebinding occurs
- Active disruption is possible

The protocol does NOT assume:

- Infinite recovery opportunity
- Perfect network reliability
- Adversary absence

---

# 4. What Jumping VPN Defends Against

Within scope:

- Session collapse due to transport volatility
- Identity reset during bounded failover
- Dual-active binding
- Silent renegotiation
- Undefined transition states

---

# 5. What It Does NOT Defend Against

Outside scope:

- Endpoint malware
- Compromised keys
- Nation-state censorship systems
- DPI bypass guarantees
- Full anonymity systems
- Traffic correlation attacks

These require additional systems beyond transport modeling.

---

# 6. Security Philosophy

Security is layered.

Jumping VPN secures:

Session continuity under transport instability.

It does not claim:

Universal network immunity.

---

# 7. Failure Model

If security ambiguity occurs:

- Prefer termination over undefined continuation
- Prefer explicit audit events over silent degradation
- Prefer bounded failure over unbounded adaptation

---

# 8. Contract Statement

Jumping VPN guarantees deterministic behavior within defined volatility bounds.

Outside those bounds:

Termination is explicit.

No undefined state exists.

---

Session continuity is protected.
Total network control is not claimed.