# Formal Transition Table — Jumping VPN (Preview)

This document defines the deterministic state transition model
for the Jumping VPN session lifecycle.

All transitions are explicit.
All transitions are reason-coded.
All transitions increment state_version.

---

# 1. States

The session may exist in exactly one of the following states:

| State        | Description |
|-------------|------------|
| BIRTH       | Session created but not yet attached |
| ATTACHED    | Active transport bound |
| VOLATILE    | Transport unstable but still delivering |
| RECOVERING  | Transport lost, reattach in progress |
| DEGRADED    | Stability compromised beyond thresholds |
| TERMINATED  | Final state, no further transitions allowed |

---

# 2. Transition Rules

## BIRTH

| Event                | Next State | Notes |
|----------------------|------------|------|
| HANDSHAKE_ACK        | ATTACHED   | Initial binding established |
| TERMINATE            | TERMINATED | Explicit failure |

---

## ATTACHED

| Event                      | Next State | Notes |
|----------------------------|------------|------|
| VOLATILITY_SIGNAL          | VOLATILE   | Quality threshold violated |
| TRANSPORT_DEAD             | RECOVERING | No viable delivery |
| TERMINATE                  | TERMINATED | Explicit termination |

---

## VOLATILE

| Event                      | Next State | Notes |
|----------------------------|------------|------|
| STABILITY_RESTORED         | ATTACHED   | Within policy bounds |
| TRANSPORT_DEAD             | RECOVERING | Hard failure |
| POLICY_EXCEEDED            | DEGRADED   | Instability bound exceeded |
| TERMINATE                  | TERMINATED | Explicit termination |

---

## RECOVERING

| Event                      | Next State | Notes |
|----------------------------|------------|------|
| REATTACH_SUCCESS           | ATTACHED   | New transport bound |
| REATTACH_REJECT_RECOVERABLE| VOLATILE   | Retry allowed |
| REATTACH_REJECT_FATAL      | TERMINATED | TTL exceeded or ambiguity |
| RECOVERY_WINDOW_EXCEEDED   | TERMINATED | Bounded recovery violated |

---

## DEGRADED

| Event                      | Next State | Notes |
|----------------------------|------------|------|
| STABILITY_RESTORED         | ATTACHED   | Within policy bounds |
| TRANSPORT_DEAD             | RECOVERING | Attempt bounded recovery |
| POLICY_EXCEEDED            | TERMINATED | Hard bound reached |
| TERMINATE                  | TERMINATED | Explicit termination |

---

## TERMINATED

| Event | Next State |
|------|------------|
| ANY  | (No transition allowed) |

TERMINATED is final.
State mutation forbidden.

---

# 3. Version Semantics

For every successful transition:

state_version = state_version + 1

Transition MUST be rejected if:

incoming_state_version != current_state_version

No implicit transitions allowed.
No version rollback allowed.

---

# 4. Hard Safety Invariants

Across all transitions:

1. Exactly one active transport in ATTACHED.
2. No active transport in RECOVERING.
3. No transport binding in TERMINATED.
4. SessionID remains constant until TERMINATED.
5. Every state mutation must emit audit event.

---

# 5. Forbidden Transitions

The following transitions are invalid:

- ATTACHED → BIRTH
- TERMINATED → ANY
- VOLATILE → BIRTH
- DEGRADED → BIRTH
- RECOVERING → ATTACHED (without REATTACH_SUCCESS)
- ATTACHED → ATTACHED (without version increment)

Invalid transition attempt → reject + security event.

---

# 6. Deterministic Termination Conditions

Session must enter TERMINATED if:

- Session TTL expired
- Recovery TTL expired
- Ownership ambiguity detected
- Version conflict unrecoverable
- Dual-active binding attempt detected
- Policy limit exceeded

Termination must include reason_code.

---

# 7. Determinism Guarantee

Given identical:

- Initial state
- Event sequence
- Policy configuration

The state machine must produce identical outputs.

No probabilistic behavior allowed.

---

# Final Principle

Continuity is permitted.
Ambiguity is not.

If correctness cannot be guaranteed,
the session must terminate explicitly.

Session is the anchor.
Transport is volatile.