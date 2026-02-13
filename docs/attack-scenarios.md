# Attack Scenarios & Expected Behavior — Jumping VPN (Preview)

This document models realistic adversarial situations
and defines the expected deterministic behavior of the system.

The purpose is to test architectural invariants under pressure.

---

# 1. Packet Loss Spike (Transport Degradation)

## Scenario

- Sudden packet loss spike (20–60%)
- Latency increases
- Transport still partially delivers traffic

## Expected Behavior

- Session enters VOLATILE or DEGRADED
- No identity reset
- No silent renegotiation
- Switch only if policy thresholds exceeded
- TransportSwitch event emitted (if triggered)
- State transition is explicit and reason-coded

## Forbidden Outcomes

- Silent session reset
- Dual-active transport binding
- Infinite oscillation

---

# 2. Hard Transport Death

## Scenario

- Transport stops delivering packets entirely
- No viable delivery within TransportLossTtlMs

## Expected Behavior

- Client enters RECOVERING
- REATTACH_REQUEST sent
- Server validates:
  - proof-of-possession
  - freshness
  - ownership authority
- If valid → ATTACHED (new transport)
- If TTL exceeded → TERMINATED

## Forbidden Outcomes

- Implicit identity renegotiation
- Silent state mutation
- Dual-active binding

---

# 3. Replay Attack on Reattach

## Scenario

Attacker replays old REATTACH_REQUEST
with valid but stale data.

## Expected Behavior

- Replay window validation fails
- Reattach rejected
- SECURITY_EVENT logged
- No state transition occurs

## Forbidden Outcomes

- Rebinding of stale transport
- State rollback
- Silent acceptance

---

# 4. Reattach Flood / Control Plane Abuse

## Scenario

Attacker floods gateway with reattach attempts
for unknown or random SessionIDs.

## Expected Behavior

- Early rejection for unknown sessions
- Rate limiting triggered
- No allocation of session state
- No state mutation

## Forbidden Outcomes

- Resource exhaustion via session allocation
- Transport switch triggered by invalid request
- Control-plane state mutation

---

# 5. Split-Brain Reattach (Cluster Conflict)

## Scenario

Two cluster nodes simultaneously receive valid reattach
for the same SessionID.

## Expected Behavior

- Ownership authority check enforced
- Only authoritative node accepts
- Other node rejects
- If ambiguity cannot be resolved → rejection
- No dual-active binding

## Forbidden Outcomes

- Two active transports for same session
- Session divergence between nodes

---

# 6. Flapping Transport (Rapid Instability)

## Scenario

Transport alternates between alive and dead rapidly.

## Expected Behavior

- Switch-rate bounded
- Cooldown applied
- Session may enter DEGRADED
- Explicit termination if bounds exceeded

## Forbidden Outcomes

- Infinite switching loop
- State oscillation without bound
- Unbounded CPU growth

---

# 7. Partial Failure (Selective Packet Corruption)

## Scenario

Some packets succeed, some are corrupted or dropped.

## Expected Behavior

- Quality floor detection
- DEGRADED state possible
- No silent corruption
- Explicit observability event

## Forbidden Outcomes

- Silent integrity assumption
- Identity mutation
- Undetected corruption state

---

# 8. On-Path Latency Manipulation

## Scenario

Attacker injects artificial delay
to trigger switch conditions.

## Expected Behavior

- Multi-signal gating (loss + window + thresholds)
- No switch on single spike
- Hysteresis respected
- Switch only if policy-bound criteria met

## Forbidden Outcomes

- Switch triggered by single packet anomaly
- Heuristic-driven instability

---

# 9. Ownership Store Unavailable

## Scenario

Cluster ownership storage temporarily unavailable.

## Expected Behavior

- Reattach denied safely
- No ambiguous binding
- Session may degrade or terminate deterministically

Consistency preferred over availability.

## Forbidden Outcomes

- Dual-active continuation
- Unverified transport binding

---

# 10. Policy-Bound Expiration

## Scenario

Session TTL or TransportLoss TTL exceeded.

## Expected Behavior

- Explicit TERMINATED state
- Reason-coded transition
- Audit event emitted

## Forbidden Outcomes

- Silent expiration
- Undocumented state disappearance

---

# 11. Evaluation Rule

For every attack scenario:

- State transitions must be explicit
- Identity must remain consistent unless terminated
- No silent behavior is allowed
- Recovery must be bounded
- Invariants must hold

If any invariant is violated,
the architecture fails.

---

# 12. Architectural Principle

The purpose of this document is not to claim invulnerability.

It is to demonstrate:

Deterministic behavior under adversarial pressure.

---

Session is the anchor.  
Transport is volatile.  
Ambiguity is failure.