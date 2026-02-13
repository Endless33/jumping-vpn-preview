# Jumping VPN — Performance Boundaries (Public Preview)

Status: Architectural Validation

This document defines behavioral performance limits,
not marketing throughput claims.

Jumping VPN is a session control layer.
It does not replace congestion control.
It does not optimize raw bandwidth.

It defines bounded recovery behavior under volatility.

---

# 1. Scope of Performance

Jumping VPN controls:

- Session continuity
- Transport switching logic
- Volatility detection
- Recovery timing
- State transitions

Jumping VPN does NOT control:

- Underlying congestion algorithm
- Raw transport throughput
- Kernel-level packet scheduling

---

# 2. Recovery Latency Boundaries

## 2.1 Detection Time

Transport instability detection is bounded by:

- HEARTBEAT_INTERVAL_MS
- HEARTBEAT_VOLATILE_MS
- LOSS_WINDOW_MS

Worst-case detection time:

<= HEARTBEAT_VOLATILE_MS

This defines upper bound for volatility recognition.

---

## 2.2 Switch Initiation Latency

Switch may occur when:

- Instability threshold crossed
- Policy permits switching
- Cooldown not active

Worst-case initiation delay:

<= SWITCH_COOLDOWN_MS

---

## 2.3 Reattach Completion Time

Total bounded recovery window:

<= RECOVERY_WINDOW_MS

If recovery fails within window → DEGRADED or TERMINATED.

No indefinite recovery loops allowed.

---

# 3. Switching Rate Boundaries

MAX_SWITCHES_PER_MIN defines:

- Upper bound of volatility adaptation rate
- Anti-flapping protection
- CPU and state churn limitation

Switch rate MUST remain bounded.

If exceeded:
- Switch denied
- Session enters DEGRADED

---

# 4. Resource Boundaries

## 4.1 Memory

Session memory footprint MUST be bounded by:

- Fixed session structure
- Bounded candidate transport set
- Bounded replay window

No unbounded growth allowed.

---

## 4.2 CPU Impact

Switch logic must be:

- O(n) relative to candidate transport set
- Not proportional to historical transitions
- Not dependent on unbounded state logs

Recovery operations must not scale with:
- Session age
- Packet history length

---

# 5. Degradation Mode Behavior

DEGRADED state ensures:

- Reduced switch attempts
- Stabilized decision-making
- Lower CPU churn
- Bounded adaptation rate

Degradation is protective,
not failure.

---

# 6. Mobile Environment Assumptions

Jumping VPN assumes:

- NAT rebinding
- LTE/WiFi switching
- Intermittent packet loss
- Variable latency spikes

Performance model prioritizes:

- Continuity over peak throughput
- Deterministic behavior over aggressive retry

---

# 7. Hard Boundaries

The system MUST:

- Never attempt infinite reattach loops
- Never allow unbounded switch oscillation
- Never allow transportless session beyond TTL
- Never perform silent renegotiation

All transitions must be explicit and bounded.

---

# 8. What This Document Does Not Claim

This is NOT:

- A bandwidth benchmark
- A throughput comparison
- A QUIC replacement
- A low-latency optimization engine

It is a volatility control layer.

---

# Final Positioning

Jumping VPN defines:

Behavioral latency bounds.
Switch rate bounds.
Recovery window bounds.
Session lifetime bounds.

It does not promise maximum speed.
It promises bounded adaptation under transport instability.