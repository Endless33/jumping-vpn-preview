# Reason Codes — Jumping VPN (Preview)

This document defines canonical reason codes used across:
- state transitions
- audit events
- security events
- reattach outcomes

Reason codes are part of the behavioral contract.
They must be stable, explicit, and machine-readable.

---

## 1) Format

- UPPER_SNAKE_CASE
- No spaces
- Deterministic meaning (not marketing)
- One code = one primary cause

Optional extension:
- `DETAILS` fields may include structured metadata (thresholds, counters, peer ids, etc.)

---

## 2) State Transition Reasons

### 2.1 Session Establishment

- `HANDSHAKE_OK`
  - Session created and attached successfully.
- `HANDSHAKE_FAIL`
  - Handshake rejected (auth/policy/invalid).

### 2.2 Volatility Detection

- `VOLATILITY_SIGNAL`
  - Instability threshold exceeded (loss/latency/jitter/heartbeat).
- `QUALITY_FLOOR_VIOLATION`
  - Delivery continues but violates policy quality floors.
- `HEALTH_RECOVERED`
  - Stability window detected (signals back within thresholds).

### 2.3 Recovery / Switching

- `RECOVERY_START`
  - Explicit recovery attempt initiated.
- `TRANSPORT_SWITCH_OK`
  - Active transport binding updated successfully.
- `TRANSPORT_SWITCH_DENIED`
  - Switch was requested but denied by policy/limits.
- `RECOVERY_RETRY`
  - Recovery attempted again after cooldown / gating.
- `RECOVERY_BOUNDS_EXCEEDED`
  - Recovery exceeded policy bounds (time or attempts).

### 2.4 Degraded Mode

- `ENTER_DEGRADED_MODE`
  - Session entered DEGRADED due to persistent instability or bounded failures.
- `EXIT_DEGRADED_MODE`
  - Session recovered to ATTACHED after stability conditions met.

### 2.5 Termination

- `TTL_SESSION_EXPIRED`
  - Session identity lifetime expired.
- `TTL_TRANSPORT_LOSS_EXPIRED`
  - No active transport within TransportLossTTL.
- `POLICY_TERMINATION`
  - Explicit policy termination (e.g., abuse bounds exceeded).
- `FATAL_PROTOCOL_ERROR`
  - Deterministic internal protocol failure; terminal.

---

## 3) Reattach Outcomes

### 3.1 Success

- `REATTACH_ACCEPT`
  - Reattach accepted and binding updated.

### 3.2 Rejection

- `AUTH_FAIL`
  - Proof-of-possession invalid.
- `FRESHNESS_INVALID`
  - Nonce/timestamp invalid or outside window.
- `REPLAY_DETECTED`
  - Reattach token reused within replay window.
- `OWNERSHIP_CONFLICT`
  - Cluster authority ambiguous (split-brain risk).
- `SESSION_NOT_FOUND`
  - Unknown session_id.
- `SESSION_EXPIRED`
  - Session exists but expired by TTL.
- `POLICY_DENY`
  - Policy denies reattach (limits, cooldown, constraints).
- `RATE_LIMITED`
  - Reattach request rate exceeded.

---

## 4) Security Events

- `SEC_REPLAY_ATTEMPT`
  - Detected replay attempt.
- `SEC_SESSION_FIXATION_ATTEMPT`
  - Attempt to bind a session_id without valid possession.
- `SEC_OWNERSHIP_ANOMALY`
  - Unexpected ownership/authority condition.
- `SEC_ABUSE_CONTROL_PLANE`
  - Control-plane abuse signals (reattach floods, invalid bursts).

---

## 5) Observability / Audit Events

- `AUDIT_INVARIANT_OK_SINGLE_ACTIVE`
  - Confirmed: single active binding held.
- `AUDIT_INVARIANT_OK_NO_RESET`
  - Confirmed: session_id continuity held.
- `AUDIT_POLICY_LIMIT_TRIGGERED`
  - Policy limit fired (switch rate, cooldown, TTL boundary).
- `AUDIT_RECOVERY_TIMELINE`
  - Recovery metrics emitted (duration, attempts, gating decisions).

---

## 6) Notes

- Reason codes are not exhaustive; new codes may be added.
- Backward compatibility matters:
  - do not rename existing codes
  - add new codes explicitly
- Any state transition must include exactly one primary reason code.

---

Session is the anchor.  
Transport is volatile.