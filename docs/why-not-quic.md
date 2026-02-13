# Why Not Just Use QUIC, MPTCP, or Existing VPNs?

Status: Architectural Positioning Document

This document explains why Jumping VPN is not merely
a configuration of existing transport technologies.

---

## 1. The Common Question

Can’t this be achieved with:

- QUIC connection migration?
- MPTCP?
- TCP failover?
- Smart load balancers?
- WireGuard with re-handshake?
- Application-level retries?

Short answer:  
Partially — but not behaviorally equivalent.

---

## 2. Transport vs Session Semantics

Most existing technologies operate at:

- Transport layer (QUIC, MPTCP)
- Tunnel layer (VPN protocols)
- Application retry logic

Jumping VPN defines:

A behavioral session layer that survives transport volatility
without renegotiation or implicit identity reset.

This is not just path switching.
It is identity continuity under volatile transport binding.

---

## 3. QUIC Comparison

QUIC provides:

- Connection migration
- Path validation
- Stream multiplexing

Limitations relative to Jumping VPN goals:

1. QUIC is still transport-bound:
   Connection identity is tied to QUIC-level cryptographic state.

2. Migration logic is not defined as:
   - operator-visible
   - reason-coded
   - policy-bounded in a deterministic state machine sense.

3. QUIC does not define:
   - session degradation state
   - bounded adaptation rules
   - explicit anti-flapping policy
   - recovery TTL semantics at session level.

QUIC solves mobility.
Jumping VPN models volatility as a first-class state.

---

## 4. MPTCP Comparison

MPTCP provides:

- Multiple simultaneous paths
- Subflow management

Limitations:

1. Path management is transport-level, not session-level.
2. No explicit degradation state modeling.
3. No deterministic recovery window semantics.
4. No operator-grade behavioral observability contract.

MPTCP increases redundancy.
Jumping VPN defines behavioral guarantees.

---

## 5. Traditional VPN Failover

Most VPNs:

- Treat transport death as session death.
- Trigger renegotiation.
- Require re-authentication.
- Reset cryptographic binding.

Jumping VPN:

- Separates session identity from transport binding.
- Allows reattach without full renegotiation (within bounded policy).
- Makes failure transitions explicit and auditable.

This is a state-machine-first design, not a tunnel-first design.

---

## 6. The Real Difference

Existing technologies optimize:

- Throughput
- Congestion control
- Path redundancy

Jumping VPN optimizes:

- Deterministic recovery
- Bounded adaptation
- Explicit failure modeling
- Identity continuity under volatility

It is not a faster tunnel.
It is a behavioral contract.

---

## 7. What Jumping VPN Is NOT

- Not a replacement for QUIC.
- Not a congestion control algorithm.
- Not a multipath transport implementation.
- Not an application retry library.

It operates above volatile transport bindings
and below application logic.

---

## 8. Positioning

Jumping VPN is:

A deterministic session control layer
for environments where transport volatility
is expected and adversarial conditions are plausible.

It complements transport protocols.
It does not reimplement them.

---

## Final Note

If QUIC solves your volatility problems,
you do not need Jumping VPN.

If your sessions collapse under failover,
then the problem is not transport —
it is behavioral semantics.