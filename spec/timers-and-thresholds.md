# Jumping VPN — Timers & Thresholds (Public Preview)

Status: Draft (architectural validation)

This document defines normative timers, thresholds, and window semantics
used by the behavioral state machine.

Values are policy-configurable.
This spec defines meanings, units, and recommended starting defaults.

---

## 0. Conventions

- All time values are in **milliseconds** unless stated otherwise.
- A "window" refers to a bounded observation interval for metrics.
- All thresholds are enforced by policy (bounded adaptation invariant).

---

## 1. Session Timers

### 1.1 SESSION_MAX_LIFETIME_MS
Meaning:
- Maximum allowed lifetime of a session since creation.

Behavior:
- If `session_age_ms > SESSION_MAX_LIFETIME_MS` → `TERMINATED`
- Reason code: `session_lifetime_exceeded`

Recommended default:
- 8h to 24h (deployment dependent)

---

### 1.2 TRANSPORT_LOST_TTL_MS
Meaning:
- Maximum time a session may remain without any valid active transport binding.

Behavior:
- If `no_active_transport` AND `transportless_age_ms > TRANSPORT_LOST_TTL_MS` → `TERMINATED`
- Reason code: `transport_ttl_exceeded`

Recommended default:
- 10s to 60s (deployment dependent)

---

## 2. Volatility & Degradation Timers

### 2.1 HEARTBEAT_INTERVAL_MS
Meaning:
- How often the client emits a heartbeat/control message on the active transport.

Recommended default:
- 250ms to 1500ms

Notes:
- Heartbeats support faster dead detection under NAT and mobile networks.

---

### 2.2 HEARTBEAT_VOLATILE_MS
Meaning:
- If no successful heartbeat or valid ACK is observed within this time,
  the session is considered volatile.

Behavior:
- If `heartbeat_age_ms > HEARTBEAT_VOLATILE_MS` → `ATTACHED → VOLATILE`
- Reason code: `heartbeat_timeout`

Recommended default:
- 2x to 4x `HEARTBEAT_INTERVAL_MS`

---

### 2.3 VOLATILE_TO_DEGRADED_MS
Meaning:
- Maximum allowed time in `VOLATILE` before entering `DEGRADED`.

Behavior:
- If `volatile_duration_ms > VOLATILE_TO_DEGRADED_MS` → `VOLATILE → DEGRADED`
- Reason code: `volatile_persisted`

Recommended default:
- 1500ms to 8000ms

---

## 3. Loss & Latency Thresholds

### 3.1 LOSS_WINDOW_MS
Meaning:
- Observation window size for loss ratio calculations.

Recommended default:
- 1000ms to 5000ms

---

### 3.2 LOSS_VOLATILE_THRESHOLD
Meaning:
- Loss ratio threshold above which the session is considered volatile.

Definition:
- `loss_ratio = dropped_packets / (delivered_packets + dropped_packets)` measured over `LOSS_WINDOW_MS`

Behavior:
- If `loss_ratio(window) > LOSS_VOLATILE_THRESHOLD` → `ATTACHED → VOLATILE`
- Reason code: `loss_threshold_exceeded`

Recommended default:
- 0.10 to 0.30 (10%–30%)

---

### 3.3 MAX_CONSECUTIVE_DROPS
Meaning:
- Maximum allowed consecutive delivery failures before triggering volatility/switch.

Behavior:
- If `consecutive_drops >= MAX_CONSECUTIVE_DROPS` → `ATTACHED → VOLATILE` and may trigger recovery
- Reason code: `consecutive_drop_exceeded`

Recommended default:
- 3 to 7

---

### 3.4 LATENCY_WINDOW_MS (Optional)
Meaning:
- Observation window for latency/jitter metrics (if implemented).

Recommended default:
- 1000ms to 5000ms

---

### 3.5 LATENCY_VOLATILE_THRESHOLD_MS (Optional)
Meaning:
- Latency threshold above which the session may be considered volatile.

Behavior:
- If `p95_latency_ms(window) > LATENCY_VOLATILE_THRESHOLD_MS` → `ATTACHED → VOLATILE`
- Reason code: `latency_threshold_exceeded`

Recommended default:
- deployment dependent

---

## 4. Switching & Anti-Flapping Limits

### 4.1 MAX_SWITCHES_PER_MIN
Meaning:
- Maximum number of transport switches per 60 seconds.

Behavior:
- If exceeded → deny switch and enter `DEGRADED` (or remain degraded)
- Reason code: `switch_rate_limited`
- Emit: `TransportSwitchDenied`

Recommended default:
- 3 to 12

---

### 4.2 SWITCH_COOLDOWN_MS
Meaning:
- Minimum time between switch attempts to avoid oscillation.

Behavior:
- If a switch is attempted within cooldown → deny or delay attempt
- Reason code: `policy_denied`

Recommended default:
- 500ms to 5000ms

---

### 4.3 RECOVERY_WINDOW_MS
Meaning:
- Time window during which recovery attempts are allowed after entering `RECOVERING`.

Behavior:
- If recovery window expires without success → `RECOVERING → DEGRADED` or `TERMINATED` (policy dependent)

Recommended default:
- 2000ms to 15000ms

---

## 5. Candidate Transport Selection

### 5.1 CANDIDATE_MIN_COUNT
Meaning:
- Minimum number of available candidate transports required to attempt switching (policy dependent).

Recommended default:
- 1

### 5.2 CANDIDATE_SCORE_THRESHOLD (Optional)
Meaning:
- If using scoring, minimum score required for a candidate to be considered.

Recommended default:
- implementation dependent

---

## 6. Security Timers (Abstract)

These are defined abstractly in this preview:

### 6.1 REATTACH_PROOF_MAX_AGE_MS
Meaning:
- Maximum age of reattach proof material before being rejected.

Behavior:
- If proof age exceeds threshold → reject reattach
- Reason code: `reattach_validation_failed`

Recommended default:
- 1000ms to 10000ms

### 6.2 REPLAY_WINDOW_SIZE
Meaning:
- Anti-replay window size for reattach validation (nonce/counter based).

Recommended default:
- implementation dependent

---

## 7. Summary Defaults (Suggested Starter Set)

A practical starter set for validation:

- `HEARTBEAT_INTERVAL_MS`: 500
- `HEARTBEAT_VOLATILE_MS`: 2000
- `LOSS_WINDOW_MS`: 2000
- `LOSS_VOLATILE_THRESHOLD`: 0.20
- `MAX_CONSECUTIVE_DROPS`: 3
- `VOLATILE_TO_DEGRADED_MS`: 4000
- `MAX_SWITCHES_PER_MIN`: 8
- `SWITCH_COOLDOWN_MS`: 1500
- `TRANSPORT_LOST_TTL_MS`: 15000

These are not claims. They are initial validation defaults.

---

## Final Note

Timers are not features.
They define the behavioral contract.

Jumping VPN treats volatility as modeled state,
with bounded adaptation and deterministic failure boundaries.