# Why This Is Not “Just QUIC”

This document clarifies the architectural distinction between
QUIC connection migration and the Jumping VPN session model.

Short version:

QUIC solves transport migration.  
Jumping VPN formalizes session continuity under volatility.

They operate at different conceptual layers.

---

## 1) What QUIC Actually Solves

QUIC provides:

- Connection migration across IP changes
- Path validation
- Congestion control
- Encrypted transport
- Stream multiplexing

It allows a connection to survive certain network changes,
such as mobile IP handover.

That is transport-layer continuity.

---

## 2) What Jumping VPN Models

Jumping VPN models volatility at the **session layer**.

Key properties:

- Explicit session identity anchor
- Deterministic state machine
- Bounded recovery windows
- Policy-driven switching constraints
- Version-controlled state mutation
- Auditable transitions

The system treats volatility as a modeled state,
not as a hidden implementation detail.

---

## 3) Conceptual Layer Separation

Transport Layer (example: QUIC)
- Handles packet delivery
- Handles congestion
- Handles path migration

Session Layer (Jumping VPN)
- Owns identity
- Owns state transitions
- Owns recovery bounds
- Owns invariants
- Decides termination vs continuation

Transport migration ≠ Session determinism.

---

## 4) Determinism vs Opportunistic Migration

QUIC migration is opportunistic and transport-centric.

Jumping VPN recovery is:

- Explicit
- Version-validated
- Policy-bounded
- Reason-coded
- Reject-on-ambiguity

If a migration cannot preserve invariants,
the session terminates explicitly.

Correctness > survival.

---

## 5) Multi-Transport Abstraction

Jumping VPN is transport-agnostic.

Possible transport candidates:

- UDP
- TCP
- QUIC
- Future protocols

The behavioral contract remains the same.

This abstraction is intentional.

---

## 6) Bounded Adaptation

Jumping VPN enforces:

- MaxRecoveryWindow
- MaxSwitchesPerMinute
- TransportLossTTL
- Anti-replay constraints
- Single active binding invariant

These constraints are external to any single transport protocol.

They are architectural guarantees.

---

## 7) Observability

Jumping VPN emits explicit:

- STATE_CHANGE events
- TRANSPORT_SWITCH events
- SECURITY_EVENT logs
- Policy-limit triggers

Transport protocols do not define SOC-grade
behavioral observability at the session layer.

Jumping VPN does.

---

## 8) When QUIC Is Useful

QUIC can be:

- A candidate transport adapter
- A latency-optimized path
- A mobility-friendly carrier

But QUIC does not define:

- Session ownership authority
- Cluster conflict resolution
- Deterministic termination semantics
- Bounded recovery policies
- Cross-node identity guarantees

Those belong to the session layer.

---

## Final Distinction

QUIC:  
"Can this connection survive a path change?"

Jumping VPN:  
"Under what deterministic constraints may a session survive transport volatility?"

That is the architectural difference.

---

Session is the anchor.  
Transport is volatile.