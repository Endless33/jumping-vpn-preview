# Behavioral Specification — Jumping VPN (Preview)

This document provides a machine-oriented behavioral contract for Jumping VPN.

It defines:
- explicit states
- allowed transitions
- switch conditions (policy gates)
- timeout semantics (TTL boundaries)
- invariants and measurable guarantees

This is a spec for review and reproducible reasoning.
It is not a claim of production completeness.

---

## 1) Definitions

**Session**
A persistent identity context with policy, state, and cryptographic binding.

**Transport**
A replaceable attachment used to carry packets (UDP/TCP/QUIC candidates).

**Active Binding**
Exactly one transport is ACTIVE for a session at any time.

**Transport Death**
No viable delivery within a bounded window (policy-defined).

**Degradation**
Delivery continues but violates quality floors (loss/latency/jitter).

---

## 2) State Model

### 2.1 Session States

- `BIRTH`       — created, not yet attached to any transport
- `ATTACHED`    — active binding exists and meets policy quality floors
- `VOLATILE`    — instability detected (signals exceed thresholds), still attached or switching
- `DEGRADED`    — session continues with restricted behavior; quality violations persist
- `RECOVERING`  — explicit recovery attempt in progress (reattach/switch)
- `TERMINATED`  — session ended deterministically (no recovery path within bounds)

### 2.2 Transport State (Conceptual)

- `CANDIDATE`   — eligible transport option
- `ACTIVE`      — the only current binding
- `REJECTED`    — refused by policy or validation
- `DEAD`        — unusable

---

## 3) Hard Invariants (Safety Contract)

I1. **Single Active Binding**
A session MUST have at most one ACTIVE transport binding.

I2. **Session Identity Continuity**
`session_id` MUST NOT change across transport switches/reattach.

I3. **No Silent Reset**
A session MUST NOT be implicitly renegotiated or reset due to transport volatility.

I4. **Deterministic Transitions**
All state transitions MUST be explicit and reason-coded.

I5. **Bounded Recovery**
Recovery attempts MUST be bounded by policy (time + switch rate).

I6. **Fail Closed on Ambiguity**
If ownership or freshness is ambiguous, reattach MUST be rejected deterministically.

---

## 4) Timeout Semantics (Policy Boundaries)

### 4.1 Session TTL (Identity Lifetime)
**`SessionTTL`**
Maximum lifetime of a session identity.
When expired:
- state MUST transition to `TERMINATED` (reason: `TTL_SESSION_EXPIRED`)
- a new session MUST be established via explicit handshake

### 4.2 Transport-Loss TTL (Continuity Window)
**`TransportLossTTL`**
Maximum time a session may remain alive without an ACTIVE transport.
When exceeded:
- transition to `TERMINATED` (reason: `TTL_TRANSPORT_LOSS_EXPIRED`)

### 4.3 Recovery Window
**`MaxRecoveryWindow`**
Maximum time allowed in `RECOVERING` before outcome is forced:
- `ATTACHED` if reattach succeeds
- `DEGRADED` or `TERMINATED` if bounds exceeded (policy-dependent)

### 4.4 Anti-Flap / Switch Limits
**`MaxSwitchesPerMinute`** + **`CooldownAfterSwitch`**
If switching exceeds bounds:
- transition to `DEGRADED` (reason: `POLICY_FLAP_LIMIT`)
Further attempts may be denied until cooldown expires.

---

## 5) Inputs / Signals

### 5.1 Health Signals (Examples)
- packet loss spikes (consecutive drops)
- latency increase beyond threshold
- jitter beyond threshold
- heartbeat timeouts
- NAT churn / port change (detected by control-plane)

### 5.2 Control Events
- `REATTACH_REQUEST`
- `REATTACH_ACCEPT`
- `REATTACH_REJECT`
- `TRANSPORT_KILLED` (forced test / kill switch)
- `OWNERSHIP_CONFLICT` (cluster)

---

## 6) Allowed Transitions (Machine Form)

### 6.1 Transition Table

| From        | To          | Trigger / Condition | Required Output |
|------------|-------------|---------------------|-----------------|
| BIRTH      | ATTACHED    | handshake succeeds | `STATE_CHANGE`, reason `HANDSHAKE_OK` |
| ATTACHED   | VOLATILE    | volatility signal exceeds threshold | `STATE_CHANGE`, reason `VOLATILITY_SIGNAL` |
| VOLATILE   | RECOVERING  | switch/reattach decision allowed by policy | `STATE_CHANGE`, reason `RECOVERY_START` |
| RECOVERING | ATTACHED    | `REATTACH_ACCEPT` and ACTIVE binding updated | `AUDIT_EVENT`, reason `TRANSPORT_SWITCH_OK` |
| RECOVERING | DEGRADED    | recovery bounds exceeded but session TTL ok | `STATE_CHANGE`, reason `RECOVERY_BOUNDS_EXCEEDED` |
| VOLATILE   | DEGRADED    | persistent quality violation + switch not allowed | `STATE_CHANGE`, reason `QUALITY_FLOOR_VIOLATION` |
| DEGRADED   | RECOVERING  | cooldown satisfied + candidates available | `STATE_CHANGE`, reason `RECOVERY_RETRY` |
| ANY        | TERMINATED  | SessionTTL expired | `STATE_CHANGE`, reason `TTL_SESSION_EXPIRED` |
| ANY        | TERMINATED  | TransportLossTTL exceeded with no ACTIVE binding | `STATE_CHANGE`, reason `TTL_TRANSPORT_LOSS_EXPIRED` |
| ANY        | TERMINATED  | explicit policy termination | `STATE_CHANGE`, reason `POLICY_TERMINATION` |

Notes:
- `ANY` excludes `TERMINATED` (terminal state).
- No implicit transitions are allowed.

---

## 7) Reattach Validation (Security Contract)

Reattach MUST be validated by:

- **Proof-of-possession** (session-bound secret / key material)
- **Freshness marker** (nonce/timestamp) within a bounded window
- **Anti-replay tracking** (reject duplicate freshness tokens)
- **Ownership authority** (single owner invariant)

Failure cases MUST be explicit:

- `REATTACH_REJECT` reason `AUTH_FAIL`
- `REATTACH_REJECT` reason `REPLAY_DETECTED`
- `REATTACH_REJECT` reason `OWNERSHIP_CONFLICT`
- `REATTACH_REJECT` reason `POLICY_DENY`

---

## 8) Measurable Guarantees (What Reviewers Can Test)

G1. **No Session Reset**
Under transport death (with backup available), `session_id` remains unchanged.

G2. **No Dual-Active**
At no point do two ACTIVE bindings exist for the same session.

G3. **Bounded Recovery Time**
Recovery completes within `MaxRecoveryWindow` or ends explicitly.

G4. **Audit Visibility**
Every state transition yields a reason-coded event suitable for timeline reconstruction.

---

## 9) Scope Notes

This behavioral spec focuses on determinism and bounded recovery.
It does not define:
- full cryptographic construction
- full packet formats
- anonymity guarantees
- censorship bypass

---

Session is the anchor.  
Transport is volatile.