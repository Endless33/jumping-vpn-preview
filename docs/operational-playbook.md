# Operational Playbook — Jumping VPN

Status: Architectural Validation  
Scope: Operator Response & Incident Handling  

This document defines how operators should respond to
transport volatility, abnormal behavior, and security events.

A protocol is not production-ready without an operational model.

---

# 1. Core Operational Philosophy

Jumping VPN does not attempt to hide volatility.

It models volatility explicitly.

Operators must:

- Observe transitions
- Validate bounded behavior
- Confirm invariants
- Intervene only when deterministic limits are exceeded

No manual override should create ambiguity.

---

# 2. Session Lifecycle Monitoring

Operators must monitor:

- Session state distribution
- Recovery latency percentiles
- Switch rate per session
- DEGRADED state frequency
- TERMINATED reasons

Key indicators:

If RECOVERING > expected baseline → investigate transport layer.
If DEGRADED spikes → investigate network quality floor.
If TERMINATED increases → check TTL policy bounds.

---

# 3. Transport Volatility Response

Scenario: Spike in TRANSPORT_DEAD events.

Steps:

1. Validate transport health metrics (loss, jitter, latency).
2. Confirm recovery latency within MaxRecoveryWindowMs.
3. Ensure no dual-active bindings.
4. Confirm switch-rate limits enforced.
5. Inspect reason codes for anomaly patterns.

If recovery remains bounded → no action required.

Volatility is not an incident by default.

---

# 4. Recovery Window Breach

If sessions exceed RecoveryWindow:

Expected behavior:
→ TERMINATED (explicit)

Operator action:

- Validate TTL configuration
- Confirm anti-flap logic not misconfigured
- Confirm control-plane not overloaded
- Check replay or abuse patterns

Never manually force silent continuation.

---

# 5. Replay / Hijack Detection

Indicators:

- Nonce reuse
- Stale state_version
- Reattach storm from unknown sources

Operator action:

1. Confirm anti_replay rejection.
2. Confirm no state mutation occurred.
3. Confirm rate limiter triggered.
4. Audit logs for anomalous patterns.
5. If repeated → IP-based mitigation upstream.

Protocol must fail closed.

---

# 6. Cluster Ownership Ambiguity

If dual ownership attempt detected:

Expected behavior:
→ REJECT or TERMINATE

Operator action:

- Validate CAS atomicity
- Confirm sticky routing integrity
- Check distributed store latency
- Confirm no split-brain configuration

Ambiguous continuation is forbidden.

---

# 7. High Churn Event

Example:

Mobile network outage.
10% sessions enter RECOVERING.

Expected:

- Bounded reattach
- No state rollback
- No global stall

Operator checklist:

- CPU within safe bounds
- Memory stable
- Switch-rate limits respected
- No infinite oscillation

---

# 8. DEGRADED Mode Handling

DEGRADED is not failure.

It means:

Transport unstable but still usable.

Operator action:

- Verify policy thresholds
- Verify quality floors
- Confirm no silent corruption
- Monitor transition back to ATTACHED

Do not terminate unless policy requires.

---

# 9. Termination Analysis

When session enters TERMINATED:

Operator must verify:

- reason_code present
- state_version incremented
- TTL or policy bound triggered
- no silent identity reset occurred

Termination without reason_code = defect.

---

# 10. Logging Outage

If observability pipeline fails:

Expected behavior:

- State machine continues correctly
- No state mutation depends on log delivery
- Telemetry degrades, not correctness

Operator action:

Restore telemetry.
Do not restart session layer unnecessarily.

---

# 11. Emergency Mode

If system under extreme instability:

Possible actions:

- Reduce MaxSwitchesPerMinute
- Tighten recovery window
- Temporarily limit new session creation
- Rate-limit reattach attempts more aggressively

Never disable version checks.
Never disable anti-replay.
Never allow dual-active binding.

---

# 12. Post-Incident Review

After volatility event:

Review:

- Recovery latency distribution
- Switch attempt counts
- Replay rejection events
- TTL-triggered terminations
- Resource usage

Update:

- Policy thresholds
- Rate limits
- Recovery bounds

But never compromise invariants.

---

# 13. Invariant Enforcement Checklist

Operators must confirm at all times:

- Only one active transport per session
- No silent identity reset
- No unbounded recovery
- No state rollback
- No replay acceptance
- No ambiguous ownership

If any violated → stop deployment.

---

# 14. Deployment Readiness Reminder

Operational maturity is defined by:

Predictable failure  
Bounded recovery  
Auditable transitions  

Not by uptime alone.

---

# Final Principle

A resilient protocol must survive volatility.

A safe protocol must survive operators.

Session is the anchor.  
Transport is volatile.  
Operations must be deterministic.