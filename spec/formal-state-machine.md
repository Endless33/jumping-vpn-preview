# Jumping VPN — Formal State Machine Definition

Status: Normative Behavioral Model (Public Preview)

This document defines the formal state model
of Jumping VPN as a deterministic finite state machine (FSM).

All behavior MUST conform to this model.

---

# 1. State Set

S = {
    BIRTH,
    ATTACHED,
    VOLATILE,
    DEGRADED,
    RECOVERING,
    TERMINATED
}

TERMINATED is absorbing (no outgoing transitions).

---

# 2. Event Set

E includes:

- attach_ok
- instability_detected
- switch_initiated
- reattach_valid
- reattach_invalid
- recovery_timeout
- session_ttl_expired
- transport_ttl_expired
- operator_terminate

All events MUST produce explicit transition logs.

---

# 3. Transition Function δ(S, E)

δ(BIRTH, attach_ok) = ATTACHED

δ(ATTACHED, instability_detected) = VOLATILE

δ(VOLATILE, switch_initiated) = RECOVERING

δ(RECOVERING, reattach_valid) = ATTACHED

δ(RECOVERING, reattach_invalid) = DEGRADED

δ(VOLATILE, recovery_timeout) = DEGRADED

δ(DEGRADED, switch_initiated) = RECOVERING

δ(*, session_ttl_expired) = TERMINATED

δ(*, transport_ttl_expired) = TERMINATED

δ(*, operator_terminate) = TERMINATED

All undefined transitions are INVALID.

INVALID transitions MUST be rejected and logged.

---

# 4. Determinism Constraint

For any given state S and event E:

- δ(S, E) MUST produce exactly one next state.
- No ambiguous transitions allowed.
- No silent fallback transitions allowed.

---

# 5. Invariants

I1: TERMINATED has no outgoing transitions.

I2: ATTACHED implies exactly one active transport binding.

I3: RECOVERING implies at least one candidate transport exists.

I4: VOLATILE implies instability threshold exceeded.

I5: DEGRADED implies adaptation rate is bounded or recovery unsuccessful.

I6: No transition to ATTACHED may occur without successful reattach validation.

---

# 6. Prohibited Behaviors

The following are strictly forbidden:

- ATTACHED → ATTACHED without explicit reason code.
- VOLATILE → ATTACHED without RECOVERING phase.
- Implicit identity renegotiation.
- Infinite transition loops without time progression.

---

# 7. Liveness Guarantees

Within bounded policy constraints:

- If a valid transport candidate exists,
  and recovery window not exceeded,
  the system SHOULD eventually reach ATTACHED.

If no candidate exists,
  and TTL exceeded,
  the system MUST reach TERMINATED.

---

# 8. Safety Guarantees

The system MUST NOT:

- Bind a transport without proof validation.
- Reset identity silently.
- Exceed switch rate limits.
- Remain transportless beyond TTL.

---

# 9. Formal Interpretation

Jumping VPN defines a:

Deterministic,
Bounded,
Explicit,
Session-Centric
Finite State Machine.

Volatility is modeled as a state,
not as undefined failure.

---

# Final Statement

This FSM defines the behavioral contract.

Any implementation claiming compatibility
must conform to this state model.