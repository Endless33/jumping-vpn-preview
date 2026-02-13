# Jumping VPN — Explicit Limitations

Status: Architectural Scope Definition

This document defines what Jumping VPN does NOT attempt to solve.

Clear boundaries increase trust.
Undefined ambition decreases it.

---

# 1. Not a Transport Replacement

Jumping VPN does NOT:

- Replace QUIC
- Replace TCP congestion control
- Replace kernel-level routing
- Optimize raw throughput

It operates above volatile transport bindings.

---

# 2. Not an Anonymity Network

Jumping VPN does NOT:

- Guarantee anonymity
- Hide traffic volume patterns
- Obfuscate traffic fingerprinting by itself
- Replace Tor or mixnets

It preserves session continuity.
It does not provide anonymity guarantees.

---

# 3. Not a DDoS Shield

Jumping VPN does NOT:

- Absorb volumetric DDoS traffic
- Replace CDN-based mitigation
- Replace edge filtering infrastructure

Transport switching may mitigate some localized disruption,
but it is not a DDoS protection system.

---

# 4. Not a Cryptographic Reinvention

Jumping VPN does NOT:

- Invent new cryptographic primitives
- Replace TLS
- Replace proven key exchange algorithms
- Claim quantum resistance

It relies on hardened, existing cryptographic standards.

---

# 5. Not Unlimited Adaptation

The system is intentionally bounded:

- Switch rate is limited.
- Recovery window is finite.
- Session lifetime is capped.
- Transportless state is temporary.

Unbounded adaptation is instability.

---

# 6. Not Zero-Overhead

Switching and observability introduce:

- Additional state tracking
- Logging overhead
- Decision evaluation cost

This is a trade-off for deterministic recovery.

---

# 7. Not Immune to Total Blackout

If:

- No transport exists
- Recovery window expires
- Session TTL exceeded

The session terminates.

No protocol survives complete physical disconnection indefinitely.

---

# 8. Not a Marketing Claim

Jumping VPN does NOT claim:

- Infinite uptime
- Perfect resilience
- Unbreakable security
- Zero latency

It claims:

Deterministic behavior under volatility.

---

# 9. Not a Universal Replacement

It may not be needed if:

- Your environment is stable.
- Failover events are rare.
- QUIC migration already solves your problem.
- Identity continuity across transport is not critical.

In such cases, simpler systems may be preferable.

---

# 10. Scope Boundary Summary

Jumping VPN provides:

- Session-centric continuity
- Bounded adaptation
- Deterministic recovery
- Explicit degradation modeling
- Operator-grade observability

It does NOT provide:

- Throughput optimization
- Anonymity guarantees
- DDoS protection
- Infinite recovery

---

# Final Position

This system exists to solve one problem well:

How to preserve session identity under transport volatility
without uncontrolled renegotiation or silent resets.

Nothing more.
Nothing less.