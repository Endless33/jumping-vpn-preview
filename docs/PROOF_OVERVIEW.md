# Jumping VPN — Proof Overview (Preview)

This document explains what is proven today, what is demonstrated,
and what remains under engineering validation.

This repository is an architectural validation layer.

---

# Core Claim

Jumping VPN guarantees:

Session identity survives transport death
without renegotiation, reset, or silent identity loss.

Within defined policy bounds.

---

# What is demonstrated today

The repository includes a behavioral Proof-of-Concept showing:

• Explicit session identity creation  
• Explicit transport attachment  
• Explicit transport death detection  
• Explicit transport switch  
• Session identity continuity  
• Deterministic state transitions  
• Audit events verifying invariants  

See:

- docs/DEMO_TRACE.md
- docs/STATE_MACHINE.md
- docs/INVARIANTS.md
- core/

---

# What is NOT claimed yet

This repository does NOT claim:

• production-grade encryption
• kernel-level VPN tunneling
• censorship resistance
• anonymity guarantees
• performance superiority vs QUIC/WireGuard

Those require separate validation.

This repository proves behavioral correctness only.

---

# What is provable from this repository

A reviewer can verify:

1. State machine correctness
2. Identity continuity invariants
3. Deterministic recovery model
4. Explicit rejection rules
5. Absence of silent identity reset

---

# Why this matters

Most VPNs bind identity to transport.

Jumping VPN binds identity to session.

Transport becomes replaceable.

This enables deterministic recovery under transport volatility.

---

Session is the anchor. Transport is volatile.