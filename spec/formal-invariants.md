# Jumping VPN — Formal Invariants

Status: Normative Behavioral Guarantees (Public Preview)

This document defines the core invariants
of the Jumping VPN session model.

These invariants must hold for all valid implementations.

---

# 1. Definitions

Let:

S = session state
T = transport set
A = active transport
C = candidate transport set
τ = current time
TTL_s = session TTL
TTL_t = transportless TTL
V = state version

States ∈ {BIRTH, ATTACHED, VOLATILE, DEGRADED, RECOVERING, TERMINATED}

---

# 2. Identity Invariants

## I1 — Single Active Binding

∀ session:

S = ATTACHED ⇒ |A| = 1

S ∈ {VOLATILE, DEGRADED, RECOVERING} ⇒ |A| ≤ 1

|A| > 1 is forbidden.

---

## I2 — No Silent Identity Reset

Let S_old be previous session identity.

∀ transition:

SessionID_new = SessionID_old

Unless:

S_new = TERMINATED AND new session explicitly created.

Implicit identity replacement is forbidden.

---

# 3. Transport Death ≠ Session Death

Let:

active transport dies at time t₀.

If:

∃ C such that |C| ≥ 1
AND τ - t₀ ≤ TTL_t

Then:

Session MUST NOT transition to TERMINATED.

---

# 4. Bounded Adaptation

Let:

switch_count(Δt=60s) ≤ MAX_SWITCHES_PER_MIN

If exceeded:

Switch must be denied.

Unbounded switching is forbidden.

---

# 5. Recovery Bound

If:

S = RECOVERING
AND τ > recovery_deadline

Then:

S_new ∈ {DEGRADED, TERMINATED}

Infinite RECOVERING loop is forbidden.

---

# 6. TTL Enforcement

If:

τ - session_created_at > TTL_s

Then:

S_new = TERMINATED

Session lifetime must be finite.

---

# 7. Transportless Bound

If:

|A| = 0
AND τ - last_active_transport > TTL_t

Then:

S_new = TERMINATED

No indefinite transportless state allowed.

---

# 8. Version Monotonicity

For each state transition:

V_new = V_old + 1

V must be strictly increasing.

Stale updates (V_old < current V) must be rejected.

---

# 9. Deterministic Transition

For any state S and event E:

∃! S'

Such that:

δ(S, E) = S'

Uniqueness required.
Ambiguous transition forbidden.

---

# 10. Liveness Condition

If:

∃ candidate transport
AND policy allows switching
AND recovery window active

Then:

Eventually S = ATTACHED

Unless security failure occurs.

---

# 11. Safety Condition

The system must never reach:

|A| > 1

or

S = ATTACHED ∧ A = null

or

dual active binding across nodes.

---

# 12. Termination Absorption

If:

S = TERMINATED

Then:

∀ E:

δ(S, E) = TERMINATED

TERMINATED is absorbing state.

---

# Final Position

Jumping VPN is defined not by features,
but by invariants.

If invariants hold,
the architecture holds.

If invariants break,
the system is undefined.