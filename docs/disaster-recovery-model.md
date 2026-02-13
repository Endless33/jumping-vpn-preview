# Disaster Recovery Model — Jumping VPN (Preview)

This document defines catastrophic failure handling
in large-scale or data-center-level incidents.

Scope:

- Full node failure
- Full data-center outage
- Store corruption
- Regional partition
- Mass transport collapse

Correctness remains the primary invariant.

---

# 1. Core Principle

In disaster scenarios:

Correctness > Continuity > Availability

If correctness cannot be guaranteed,
the session must terminate explicitly.

---

# 2. Disaster Categories

## 2.1 Single Node Failure

Scenario:
Active session owner crashes.

Required behavior:

Sticky model:
- Session unavailable until TTL expiration.

Shared store model:
- New node attempts ownership acquisition.
- Must validate:
  - session TTL valid
  - no version rollback
  - no conflicting owner
- If safe → transition to RECOVERING.
- If ambiguous → TERMINATED.

No silent failover.

---

## 2.2 Data Center Outage

Scenario:
Entire edge cluster becomes unreachable.

Behavior:

Client enters RECOVERING.
Client may attempt alternate region (if configured).

Server-side rules:

- Session reattach allowed only if:
  - ownership resolved
  - version continuity validated
  - TTL not expired

If region-level state replication lag creates ambiguity:

Terminate deterministically.

---

## 2.3 Session Store Corruption

Scenario:
Shared session store corrupted or inconsistent.

Required action:

- Reject all reattach requests.
- Emit critical security event.
- Enter fail-closed mode.

No partial acceptance allowed.

---

## 2.4 Network Partition (Split Region)

Scenario:
Cluster splits into two partitions.

Each side may believe it owns session.

Required behavior:

- Only side with valid ownership token may mutate.
- Version authority enforced.
- If ownership cannot be proven → reject.

If ambiguity persists:

Session TERMINATED.

---

## 2.5 Mass Transport Collapse

Scenario:
Regional network instability.
Packet loss spikes across many sessions.

Behavior:

- Sessions enter VOLATILE or DEGRADED.
- Rate limits prevent cascade switching.
- Recovery bounded by MaxRecoveryWindow.

If transport-loss TTL exceeded:

Terminate deterministically.

No infinite retry loops.

---

# 3. Recovery Order of Operations

In catastrophic recovery:

1. Validate ownership authority
2. Validate version continuity
3. Validate TTL constraints
4. Validate anti-replay freshness
5. Bind new transport
6. Emit state transition

If any step fails → reject or terminate.

---

# 4. State Integrity Rule

Disaster recovery must NOT:

- Roll back state_version
- Duplicate active transport
- Recreate session silently
- Downgrade security checks

---

# 5. Session Resurrection Policy

Jumping VPN does NOT support:

- Implicit session resurrection
- Session cloning across regions
- Silent recreation after TTL expiration

After TERMINATED:

New session required.

---

# 6. Observability Under Disaster

Logging layer must:

- Remain non-blocking
- Never influence state mutation
- Preserve deterministic reason codes

Telemetry loss must not cause state corruption.

---

# 7. Disaster Safety Invariants

Across all disaster scenarios:

1. No dual-active binding.
2. No silent identity reset.
3. No ambiguous ownership continuation.
4. No version rollback.
5. Explicit termination over unsafe continuation.

---

# 8. Operational Philosophy

Resilience is not infinite retry.

Resilience is bounded recovery under strict correctness rules.

---

# Final Principle

If disaster prevents provable correctness,
the session must end explicitly.

Transport instability is tolerable.
Ownership ambiguity is not.
State corruption is not.

Session is the anchor.
Transport is volatile.
Correctness is non-negotiable.