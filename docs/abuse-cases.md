# Jumping VPN — Abuse Cases & Adversarial Scenarios

Status: Adversarial Analysis (Public Preview)

This document outlines potential abuse scenarios
against a session-centric, transport-volatile VPN model.

The purpose is not to claim immunity,
but to define failure behavior under attack.

---

# 1. Replay Attack on Reattach

## Scenario

An attacker captures a valid REATTACH_REQUEST
and attempts to replay it later
to hijack a session binding.

## Risk

- Session takeover
- Forced transport switch
- State churn
- Identity confusion

## Expected Behavior

Replay MUST fail due to:

- freshness window validation
- replay cache detection
- proof-of-possession mismatch

System MUST:

- deny reattach
- emit `SecurityReplayDetected`
- not change active transport

---

# 2. Transport Flapping Induction

## Scenario

Attacker injects artificial packet loss
to force repeated transport switching.

## Risk

- Oscillation
- Resource exhaustion
- Observability noise

## Expected Behavior

Switching MUST be:

- rate-limited
- bounded by policy
- cooldown enforced

If switch rate exceeded:

- deny switching
- emit `switch_rate_limited`
- possibly enter DEGRADED

---

# 3. Reattach Flood (State Mutation Flood)

## Scenario

Attacker floods server with reattach attempts
using guessed or random SessionIDs.

## Risk

- CPU exhaustion
- replay cache growth
- log flooding

## Expected Behavior

- Unknown sessions rejected early
- Rate limits applied per source
- Replay window bounded
- No state mutation for invalid session IDs

---

# 4. Stale Transport Hijack Attempt

## Scenario

Attacker attempts reattach after transport TTL expired.

## Risk

- Late hijack attempt
- Binding to terminated session

## Expected Behavior

If transport TTL exceeded:

- reattach MUST fail
- reason: `transport_ttl_exceeded`
- no state mutation allowed

---

# 5. Dual Binding Attempt (Cluster Race)

## Scenario

Two reattach attempts hit different nodes simultaneously.

## Risk

- Dual active transport
- Split-brain session

## Expected Behavior

- Versioned state update required
- One request succeeds
- Other fails with `stale_state_version`
- No dual binding allowed

---

# 6. Key Compromise Simulation

## Scenario

Session key suspected compromised.

## Risk

- Hijacked continuity
- Silent abuse

## Expected Behavior

Policy MUST allow:

- immediate termination
- explicit reason: `security_failure`
- security event emission

Session continuity must never override identity integrity.

---

# 7. Resource Exhaustion via Volatility

## Scenario

Network degraded to induce repeated volatility states.

## Risk

- Infinite recovery loops
- CPU churn
- Log amplification

## Expected Behavior

- RECOVERING state bounded
- Recovery window enforced
- Transition to DEGRADED or TERMINATED if bounded limits exceeded

No infinite loops allowed.

---

# 8. Session Fixation Attempt

## Scenario

Attacker attempts to reuse a known SessionID
in a different context.

## Risk

- Cross-context session reuse
- Identity confusion

## Expected Behavior

SessionID must be cryptographically bound to:

- key material
- identity context
- freshness window

Fixation attempts must fail validation.

---

# 9. Observability Abuse

## Scenario

Attacker triggers events to flood logging pipeline.

## Risk

- SIEM overload
- Alert fatigue

## Expected Behavior

- Logging rate limits may apply
- Security events remain explicit
- Core state transitions never suppressed

Auditability must remain intact.

---

# 10. Design Principle

Jumping VPN does not claim:

- immunity from transport attacks
- elimination of packet loss
- perfect uptime

It enforces:

- deterministic reaction
- bounded adaptation
- explicit failure states
- no silent corruption

---

# Final Position

Volatility increases attack surface.

The architecture must:

- model adversarial conditions
- bound recovery behavior
- enforce atomic state mutation
- preserve session identity integrity