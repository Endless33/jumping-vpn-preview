# Attack Surface Breakdown — Jumping VPN (Preview)

This document enumerates the primary attack surfaces introduced by a
session-centric, transport-volatile VPN architecture.

The goal is clarity:
every feature expands the surface area.
This document makes that surface explicit.

---

# 1. Control Plane Surfaces

## 1.1 REATTACH_REQUEST Flooding

Attack:
- Adversary floods reattach attempts to exhaust CPU/state.

Mitigations (design targets):
- Early rejection for unknown SessionID
- Rate limiting per source / per SessionID
- Bounded parsing and constant-time validation where possible
- Fail-closed behavior (no state mutation on invalid reattach)

Signals:
- Audit + security events on abuse patterns

---

## 1.2 Session Table Exhaustion

Attack:
- Create many sessions to exhaust memory/state.

Mitigations:
- Session TTL enforcement
- Hard caps per IP / subnet / token
- Eviction policy with reason-coded termination
- Bounded session metadata

---

## 1.3 Policy Abuse (Switch Trigger Manipulation)

Attack:
- Induce volatility signals to force switches (flapping).

Mitigations:
- Hysteresis (multi-signal gating)
- Cooldown windows after switches
- MaxSwitchesPerMinute enforcement
- DEGRADED mode under persistent churn

---

# 2. Transport Layer Surfaces

## 2.1 NAT Rebinding Confusion

Attack:
- Exploit NAT rebinding to confuse transport identity.

Mitigations:
- Transport identity is not trusted alone
- Binding requires session proof-of-possession + freshness
- Old transport becomes invalid after rebind confirmation

---

## 2.2 Path Injection / Fake Candidates

Attack:
- Maliciously advertise candidate paths (in environments where discovery exists).

Mitigations:
- Candidates are policy-filtered
- Only authenticated endpoints accepted
- Deterministic selection rules reduce ambiguity

---

# 3. Cryptographic Surfaces (Abstract)

## 3.1 Replay of Reattach Messages

Attack:
- Replay old REATTACH_REQUEST to hijack or desync session.

Mitigations:
- Freshness markers (nonce / counter / timestamp window)
- Replay window tracking (bounded memory)
- Replays rejected deterministically and logged

---

## 3.2 Session Fixation

Attack:
- Force a victim to bind to attacker-chosen SessionID.

Mitigations:
- SessionID is derived/bound to cryptographic context
- Reattach requires proof-of-possession
- Session creation is authenticated

---

## 3.3 Transport Hijack During Migration

Attack:
- Attempt to claim a session during transport switch.

Mitigations:
- Strong binding(SessionID, Keys, Identity)
- Reattach must validate possession + freshness
- Cluster ownership rejects ambiguous continuation

---

# 4. Observability Surfaces

## 4.1 Log / Telemetry Injection

Attack:
- Inject fake events into SIEM pipelines.

Mitigations:
- Logs signed or integrity-protected (design target)
- Correlate events with server-side truth
- Separate control-plane truth from exported telemetry

---

## 4.2 Telemetry Backpressure

Attack/Failure:
- Observability pipeline outage causes protocol failure.

Mitigations:
- Observability is non-blocking
- Protocol state must not depend on log delivery
- Backpressure degrades telemetry, not correctness

---

# 5. Cluster Surfaces

## 5.1 Split-Brain Acceptance

Attack/Failure:
- Two nodes accept reattach simultaneously.

Mitigations:
- Authoritative ownership model (sticky routing or atomic store)
- CAS-based state updates with versioning
- Reject ambiguous continuation

Consistency is preferred over availability.

---

# 6. Explicit Non-Goals (Security)

This system does NOT claim:

- Endpoint compromise protection
- Full anonymity against global adversaries
- DPI/censorship bypass guarantees

The security scope is focused on:

Deterministic continuity under bounded volatility
without silent identity reset or undefined behavior.

---

# 7. Summary

Attack surfaces exist.
They are acknowledged explicitly.

The design goal is not “no attacks”.
The goal is:

- bounded behavior
- deterministic outcomes
- explicit termination under ambiguity
- audit visibility

---

Session is the anchor.
Transport is volatile.