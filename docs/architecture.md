# Jumping VPN — Architecture Overview

This document outlines the high-level architectural model
behind Jumping VPN.

It describes behavioral guarantees, state modeling,
and transport abstraction principles.

This is not a full implementation specification.

---

# 1. Architectural Philosophy

Traditional VPNs assume:

- Stable transport
- Predictable routing
- Fixed IP bindings
- Renegotiation on failure

Jumping VPN assumes:

- Transport volatility
- IP drift
- Path degradation
- Packet loss spikes

The protocol models volatility as an expected condition,
not as an exception.

---

# 2. Core Separation Principle

The foundational architectural rule:

> Session ≠ Transport

The session is the persistent logical identity.
The transport is a replaceable path binding.

Transport death does not imply session death.

---

# 3. Session Lifecycle Model

A session transitions through deterministic states:

```
[BIRTH]
   ↓
[ATTACHED]
   ↓
[VOLATILE]
   ↓
[DEGRADED]
   ↓
[RECOVERING]
   ↺
[ATTACHED]
   ↓
[TERMINATED]
```

### State Definitions

**BIRTH**  
Session created with identity and policy context.

**ATTACHED**  
Stable transport bound.

**VOLATILE**  
Transport instability detected (latency, loss, jitter).

**DEGRADED**  
Partial failure but session continuity preserved.

**RECOVERING**  
Explicit reattachment attempt under policy constraints.

**TERMINATED**  
Session lifetime expired or unrecoverable failure.

---

# 4. Transport Abstraction Layer

Transports are:

- Ephemeral
- Competing
- Policy-scored
- Explicitly switchable

Switch triggers may include:

- Packet loss threshold
- Latency threshold
- Explicit operator policy
- Hard transport failure

Switching must be:

- Logged
- Bounded
- Rate-limited
- Auditable

---

# 5. Deterministic Recovery Model

When transport failure occurs:

1. Session does not immediately terminate.
2. State transitions to VOLATILE or DEGRADED.
3. Recovery window is opened.
4. Reattachment requires session-bound validation.
5. If successful → ATTACHED.
6. If not within bounds → TERMINATED.

No uncontrolled renegotiation.
No silent identity reset.

---

# 6. Anti-Oscillation Controls

To prevent unstable flapping:

- Maximum switch rate per time window
- Cooldown intervals
- Stability scoring
- Dampening policy

Adaptation must remain predictable.

---

# 7. Observability Guarantees

Every critical transition emits:

- Session ID
- Previous state
- New state
- Transport change
- Reason code
- Timestamp

This enables:

- SOC visibility
- Deterministic auditing
- Post-incident reconstruction

---

# 8. Failure Classification

Failures are categorized as:

**Soft Failure**
- Packet loss spike
- Latency degradation
- Partial path instability

**Hard Failure**
- All transports dead
- Policy exhaustion
- Session lifetime exceeded

Soft failure preserves identity.
Hard failure ends the session.

---

# 9. Security Model (High-Level)

Jumping VPN principles include:

- Session-bound identity
- Replay resistance
- Reattachment validation
- Policy-bounded recovery
- Deterministic key lifecycle triggers

Cryptographic details are intentionally not exposed
in this preview.

---

# 10. Non-Goals

Jumping VPN does not attempt to:

- Replace anonymity networks
- Guarantee endpoint compromise resistance
- Eliminate all latency variation
- Function as a censorship bypass system

It focuses specifically on session continuity
under transport volatility.

---

# 11. Deployment Vision (Conceptual)

Potential deployment contexts include:

- Mobile workforce infrastructure
- Fintech session reliability
- Cross-border routing instability
- Edge computing environments
- High-availability distributed systems

---

# Closing Principle

Jumping VPN is not designed for convenience.

It is designed for environments
where transport instability is normal.

The session remains the anchor.
Transports come and go.