# Attack Surface Map — Jumping VPN (Preview)

This document enumerates the primary attack surfaces
for the Jumping VPN architectural model.

It focuses on the control-plane and session lifecycle behavior.

This is not a penetration test.
It is a structural threat exposure analysis.

---

## 1) Attack Surface Categories

The system exposes four primary surfaces:

1. Client Agent Surface
2. Server Gateway Surface
3. Session Ownership / Storage Layer
4. Observability & Export Layer

Each surface is analyzed independently.

---

# 2) Client Agent Surface

### 2.1 Transport Interface

Attack vectors:
- Packet loss injection
- Delay injection
- Jitter amplification
- NAT churn forcing
- Artificial transport flapping

Impact:
- Trigger VOLATILE / RECOVERING
- Induce reattach attempts

Mitigation:
- Bounded recovery window
- Switch rate limiting
- Cooldown enforcement
- Deterministic termination if unstable

Design principle:
Transport disruption must not hijack session identity.

---

### 2.2 Control-Plane Injection

Attack vectors:
- Fake REATTACH_ACK
- Replay of previous server responses
- Message tampering

Mitigation:
- Proof-of-possession validation
- Nonce freshness checks
- Version matching
- Fail-closed rejection

---

### 2.3 Local Resource Exhaustion

Attack vectors:
- Rapid transport cycling
- CPU exhaustion via reattach attempts

Mitigation:
- Local rate limiter
- Policy-bound retry logic
- Recovery window TTL

---

# 3) Server Gateway Surface

### 3.1 Reattach Flooding

Attack vector:
- High-rate REATTACH_REQUEST
- Session enumeration attempts

Mitigation:
- Early reject unknown session_id
- Rate limiting (per-IP / per-session)
- Bounded replay window
- Lightweight pre-validation before heavy crypto

Fail-closed rule:
Control-plane must reject without mutating state.

---

### 3.2 Replay Attacks

Attack vector:
- Reuse of old nonce
- Delayed reattach messages

Mitigation:
- Monotonic nonce enforcement
- Sliding replay window
- Reject stale or duplicate nonce
- Log security event

---

### 3.3 Dual-Active Binding Attempt

Attack vector:
- Attempt to bind second transport
- Parallel reattach race

Mitigation:
- Atomic CAS on state_version
- Single active transport invariant
- Ownership authority enforcement

Ambiguity must terminate or reject.

---

### 3.4 TTL Bypass Attempt

Attack vector:
- Reattach after session TTL expiry
- Attempt to revive dead session

Mitigation:
- Strict TTL validation before binding
- TTL expiration → TERMINATED
- No silent revival

---

# 4) Session Ownership Layer

### 4.1 Split-Brain Risk (Clustered Deployment)

Attack scenario:
- Two nodes accept reattach simultaneously
- Network partition

Mitigation options:
- Sticky routing (preferred simplicity)
- Atomic versioned shared store (CAS)
- Reject on ownership ambiguity

Consistency > availability for identity safety.

---

### 4.2 Version Rollback

Attack vector:
- Stale state_version update
- Concurrent mutation race

Mitigation:
- Monotonic version increment
- Reject mismatched version
- No implicit override

Version rollback is forbidden.

---

# 5) Observability Layer

### 5.1 Log Delivery Failure

Attack scenario:
- SIEM offline
- Logging blocked

Mitigation:
- Observability must be non-blocking
- State transitions must not depend on export success

Logging failure must not break correctness.

---

### 5.2 Event Flooding

Attack vector:
- Trigger excessive volatility
- Generate audit spam

Mitigation:
- Event rate bounds
- Switch rate limit
- Recovery TTL enforcement

---

# 6) Abuse Scenarios

## 6.1 Malicious Transport Oscillation

Goal:
Force repeated switches to degrade service.

Defense:
- Switch rate limit
- Cooldown window
- Transition to DEGRADED
- Explicit termination if bounds exceeded

---

## 6.2 Control-Plane DoS

Goal:
Exhaust CPU via reattach validation.

Defense:
- Early session existence check
- Rate limiter before expensive validation
- Replay window bounding
- Proof-of-possession verification cost bounded

---

## 6.3 Identity Hijack Attempt

Goal:
Attach attacker-controlled transport to valid session.

Defense:
- Proof-of-possession required
- Nonce freshness enforced
- Version matching required
- Ownership validation required

Transport disruption alone must not hijack identity.

---

# 7) Explicit Non-Defended Areas (Out of Scope)

This architecture does NOT claim protection against:

- Compromised client endpoint
- Kernel-level malware
- Insider abuse with valid credentials
- Global traffic correlation adversary
- Full anonymity network attacks

Scope is limited to:

Deterministic session continuity under transport volatility.

---

# 8) Safety Principles

1. Fail closed on ambiguity.
2. Never allow dual-active identity.
3. Never silently reset identity.
4. Bound recovery attempts.
5. Make all critical transitions auditable.
6. Prefer termination over undefined behavior.

---

# 9) Residual Risk Areas (Research Ongoing)

- Cluster consistency under network partitions
- Replay window memory pressure at scale
- Extreme churn scenarios (100k+ sessions)
- Coordinated control-plane floods
- Cross-layer attack amplification

These areas require empirical validation.

---

# Summary

The primary attack surfaces are:

- Transport instability manipulation
- Control-plane replay and injection
- Session ownership ambiguity
- Resource exhaustion

Mitigation strategy is structural:

- Deterministic state machine
- Bounded adaptation
- Versioned mutation
- Explicit rejection rules
- Fail-closed invariants

Security is enforced by architecture,
not by heuristic behavior.

---

Session is the anchor.  
Transport is volatile.