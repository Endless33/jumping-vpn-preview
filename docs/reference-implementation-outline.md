# Reference Implementation Outline — Jumping VPN (Preview)

This document describes a production-oriented reference architecture for Jumping VPN.

It is an implementation outline (module boundaries + responsibilities),
not a claim of completed production code.

---

## 1. System Goal

Provide deterministic session continuity under transport volatility.

Key contract:
- Session is the identity anchor
- Transport is replaceable
- Recovery is bounded, auditable, and policy-driven

---

## 2. High-Level Components

### 2.1 Client Agent
Responsibilities:
- Maintain session context (SessionID + keys + policy)
- Monitor transport health signals (loss/latency/jitter)
- Initiate REATTACH_REQUEST on transport death or policy-driven switch
- Enforce local anti-flap limits and cooldown windows
- Emit client-side observability events (optional)

Interfaces:
- Transport adapters (UDP/TCP/QUIC candidates)
- Control-plane messages (handshake, reattach, errors)

---

### 2.2 Server Gateway (Edge)
Responsibilities:
- Validate session-bound reattach (proof-of-possession + freshness)
- Bind a new transport to an existing session
- Enforce server-side anti-abuse limits (rate limits, TTL bounds)
- Emit audit-grade events for all state transitions
- Provide deterministic errors and transitions (no silent behavior)

Interfaces:
- Transport listeners (UDP/TCP/QUIC)
- Session table / ownership layer
- Observability export (non-blocking)

---

### 2.3 Session Table / Ownership Layer
Responsibilities:
- Authoritative session ownership (single owner invariant)
- TTL enforcement:
  - session TTL
  - transport-loss TTL
- Versioned state transitions (prevent rollback)
- Atomic ownership update on reattach
- Eviction policy with deterministic reason codes

Implementation options:
- Sticky routing (SessionID -> node)
- Atomic shared store (CAS/transactions) + version counter

---

### 2.4 Policy Engine
Responsibilities:
- Evaluate health thresholds and bounds:
  - MaxRecoveryWindowMs
  - MaxSwitchesPerMinute
  - TransportLossTtlMs
  - Quality floors (loss/latency/jitter)
- Decide allowed transports and candidate filtering
- Decide whether session enters DEGRADED vs TERMINATED

Policy must be deterministic and reproducible.

---

### 2.5 Observability Layer (Non-Blocking)
Responsibilities:
- Emit STATE_CHANGE, AUDIT_EVENT, SECURITY_EVENT
- Export to SIEM/NOC pipelines without blocking correctness
- Provide a session timeline view:
  - transport switches
  - reasons
  - recovery latency
  - policy-limit triggers

Design rule:
Logging failures degrade telemetry, not protocol correctness.

---

## 3. Control Plane Message Flow (Abstract)

### 3.1 Initial Session Establishment
1) HANDSHAKE_INIT
2) HANDSHAKE_RESPONSE
3) Session enters ATTACHED

Outputs:
- SessionID
- Key context
- Policy snapshot

---

### 3.2 Transport Death / Reattach
Trigger:
- TRANSPORT_DEAD (no viable delivery within bounded window)

Flow:
1) Client enters RECOVERING
2) Client sends REATTACH_REQUEST(SessionID, proof, freshness, metadata)
3) Server validates:
   - ownership authority
   - proof-of-possession
   - freshness / anti-replay window
4) Server binds new transport
5) Server emits TransportSwitch + STATE_CHANGE
6) Client returns to ATTACHED

Failure outcomes are explicit:
- REATTACH_FAIL -> VOLATILE / DEGRADED
- TTL/policy exceeded -> TERMINATED

---

## 4. Data Plane (Out of Scope Here)

Data-plane encryption and packet formats are not specified in this outline.
This repo focuses on behavioral continuity, determinism, and bounded recovery.

---

## 5. Hard Safety Rules (Implementation Targets)

- No dual-active transport binding
- No silent identity reset
- No implicit state transitions
- Recovery is bounded by policy
- Ambiguity -> reject or terminate deterministically
- All critical transitions are auditable

---

## 6. Engineering Notes

This outline is intended to help reviewers reason about:

- Implementation complexity
- Module boundaries
- Integration points
- Operational safety under volatility

---

Session is the anchor.  
Transport is volatile.