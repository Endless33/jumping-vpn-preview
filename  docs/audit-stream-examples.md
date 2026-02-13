# Audit Stream Examples — Jumping VPN (Preview)

This document shows example audit events emitted by the runtime demo.

The goal is to demonstrate:

- Explicit state transitions
- Deterministic recovery
- Replay rejection
- Bounded recovery window
- No silent identity reset
- Single active transport invariant

These examples correspond to:
core/runtime_demo_events.py

---

## 1. Session Initialization

```json
{
  "ts_ms": 0,
  "event_type": "TRANSPORT_SELECTED",
  "session_id": "SESSION_EVT_01",
  "state_version": 0,
  "reason_code": "ACTIVE_SELECTED",
  "details": {
    "active": "udp-primary"
  }
}
```

Meaning:
Initial transport binding selected.
Session is in ATTACHED state.

---

## 2. Transport Death

```json
{
  "ts_ms": 1200,
  "event_type": "TRANSPORT_DEAD",
  "session_id": "SESSION_EVT_01",
  "state_version": 1,
  "reason_code": "TRANSPORT_FAILURE",
  "details": {}
}
```

Transition:
ATTACHED → RECOVERING

No renegotiation.
No identity reset.
State version increments.

---

## 3. Successful Reattach

```json
{
  "ts_ms": 1500,
  "event_type": "REATTACH_ACCEPTED",
  "session_id": "SESSION_EVT_01",
  "state_version": 2,
  "reason_code": "REATTACH_SUCCESS",
  "details": {
    "nonce": 1
  }
}
```

Transition:
RECOVERING → ATTACHED

Guarantees:
- SessionID unchanged
- No dual-active transport
- Version monotonic

---

## 4. Replay Attempt (Rejected)

```json
{
  "ts_ms": 1510,
  "event_type": "REPLAY_REJECTED",
  "session_id": "SESSION_EVT_01",
  "state_version": 2,
  "reason_code": "NONCE_REPLAY",
  "details": {
    "nonce": 1
  }
}
```

Properties:
- No state mutation
- No transport change
- Explicit security event
- Deterministic rejection

---

## 5. Final Snapshot

```json
{
  "ts_ms": 3000,
  "event_type": "SNAPSHOT",
  "session_id": "SESSION_EVT_01",
  "state_version": 2,
  "reason_code": "FINAL",
  "details": {
    "state": "ATTACHED",
    "active_transport": "udp-backup",
    "switch_count": 1,
    "recovery_attempts": 1
  }
}
```

Observations:
- Session remains ATTACHED
- Transport successfully replaced
- Switch bounded
- Recovery completed within policy window

---

# What Reviewers Should Verify

## 1. Determinism

Every transition:
- Is explicit
- Has a reason_code
- Increments state_version

No silent behavior.

---

## 2. Safety Invariants

Audit stream must never show:

- Dual ACTIVE transports
- State rollback
- Silent identity reset
- Implicit termination

---

## 3. Bounded Recovery

Recovery must:
- Complete within max_recovery_window_ms
OR
- End in explicit TERMINATED

Never infinite retry loops.

---

## 4. Replay Handling

Replay attempts:
- Must not mutate session state
- Must be logged
- Must not trigger transport switch

---

## 5. Observability Rule

Observability is:

Non-blocking  
Deterministic  
Complete for critical transitions  

Logging failure must never change session correctness.

---

# Why This Matters

Many VPN systems hide failover behavior inside transport layers.

Jumping VPN makes:

- Failover explicit
- State visible
- Recovery bounded
- Decisions auditable

The audit stream is not cosmetic.
It is a correctness surface.

---

Session is the anchor.  
Transport is volatile.  
Behavior is explicit.