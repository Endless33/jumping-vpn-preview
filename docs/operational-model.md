# Operational Model — Jumping VPN (Preview)

This document describes how Jumping VPN behaves
from an operational perspective.

It defines:

- Runtime expectations
- Operator responsibilities
- Incident behavior
- Degraded-mode handling
- Observability expectations

This is not infrastructure-as-code.
It is behavioral operations guidance.

---

# 1. Operational Philosophy

Jumping VPN is built around:

Determinism over convenience  
Explicit failure over silent corruption  
Bounded recovery over infinite retry  

Operators must understand:

Transport instability is normal.
Identity ambiguity is not.

---

# 2. Runtime States (Operational View)

Each session exists in one of:

- BIRTH
- ATTACHED
- VOLATILE
- RECOVERING
- DEGRADED
- TERMINATED

Operators must monitor:

- State distribution
- Switch frequency
- Recovery latency
- Degraded rate
- Termination causes

---

# 3. Expected Normal Behavior

In volatile networks:

- Sessions may enter VOLATILE
- Controlled RECOVERING cycles may occur
- TransportSwitch events expected
- Short-lived degradation possible

This is normal.

Repeated uncontrolled switching is not.

---

# 4. Switch Frequency Monitoring

Operators must track:

Switches per minute (per session)
Global switch rate
Recovery success ratio
Average recovery latency

Threshold breach should trigger:

Policy review
Network health investigation
Transport candidate reassessment

---

# 5. Degraded Mode Operations

DEGRADED is not failure.

It signals:

- Reduced stability
- Reduced switching tolerance
- Recovery window narrowing

In DEGRADED:

- Switching becomes more conservative
- Observability importance increases
- Session continuity preserved where possible

Persistent DEGRADED may indicate:

- Path instability
- Underlying network misconfiguration
- Policy miscalibration

---

# 6. Termination Semantics

TERMINATED must be:

- Explicit
- Reason-coded
- Auditable

Common reasons:

SESSION_TTL_EXPIRED
TRANSPORT_LOSS_TTL_EXPIRED
RATE_LIMIT_EXCEEDED
OWNERSHIP_CONFLICT
REPLAY_DETECTED

Termination is preferable to silent inconsistency.

---

# 7. Incident Handling Model

Incidents may involve:

- Reattach storms
- Replay attack attempts
- Transport instability spikes
- Cluster ownership conflicts

Operator action model:

1. Confirm invariant violations
2. Review session logs
3. Confirm state_version progression
4. Inspect rate limiter triggers
5. Validate ownership consistency

Never override session identity manually.

---

# 8. Logging Expectations

Each critical event must emit:

- timestamp
- session_id
- state transition
- reason code
- state_version

Operators must be able to reconstruct:

Full session timeline deterministically.

If logs are incomplete,
behavior must still remain correct.

---

# 9. Policy Tuning Model

Operators may tune:

MaxSwitchesPerMinute  
RecoveryWindowMs  
TransportLossTtlMs  
SessionTtlMs  
Quality thresholds  

Operators must not change:

State machine invariants  
Ownership rules  
Replay enforcement semantics  

Policy can change tolerance.
Not identity guarantees.

---

# 10. Cluster Operations

Clustered deployments must:

- Maintain ownership consistency
- Avoid dual-active binding
- Prefer termination over ambiguity

Monitoring must include:

- Ownership conflicts
- Version mismatch rejections
- CAS conflicts
- Reattach rejection rate

---

# 11. Abuse & Attack Signals

Operational red flags:

- High REATTACH_REJECT rate
- Frequent NONCE_REPLAY errors
- Rapid session churn
- Dual-binding attempts
- Rate limit exhaustion

Response:

Investigate.
Throttle.
Harden.
Never silently downgrade.

---

# 12. Disaster Recovery Principles

In catastrophic conditions:

If correctness cannot be guaranteed:
Terminate.

Session identity must never be duplicated.
Ambiguity must never be tolerated.

Recovery must remain bounded.

---

# 13. Operational Metrics Summary

Minimum recommended metrics:

Active sessions  
Sessions in VOLATILE  
Sessions in DEGRADED  
Recovery latency p95  
Switch rate p95  
Termination reason distribution  
Replay rejections  
Rate limiter triggers  

Operations must be measurable.

---

# 14. What Operations Does Not Control

Operators cannot:

Override replay window rules  
Force identity continuation  
Skip version increments  
Allow dual binding  

These are architectural invariants.

---

# 15. Operational Success Criteria

Deployment is operationally healthy when:

- Recovery latency within bounds
- Switch rate within policy
- No dual-active binding
- No silent resets
- Reattach rejection rare and explainable

If these hold,
the system behaves as designed.

---

# Final Principle

Operations manages policy.

Architecture enforces invariants.

Transport instability is operational reality.

Identity integrity is architectural law.

Session is the anchor.  
Transport is volatile.