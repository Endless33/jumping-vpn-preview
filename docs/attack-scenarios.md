# Jumping VPN — Attack Scenarios & Behavioral Response

Status: Architectural Threat Modeling (Public Preview)

This document describes adversarial scenarios
and the expected behavioral response of the system.

The purpose is not to claim invulnerability.
It is to demonstrate deterministic handling of volatility
under hostile conditions.

---

# 1. Induced Packet Loss Attack

## Scenario

An attacker induces artificial packet loss on the active transport
(e.g., targeted interference, rate limiting, path disruption).

## Expected Behavior

- ATTACHED → VOLATILE
- Volatility detection triggered via:
  - LOSS_VOLATILE_THRESHOLD
  - MAX_CONSECUTIVE_DROPS
- Switch initiated if candidate transport exists

## Guarantees

- Session remains intact
- No renegotiation
- No silent identity reset
- Explicit TransportSwitch event logged

---

# 2. Transport Flapping Attack

## Scenario

Attacker alternates path stability rapidly,
attempting to force oscillation and CPU churn.

## Expected Behavior

- Switch attempts bounded by MAX_SWITCHES_PER_MIN
- SWITCH_COOLDOWN_MS enforced
- Session enters DEGRADED if instability persists

## Guarantees

- No infinite switching loop
- No unbounded resource usage
- Switch denials are logged and auditable

---

# 3. Reattach Replay Attack

## Scenario

Attacker captures a valid reattach message
and attempts replay during RECOVERING state.

## Required Controls

- Nonce-based replay protection
- REATTACH_PROOF_MAX_AGE_MS enforcement
- Cryptographic binding to session identity

## Expected Behavior

- Reattach rejected
- RECOVERING → DEGRADED
- Reason: reattach_validation_failed

## Guarantee

No unauthorized transport binding.

---

# 4. Session Hijack Attempt During Volatility

## Scenario

Attacker attempts to bind a malicious transport
while legitimate transport is unstable.

## Required Guarantee

Reattach must require:

- Valid session proof
- Key possession validation
- Freshness constraints

## Expected Behavior

- Invalid attempt rejected
- No state corruption
- Session remains bound to valid identity

---

# 5. NAT Expiry & Legitimate Rebinding

## Scenario

NAT mapping expires naturally.
Client appears from new source port/IP.

## Expected Behavior

- Volatility detection
- Reattach validation
- RECOVERING → ATTACHED

## Guarantee

Legitimate mobility supported.
No identity reset required.

---

# 6. Complete Path Blackout

## Scenario

All transports unavailable.
Network connectivity temporarily lost.

## Expected Behavior

- ATTACHED → VOLATILE → DEGRADED
- Session survives within TRANSPORT_LOST_TTL_MS
- After TTL → TERMINATED

## Guarantee

No indefinite zombie session.

---

# 7. Recovery Window Exhaustion Attack

## Scenario

Attacker prevents successful reattach repeatedly
to exhaust recovery window.

## Expected Behavior

- RECOVERING → DEGRADED
- If policy threshold exceeded → TERMINATED

## Guarantee

Bounded retry.
No infinite recovery loop.

---

# 8. Switch Rate Abuse

## Scenario

Attacker triggers repeated instability events
to exceed switch threshold.

## Expected Behavior

- TransportSwitchDenied
- DEGRADED state enforced
- No further switching until cooldown

## Guarantee

Deterministic anti-flapping behavior.

---

# 9. Split-Brain Risk Scenario

## Scenario

Client and server disagree on session state after volatility.

## Required Design Constraint

State transitions must be:

- Explicit
- Logged
- Versioned
- Rejecting unknown transitions

## Expected Behavior

- Invalid state transition rejected
- No dual-active session state

---

# 10. Observability Under Attack

Under all adversarial scenarios:

- SessionStateChange MUST be logged
- Reason code MUST be emitted
- TransportSwitch events MUST be auditable
- No silent state mutation allowed

---

# Final Statement

Jumping VPN does not assume stable networks.

It assumes:

- Active adversaries
- Induced instability
- Path manipulation
- Replay attempts
- Flapping behavior

Security is not guaranteed by optimism.
It is enforced by bounded, explicit transitions.

Volatility without structure is chaos.

Volatility with deterministic constraints
is survivable.