# Jumping VPN
## A Session-Centric Model for Deterministic Recovery Under Transport Volatility

Draft Whitepaper — Preview Version

---

# Abstract

Modern networks are volatile by default.

Mobile handovers, packet loss spikes, NAT churn,
and cross-border routing instability
make transport continuity unreliable.

Traditional VPN architectures assume transport stability
and treat instability as exceptional failure.

Jumping VPN proposes a session-centric model
where identity continuity is independent of transport binding.

This document outlines the behavioral architecture,
formal properties, threat model, and recovery guarantees
of the proposed system.

This is an architectural draft,
not a production specification.

---

# 1. Introduction

Secure communication systems historically evolved
in environments where network paths were relatively stable.

In contemporary environments:

- Transport paths change frequently
- IP addresses are ephemeral
- Packet loss is common
- NAT mappings expire unpredictably
- Mobile connectivity flaps

The assumption of stability has become incorrect.

Protocols that assume stability inherit fragility.

Jumping VPN addresses this mismatch.

---

# 2. Design Principle

Core inversion:

Session = identity anchor  
Transport = replaceable attachment

Transport volatility does not imply session termination.

Volatility is treated as a modeled state,
not as an unexpected error.

---

# 3. Behavioral Model

## 3.1 Session States

A session transitions through:

- BIRTH
- ATTACHED
- VOLATILE
- DEGRADED
- RECOVERING
- TERMINATED

All transitions are:

- explicit
- reason-coded
- policy-bound
- auditable

---

## 3.2 Deterministic Recovery

When transport death occurs:

1. Session enters RECOVERING
2. Client sends REATTACH_REQUEST
3. Server validates proof-of-possession + freshness
4. Ownership authority verified
5. New transport bound
6. Session returns to ATTACHED

Recovery is bounded by policy.

If bounds are exceeded:

Session transitions to TERMINATED.

---

# 4. Formal Properties

The system enforces:

- Single active transport binding
- Session identity immutability
- Versioned state transitions
- Bounded recovery windows
- Bounded switch rate
- Deterministic termination

Ambiguity resolves to rejection or termination.

Safety is prioritized over availability.

---

# 5. Threat Model

Assumptions:

- On-path attackers can observe and disrupt traffic
- Packet loss and delay can be induced
- Reattach requests may be replayed
- Control plane may be flooded

Mitigations:

- Proof-of-possession binding
- Freshness validation (anti-replay window)
- Rate-limited switching
- Ownership authority enforcement
- Explicit invariant checks

This architecture does not claim anonymity guarantees
or censorship resistance.

---

# 6. Cluster Model

Production deployment requires:

- Authoritative session ownership
- Sticky routing OR atomic shared state store
- Versioned updates (CAS/transactions)

Dual-active binding is forbidden.

Consistency is preferred over availability.

---

# 7. Comparative Positioning

Jumping VPN differs from:

WireGuard:
- Endpoint-centric
- Minimal state abstraction

IPsec:
- SA-bound identity
- Timer-driven renegotiation

QUIC:
- Transport-layer migration
- No session-level invariants

Jumping VPN introduces:

Session-level behavioral determinism
above transport abstraction.

---

# 8. Engineering Scope

This repository defines:

- Behavioral model
- Formal invariants
- Threat model
- Attack scenarios
- Benchmark plan
- Production readiness gap

It does not include:

- Production-grade crypto
- Hardened control plane
- Performance claims
- Full distributed implementation

---

# 9. Intended Applications

The model may be applicable to:

- Mobile-first fintech systems
- Edge computing deployments
- Cross-border enterprise networks
- High-volatility carrier environments

Where session continuity is critical.

---

# 10. Limitations

Jumping VPN does not:

- Replace anonymity networks
- Guarantee zero downtime
- Eliminate denial-of-service risk
- Provide endpoint compromise protection
- Claim performance superiority

It focuses narrowly on:

Deterministic recovery under transport instability.

---

# 11. Conclusion

Modern networks are unstable.

Protocols that assume stability
must constantly renegotiate identity.

Jumping VPN assumes instability
and encodes it explicitly into behavior.

The key claim:

Session identity can remain stable
while transport bindings change,
under bounded, deterministic rules.

This is an architectural direction,
not a finished product.

---

Session is the anchor.  
Transport is volatile.  
Continuity must be deterministic.