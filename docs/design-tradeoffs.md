# Jumping VPN — Design Tradeoffs

Status: Architectural Rationale (Public Preview)

This document explains deliberate tradeoffs
made in the Jumping VPN architecture.

A protocol is defined not only by what it enables,
but also by what it refuses to do.

---

# 1. Consistency over Availability

Tradeoff:
In distributed deployments,
the system prefers deterministic termination
over ambiguous continuation.

Rationale:
Dual-active identity is worse than explicit failure.

Consequence:
Under cluster partition,
sessions may terminate rather than continue inconsistently.

---

# 2. Determinism over Heuristic Optimization

Tradeoff:
No AI-driven routing decisions.
No predictive congestion logic.

Rationale:
Heuristics reduce auditability.
Deterministic behavior is explainable.

Consequence:
System may not always select the globally optimal path,
but it will always select a bounded, explainable one.

---

# 3. Bounded Adaptation over Unlimited Resilience

Tradeoff:
Switching is rate-limited.
Recovery windows are finite.
Session TTL is enforced.

Rationale:
Unbounded adaptation leads to oscillation and instability.

Consequence:
Under extreme volatility,
session may terminate rather than endlessly recover.

---

# 4. Explicit State Model over Implicit Recovery

Tradeoff:
All volatility phases are represented as formal states.

Rationale:
Hidden recovery logic leads to debugging ambiguity.

Consequence:
More state transitions,
but greater transparency.

---

# 5. No Silent Renegotiation

Tradeoff:
Transport switch does not imply full cryptographic renegotiation.

Rationale:
Session identity is separate from transport.

Consequence:
Security model must strongly bind reattach proof
to session identity.

---

# 6. No Infinite Session

Tradeoff:
Session lifetime is bounded.

Rationale:
Long-lived identity without renewal increases attack surface.

Consequence:
Long-lived applications must tolerate session renewal events.

---

# 7. No Transport Randomization

Tradeoff:
Selection is deterministic,
not random.

Rationale:
Random behavior reduces auditability and reproducibility.

Consequence:
Selection policy must be carefully tuned.

---

# 8. Volatility Is Modeled, Not Eliminated

Tradeoff:
The protocol does not attempt to “fix” network instability.

Rationale:
Transport volatility is a property of the internet.

Consequence:
Jumping VPN adapts to volatility,
but does not claim to eliminate it.

---

# 9. Security Over Convenience

Tradeoff:
Reattach may be denied if proof stale or invalid.

Rationale:
Continuity must never compromise identity integrity.

Consequence:
Some recovery attempts fail intentionally.

---

# Final Position

Jumping VPN does not promise:

- Perfect uptime
- Magical routing
- Infinite adaptation

It promises:

- Deterministic behavior
- Explicit volatility modeling
- Bounded adaptation
- Identity integrity
- Auditability under pressure

Architecture maturity is defined
by explicit tradeoffs.