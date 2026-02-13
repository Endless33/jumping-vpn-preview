# Control Plane Sequence — Jumping VPN (Preview)

This document defines the control-plane message flow
for session establishment, transport death, and deterministic reattach.

It is written as a sequence-level contract,
not as a packet-level specification.

---

## 1) Initial Session Establishment

### Actors
- Client Agent
- Server Gateway
- Session Table / Ownership Layer

### Sequence

1. Client → Server: `HANDSHAKE_INIT`
2. Server:
   - validates client identity
   - creates new SessionID
   - allocates policy snapshot
   - records authoritative ownership
3. Server → Client: `HANDSHAKE_RESPONSE`
   - SessionID
   - session-bound key material (abstracted)
   - policy parameters
4. State transition:
   - `BIRTH → ATTACHED`
   - reason: `HANDSHAKE_OK`

### Guarantees

- SessionID must be globally unique
- Only one authoritative owner exists
- Initial transport binding becomes ACTIVE

---

## 2) Transport Health Monitoring

### Inputs

Client monitors:
- packet loss
- latency
- jitter
- heartbeat timeout

Server monitors:
- inactivity window
- heartbeat expiration
- control-plane anomalies

### Possible Outcomes

If health within thresholds:
- Remain `ATTACHED`

If thresholds exceeded:
- Transition `ATTACHED → VOLATILE`
- reason: `VOLATILITY_SIGNAL`

---

## 3) Transport Death Detection

Transport is declared DEAD if:

- No viable delivery within `TransportLossWindow`
- OR socket/channel explicitly closed
- OR path becomes unreachable

Client transition:
- `ATTACHED → RECOVERING`
- reason: `RECOVERY_START`

Server does NOT terminate immediately.
Session remains alive within `TransportLossTTL`.

---

## 4) Reattach Sequence

### 4.1 Client Initiates

Client → Server: `REATTACH_REQUEST`
Includes:
- SessionID
- Proof-of-possession
- Freshness marker (nonce/timestamp)
- Optional transport metadata

---

### 4.2 Server Validation Steps (Deterministic Order)

1. Session exists?
   - If no → `REATTACH_REJECT` (`SESSION_NOT_FOUND`)

2. Session TTL expired?
   - If yes → `REATTACH_REJECT` (`SESSION_EXPIRED`)

3. Ownership authority valid?
   - If ambiguous → `REATTACH_REJECT` (`OWNERSHIP_CONFLICT`)

4. Proof-of-possession valid?
   - If no → `REATTACH_REJECT` (`AUTH_FAIL`)

5. Freshness within window?
   - If invalid → `REATTACH_REJECT` (`FRESHNESS_INVALID`)

6. Replay detected?
   - If yes → `REATTACH_REJECT` (`REPLAY_DETECTED`)

7. Policy allows switch?
   - If rate/cooldown exceeded → `REATTACH_REJECT` (`POLICY_DENY`)

If all pass:

- Update ACTIVE binding atomically
- Increment state_version
- Emit `TRANSPORT_SWITCH_OK`
- Transition `RECOVERING → ATTACHED`

---

## 5) Failure Outcomes

### Case A — Temporary Instability

If reattach rejected but bounds not exceeded:
- Transition `RECOVERING → VOLATILE`
- Retry allowed after cooldown

---

### Case B — Recovery Window Exceeded

If `MaxRecoveryWindow` exceeded:
- Transition to `DEGRADED`
- reason: `RECOVERY_BOUNDS_EXCEEDED`

---

### Case C — TransportLossTTL Exceeded

If no ACTIVE binding before TTL:
- Transition to `TERMINATED`
- reason: `TTL_TRANSPORT_LOSS_EXPIRED`

---

## 6) Anti-Flap Protection

Switch is allowed only if:

- Switches in last minute < `MaxSwitchesPerMinute`
- Cooldown after last switch satisfied
- Candidate transport quality exceeds minimum floor

Otherwise:
- Transition to `DEGRADED`
- reason: `POLICY_FLAP_LIMIT`

---

## 7) Cluster Authority Model (If Distributed)

If deployed across multiple nodes:

- Session ownership must be authoritative
- Reattach must update ownership atomically
- Dual-active binding is forbidden

If conflict detected:
- Reject reattach
- Emit `SEC_OWNERSHIP_ANOMALY`

Consistency > availability.

---

## 8) Observability Contract

Every state transition MUST emit:

- `session_id`
- `previous_state`
- `new_state`
- `reason_code`
- `ts_ms`
- `state_version`

This enables full reconstruction of the session timeline.

---

## 9) Explicit Non-Behavior

The control plane does NOT:

- Implicitly renegotiate identity
- Silently rotate session identifiers
- Continue under ambiguous ownership
- Retry infinitely without bounds

Ambiguity must result in explicit rejection or termination.

---

Session is the anchor.  
Transport is volatile.