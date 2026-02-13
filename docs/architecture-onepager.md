# Jumping VPN — Architecture One-Pager

Status: Executive / Engineering Summary  
Audience: CTOs, Principal Engineers, Security Architects

---

## 1. Problem

Most VPN protocols were designed for stable networks:

- fixed IPs
- predictable paths
- low mobility
- minimal packet volatility

Modern networks behave differently:

- mobile flapping
- NAT churn
- cross-border degradation
- packet loss spikes
- transport disruption

Traditional VPN behavior:

Transport fails → renegotiate → reset session → reauthenticate user.

This is not resilience.
This is restart logic.

---

## 2. Core Thesis

Jumping VPN separates:

Session identity  
from  
Transport path.

The session is the anchor.
Transports are volatile.

Transport death ≠ session death.

Volatility is modeled, not treated as fatal error.

---

## 3. Behavioral Model

Session lifecycle:

BIRTH → ATTACHED → VOLATILE → RECOVERING → ATTACHED  
or  
→ DEGRADED → TERMINATED

Transport switching is:

- explicit
- bounded
- policy-driven
- auditable

No silent renegotiation.
No uncontrolled identity reset.

---

## 4. Deterministic Recovery

Under transport failure:

If:
- backup transport exists
- within transport TTL
- policy allows switching
- security validation succeeds

Then:
Session MUST return to ATTACHED.

If not:
Session transitions deterministically to TERMINATED.

No undefined states.
No ambiguous recovery.

---

## 5. Formal Guarantees

The architecture defines:

- Formal state machine
- Explicit invariants
- Temporal guarantees
- Bounded adaptation rules
- Anti-flapping constraints
- Versioned state mutation
- Observability contract
- Cluster consistency model

Behavior is defined as constraints,
not feature claims.

---

## 6. Observability by Design

Every transition emits structured events.

SOC / SIEM / NOC pipelines can reconstruct:

- state transitions
- transport switches
- degradation windows
- termination causes

No silent behavior.

If adaptation happens,
it is visible.

---

## 7. Distributed Safety

In clustered environments:

- No dual-active binding
- Versioned state transitions
- Split-brain prevention model
- Deterministic termination over inconsistency

Identity must never fork.

---

## 8. Non-Goals

Jumping VPN does NOT:

- Predict future congestion
- Use heuristic AI routing
- Attempt hidden optimization tricks
- Replace congestion control
- Eliminate physical network limits

It enforces deterministic session behavior
under volatile transport conditions.

---

## 9. Target Use Cases

- Mobile fintech with packet loss spikes
- Cross-border session continuity
- High-volatility enterprise mobility
- Infrastructure under frequent transport churn
- Environments where reauthentication is costly

---

## 10. Current Status

This repository represents:

- Architectural validation
- Formal behavioral modeling
- Deterministic recovery PoC
- Policy-driven design boundaries

It is not a marketing site.
It is a protocol design preview.

---

## 11. Why It Matters

The internet already changed.

Protocols did not.

Jumping VPN exists to align session behavior
with modern transport volatility.

Stability can no longer be assumed.

Continuity must be engineered.