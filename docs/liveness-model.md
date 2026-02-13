# Liveness Model — Jumping VPN (Preview)

This document defines how Jumping VPN reasons about liveness
without violating safety invariants.

Safety > Liveness.

Continuity is desirable.
Correctness is mandatory.

---

# 1. Definitions

Safety:
The system never enters an invalid state.

Liveness:
The system eventually makes progress under acceptable conditions.

Jumping VPN guarantees safety absolutely.
Liveness is conditional.

---

# 2. Liveness Conditions

A session can remain live if:

- At least one viable transport exists
- Recovery window has not expired
- State store remains consistent
- Policy bounds are not exceeded

If these conditions hold,
the session may recover.

If not,
termination is explicit.

---

# 3. Recovery Window

Let:

MaxRecoveryWindowMs = policy-defined bound

If:

CurrentTime - TransportDeathTime > MaxRecoveryWindowMs

Then:

RECOVERING → TERMINATED

No infinite retry loop allowed.

---

# 4. Switch Rate Bound

Let:

MaxSwitchesPerMinute = policy-defined bound

If switching exceeds threshold:

Session enters DEGRADED.

If degradation persists:

Termination may occur.

Prevents oscillation storms.

---

# 5. Cluster Partition Scenario

Case: network split between nodes.

Guarantee:

- No dual-active continuation.
- One side may reject reattach.
- Safety preserved.

Liveness may degrade.
Safety cannot.

---

# 6. Control-Plane Attack Scenario

If reattach requests are flooded:

- Rate limiting applies.
- Replay window enforced.
- State not mutated on invalid request.

Liveness may reduce.
Session not corrupted.

---

# 7. Total Transport Loss

If all candidate transports fail:

Session enters RECOVERING.

If recovery window expires:

TERMINATED.

No undefined state allowed.

---

# 8. Store Failure Scenario

If authoritative session store unavailable:

System must fail closed.

Reattach denied.
No ambiguous ownership allowed.

Availability sacrificed for correctness.

---

# 9. Design Philosophy

Jumping VPN is not designed to:

- Survive infinite network collapse
- Override physical disconnection
- Guarantee availability under partition

It is designed to:

- Preserve identity deterministically
- Recover within bounded constraints
- Fail explicitly when recovery is impossible

---

# 10. Formal Balance

| Property      | Priority |
|--------------|----------|
| Identity Safety | Absolute |
| Version Monotonicity | Absolute |
| Bounded Recovery | Absolute |
| Availability | Conditional |
| Multi-path survival | Conditional |

---

# Final Principle

If the system must choose between:

- continuing incorrectly
- terminating correctly

It terminates.

Continuity without correctness is corruption.

Session is the anchor.
Transport is volatile.
Correctness is sovereign.