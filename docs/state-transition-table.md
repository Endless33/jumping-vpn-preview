# State Transition Table — Jumping VPN (Formal View)

This document defines the allowed session state transitions.

It is the canonical transition reference.

Any implementation must conform to this table.

---

# 1. States

- BIRTH
- ATTACHED
- VOLATILE
- DEGRADED
- RECOVERING
- TERMINATED

TERMINATED is final.

---

# 2. Transition Rules

| Current State | Event | Conditions | Next State | Version++ | Notes |
|---------------|-------|-----------|------------|-----------|-------|
| BIRTH | HANDSHAKE_ACK | Session created | ATTACHED | Yes | Initial binding |
| ATTACHED | TRANSPORT_DEAD | No viable delivery | RECOVERING | Yes | Enter recovery |
| ATTACHED | QUALITY_VIOLATION | Policy threshold exceeded | VOLATILE | Yes | Non-fatal instability |
| VOLATILE | STABILITY_SIGNAL | Within policy window | ATTACHED | Yes | Recovery success |
| VOLATILE | TRANSPORT_DEAD | Hard failure | RECOVERING | Yes | Escalation |
| RECOVERING | REATTACH_ACK | Proof valid, TTL valid | ATTACHED | Yes | Successful rebind |
| RECOVERING | REATTACH_REJECT | Policy violation | DEGRADED | Yes | Partial continuation |
| RECOVERING | TTL_EXPIRED | Session TTL exceeded | TERMINATED | Yes | Deterministic termination |
| DEGRADED | STABILITY_SIGNAL | Stable transport found | ATTACHED | Yes | Recovery |
| DEGRADED | VOLATILITY_PERSISTENT | Policy bounds exceeded | TERMINATED | Yes | Controlled stop |
| ANY (except TERMINATED) | SESSION_TTL_EXPIRED | TTL exceeded | TERMINATED | Yes | Hard boundary |
| ANY | OWNERSHIP_CONFLICT | Dual-active detected | TERMINATED | Yes | Safety over liveness |

---

# 3. Forbidden Transitions

The following transitions MUST NOT occur:

- ATTACHED → ATTACHED (without version increment)
- ATTACHED → TERMINATED (without explicit reason code)
- VOLATILE → BIRTH
- TERMINATED → any state
- RECOVERING → ATTACHED (without REATTACH_ACK validation)
- Parallel ATTACHED bindings

All forbidden transitions must be rejected explicitly.

---

# 4. Transition Requirements

Every valid transition must:

- Increment state_version
- Emit STATE_CHANGE event
- Include reason_code
- Preserve invariant checks
- Be auditable

No silent transitions.

---

# 5. Deterministic Outcomes

If multiple conditions apply:

Priority order:

1. SESSION_TTL_EXPIRED
2. OWNERSHIP_CONFLICT
3. TRANSPORT_DEAD
4. QUALITY_VIOLATION
5. STABILITY_SIGNAL

Higher priority events override lower ones.

This prevents ambiguity during simultaneous triggers.

---

# 6. Recovery Boundaries

Recovery window is bounded by:

- TransportLossTtlMs
- MaxSwitchesPerMinute
- MaxRecoveryWindowMs

If any bound exceeded:

RECOVERING → TERMINATED

No infinite retry loops.

---

# 7. Invariants Enforced During Transition

Before applying any transition:

- Single active transport check
- State_version monotonic check
- Ownership validation (cluster mode)
- TTL validation

If invariant fails:

Reject transition.
Do not mutate state.

---

# 8. Observability Requirement

Each transition must emit:

{
  "event_type": "STATE_CHANGE",
  "session_id": "...",
  "from_state": "...",
  "to_state": "...",
  "reason_code": "...",
  "state_version": N
}

Logging failures must not block correctness.

---

# 9. Terminal Guarantees

TERMINATED state guarantees:

- No active transport
- No future reattach accepted
- Session memory eligible for eviction
- Final audit event emitted

Termination is irreversible.

---

# Final Principle

State transitions define the protocol.

If transitions are not deterministic,
the protocol is undefined.

Session is the anchor.
Transport is volatile.
Transitions are explicit.