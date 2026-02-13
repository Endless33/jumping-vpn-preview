# Adversarial Analysis — Jumping VPN (Preview)

This document models adversarial behavior
against the Jumping VPN control-plane.

It evaluates:

- Disruption attacks
- Replay attempts
- Reattach hijacking
- Control-plane abuse
- State desynchronization
- Cluster ambiguity

This is not a cryptographic proof.
It is a behavioral threat analysis.

---

# 1. Threat Model Assumptions

Attacker capabilities:

- Can observe network traffic (on-path)
- Can drop packets
- Can induce packet loss
- Can replay captured control-plane messages
- Can inject forged control-plane messages
- Can cause NAT churn
- Can force transport instability
- Can attempt reattach flooding

Attacker limitations:

- Cannot break cryptographic primitives
- Cannot extract SessionKey from secure memory
- Cannot bypass server-side invariant enforcement
- Cannot modify server code

If endpoint host is compromised,
session integrity cannot be guaranteed.
Endpoint security is out of scope.

---

# 2. Attack Surface Overview

Primary surfaces:

1. Initial handshake
2. Transport death trigger
3. Reattach request
4. Replay window validation
5. Rate limiter boundary
6. Cluster ownership validation

Each must fail closed.

---

# 3. Attack: Transport Disruption

Attack:

Attacker drops packets or induces latency spikes
to force frequent transport switching.

Goal:

Trigger instability collapse or state corruption.

Defense:

- Switch rate limit
- Cooldown window
- Recovery TTL bound
- Deterministic state transitions

Outcome:

Session may enter VOLATILE or DEGRADED.
If disruption persists beyond bound → TERMINATED.

No identity duplication possible.

---

# 4. Attack: Replay of REATTACH_REQUEST

Attack:

Attacker replays captured REATTACH_REQUEST.

Goal:

Hijack session binding.

Defense:

- Nonce freshness validation
- Sliding replay window
- Version match requirement
- Proof-of-possession required

Replay rejected before state mutation.

Outcome:

No state change.
Security event logged.

---

# 5. Attack: Dual Reattach Race

Attack:

Attacker attempts simultaneous reattach from multiple transports.

Goal:

Create dual-active identity.

Defense:

- Version monotonicity
- Atomic ownership validation
- CAS-style mutation enforcement
- Single active transport invariant

Outcome:

One reattach may succeed.
Others rejected.
Dual-active impossible.

---

# 6. Attack: Control-Plane Flood

Attack:

Mass reattach attempts
with random SessionIDs.

Goal:

Exhaust control-plane resources.

Defense:

- Early rejection for unknown session
- Rate limiter
- Bounded replay structure
- Stateless pre-validation

Outcome:

Invalid attempts rejected without state mutation.

---

# 7. Attack: State Version Desynchronization

Attack:

Send stale state_version to force rollback.

Goal:

Corrupt state or cause ambiguity.

Defense:

Server requires:

V_request == V_current

Else → reject.

Outcome:

Rollback impossible.

---

# 8. Attack: Cluster Split-Brain

Attack:

Two gateway nodes accept reattach simultaneously.

Goal:

Dual identity continuation.

Defense:

- Sticky routing OR
- Atomic shared session store
- Ownership conflict detection

Ambiguity → reject or terminate.

Correctness preferred over availability.

---

# 9. Attack: Transport Pinning

Attack:

Force session to remain on degraded transport.

Defense:

Policy re-evaluation interval
Quality thresholds
Switch eligibility rules

Session cannot be permanently pinned
if policy permits replacement.

---

# 10. Attack: Oscillation Amplification

Attack:

Alternate path degradation
to induce rapid switching.

Defense:

- Switch rate limit
- Cooldown
- Recovery window bound
- Escalation to DEGRADED

Infinite oscillation prevented by bounded switching.

---

# 11. Attack: Reattach Flood on Valid Session

Attack:

Attacker with stolen SessionID
attempts repeated reattach attempts.

Defense:

Without SessionKey → proof fails.
With SessionKey compromised → endpoint breach assumed.

Protocol cannot defend against compromised endpoint.

Endpoint security is external requirement.

---

# 12. Failure Preference

If attack conditions create ambiguity:

System chooses:

TERMINATION over corruption.

Identity safety is prioritized
over continuity.

---

# 13. Residual Risks

Not addressed:

- Global passive adversary anonymity
- Traffic analysis
- Data-plane encryption weaknesses
- Endpoint malware
- Kernel compromise
- Side-channel attacks

These require additional layers.

---

# 14. Adversarial Summary

Under defined assumptions:

- Identity duplication prevented
- Replay prevented
- Rollback prevented
- Dual binding prevented
- Oscillation bounded
- State mutation deterministic

Volatility may terminate session.

It cannot corrupt identity.

---

# Final Principle

Adversary may disrupt transport.

Adversary may not corrupt identity
without breaking cryptography
or compromising endpoints.

Session is the anchor.
Transport is volatile.