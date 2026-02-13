# Jumping VPN — Temporal Guarantees

Status: Normative Temporal Behavior (Public Preview)

This document expresses key behavioral guarantees
using lightweight temporal logic notation.

Goal:
Define what must **eventually** happen (liveness)
and what must **never** happen (safety)
over time.

This is a readable formalization,
not a complete proof system.

---

## 0. Notation

We use:

- ALWAYS(P): P must hold at all times
- EVENTUALLY(P): P must hold at some future time
- UNTIL(P, Q): P holds until Q becomes true
- IMPLIES(P, Q): if P then Q

State variables:

- state ∈ {BIRTH, ATTACHED, VOLATILE, DEGRADED, RECOVERING, TERMINATED}
- active_transport_count = |A|
- candidate_count = |C|
- within_transport_ttl = (transportless_age_ms ≤ TRANSPORT_LOST_TTL_MS)
- within_session_ttl = (session_age_ms ≤ SESSION_MAX_LIFETIME_MS)
- policy_allows_switch = boolean
- security_valid = boolean

---

# 1. Safety Guarantees (Must Never Happen)

## S1 — No dual-active binding

ALWAYS(active_transport_count ≤ 1)

---

## S2 — ATTACHED implies active transport exists

ALWAYS(state = ATTACHED IMPLIES active_transport_count = 1)

---

## S3 — No silent identity reset

ALWAYS(identity_reset IMPLIES state = TERMINATED)

Where:
identity_reset means SessionID changes without explicit session termination.

---

## S4 — No infinite uncontrolled switching

ALWAYS(switch_rate_exceeded IMPLIES switch_denied)

Bounded adaptation must always apply.

---

## S5 — TERMINATED is absorbing

ALWAYS(state = TERMINATED IMPLIES NEXT(state) = TERMINATED)

No outgoing transitions.

---

# 2. Liveness Guarantees (Must Eventually Happen)

## L1 — If recovery is possible, session returns to ATTACHED

ALWAYS(
  (state = RECOVERING AND candidate_count ≥ 1 AND policy_allows_switch AND security_valid AND within_transport_ttl)
  IMPLIES
  EVENTUALLY(state = ATTACHED)
)

---

## L2 — If no recovery possible, system terminates deterministically

ALWAYS(
  (active_transport_count = 0 AND NOT within_transport_ttl)
  IMPLIES
  EVENTUALLY(state = TERMINATED)
)

---

## L3 — Session TTL eventually terminates session

ALWAYS(
  (NOT within_session_ttl)
  IMPLIES
  EVENTUALLY(state = TERMINATED)
)

---

# 3. Volatility Handling Guarantees

## V1 — Instability triggers visibility

ALWAYS(
  (instability_detected)
  IMPLIES
  EVENTUALLY(state ∈ {VOLATILE, RECOVERING, DEGRADED})
)

No "silent instability".

---

## V2 — Recovery is bounded in time

ALWAYS(
  (state = RECOVERING)
  IMPLIES
  EVENTUALLY(state ∈ {ATTACHED, DEGRADED, TERMINATED})
)

No infinite RECOVERING loops.

---

# 4. Auditability Guarantees

## A1 — Every state transition emits an event

ALWAYS(
  (state_changes)
  IMPLIES
  EVENTUALLY(event_type = "SessionStateChange")
)

---

## A2 — Every switch decision is explicit

ALWAYS(
  (switch_attempted)
  IMPLIES
  EVENTUALLY(event_type ∈ {"TransportSwitch", "TransportSwitchDenied"})
)

---

# 5. Security Guarantees Under Reattach

## SEC1 — No bind without proof

ALWAYS(
  (reattach_attempted AND NOT security_valid)
  IMPLIES
  EVENTUALLY(state ∈ {DEGRADED, TERMINATED})
)

Unauthorized reattach must fail.

---

## SEC2 — Replay attempt never results in ATTACHED

ALWAYS(
  (replay_detected)
  IMPLIES
  EVENTUALLY(state ≠ ATTACHED)
)

---

# 6. Interpretation

These guarantees assert:

- Safety: what must never happen
- Liveness: what must eventually happen
- Bounded adaptation: no infinite oscillation
- Deterministic recovery: possible recovery leads to ATTACHED
- Deterministic failure: impossible recovery leads to TERMINATED
- Auditability: events reflect behavior

---

# Final Statement

Jumping VPN is defined by behavior over time.

This document formalizes that behavior:

- explicitly
- deterministically
- auditably

Volatility is survivable
only when constrained by guarantees.