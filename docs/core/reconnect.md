# Jumping VPN — Reconnect Semantics (Core)

Reconnect defines how a session preserves identity while replacing a failing
transport under volatility. It is a deterministic, auditable, policy‑bounded
process.

Session is the anchor.  
Transport is volatile.

---

## 1. Reconnect Path (Formal)

The only valid reconnect path:


ATTACHED → VOLATILE → DEGRADED → REATTACHING → RECOVERING → ATTACHED


Any deviation is a protocol violation.

---

## 2. Reattach Sequence (Mandatory Events)

A valid reattach attempt MUST emit:

1. `ReattachRequest`
2. `ReattachProof`
3. `TransportSwitch`
4. Audit events:
   - `NO_IDENTITY_RESET`
   - `NO_DUAL_ACTIVE_BINDING`

These events guarantee identity continuity and prevent hidden renegotiation.

---

## 3. Timers

### `volatility_timeout_ms`
Instability must persist for this duration before entering `VOLATILE`.

### `reattach_grace_ms`
Maximum allowed time for reattachment before failure.

### `recovery_window_ms`
Time window for metrics to stabilize after switch.

Timers enforce bounded adaptation.

---

## 4. Success Conditions

Reconnect succeeds if:

- session_id remains constant  
- new transport validated  
- metrics stabilize  
- no identity reset  
- no dual-active binding  
- state returns to `ATTACHED`  

This is the definition of continuity.

---

## 5. Failure Conditions

Reconnect fails if:

- no candidate transport exists  
- `reattach_grace_ms` expires  
- identity proof fails  
- dual-active binding detected  
- metrics diverge beyond policy bounds  

Failure leads to:


TERMINATED(reason="reattach_failed")


---

## 6. Output Events

Reconnect emits:

- `VolatilitySignal`
- `MultipathScoreUpdate`
- `ReattachRequest`
- `ReattachProof`
- `TransportSwitch`
- `RecoverySignal`
- `SessionStateChange`
- `AuditEvent`

These events form the observable trace of the reconnect process.

---

## 7. Relationship to Invariants

Reconnect enforces:

- identity immutability  
- explicit transitions  
- deterministic switch  
- no dual-active binding  
- bounded adaptation  

Reconnect is where invariants become runtime behavior.

---

## Summary

Reconnect is the controlled replacement of a failing transport.
It is deterministic, auditable, and identity‑preserving.

Session is the anchor.  
Transports come and go.