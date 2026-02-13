# Jumping VPN — Executive Whitepaper Preview

## Deterministic Session Continuity in Volatile Networks

---

# 1. Executive Summary

Modern networks are volatile by default.

Mobile switching, packet loss spikes, NAT rebinding,
cross-border degradation, and active disruption
are not edge cases — they are normal operating conditions.

Most VPN systems assume stability.
When transport fails, sessions collapse.

Jumping VPN models volatility as a first-class state.

The session is the anchor.
Transport is replaceable.

---

# 2. Core Thesis

Traditional model:

Transport = identity carrier  
Transport failure = session reset  

Jumping VPN model:

Session = identity anchor  
Transport = attachable surface  

Transport failure ≠ session termination  
(within defined policy bounds)

---

# 3. Architectural Model

Jumping VPN introduces:

- Deterministic state machine
- Explicit reason-coded transitions
- Bounded recovery windows
- Anti-flapping constraints
- Single-active transport invariant
- Authoritative cluster ownership model

All transitions are observable.

No silent renegotiation.
No undefined continuation.

---

# 4. Deterministic Recovery

Under transport death:

1. Session enters RECOVERING
2. Reattach attempt is initiated
3. Proof-of-possession validated
4. Active transport replaced
5. Session remains intact

If recovery exceeds policy bounds:
Session is explicitly terminated.

No ambiguous state allowed.

---

# 5. Security Boundaries

Jumping VPN secures:

Session continuity under transport volatility.

It does not claim:

- Global anonymity
- Endpoint compromise protection
- DPI bypass guarantees
- Nation-state censorship immunity

Security scope is explicit and bounded.

---

# 6. Cluster Safety

Split-brain is explicitly prevented.

Ownership model ensures:

- At most one active session owner
- Atomic reattach
- No dual-binding continuation

Consistency is preferred over availability.

---

# 7. Measurement Plan

Behavioral guarantees are measurable:

- RecoveryLatencyMs
- SwitchRate
- SessionResetCount
- DualBindingIncidents

Performance claims are not made without reproducible benchmarks.

---

# 8. Intended Audience

Jumping VPN is relevant for:

- Fintech platforms under failover stress
- Mobile infrastructure providers
- High-availability systems with transport churn
- Operators requiring deterministic recovery

---

# 9. Project Status

This repository represents:

Architectural validation stage.

It includes:

- Formal state machine
- Threat model
- Invariants
- Attack surface breakdown
- Benchmark plan
- Security review checklist
- Deterministic PoC

It is not a production release.

---

# 10. Closing Principle

Volatility is not an anomaly.

It is the default condition of modern networks.

A secure system must not collapse when the network shifts.

Session remains the anchor.  
Transport is volatile.