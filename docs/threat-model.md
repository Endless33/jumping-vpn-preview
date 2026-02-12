# Jumping VPN — Threat Model (Public Preview)

This document describes the security threat model assumptions
and the intended protection goals of Jumping VPN.

This repository is an architectural preview.
It does not publish full cryptographic implementation details.

---

## 1. Scope

Jumping VPN focuses on **session continuity under transport volatility**.

It is designed to preserve a long-lived session identity while:
- transports fail or disappear
- IPs change
- NAT bindings expire
- packet loss and jitter spike
- paths compete or flap

The security model is designed around **reattachment safety** and **state integrity**.

---

## 2. Assets to Protect

Primary assets:

- **Session integrity**
  - Session identity must not be stolen, fixed, or silently replaced.

- **Transport reattachment safety**
  - A new transport must not be bound to an existing session without valid proof.

- **State machine integrity**
  - Session state must not diverge into undefined behavior under stress.

- **Auditability**
  - Critical session and transport decisions must remain observable and explainable.

Secondary assets (deployment dependent):
- Confidentiality of payload (depends on hardened crypto layer)
- Metadata reduction (depends on routing/veil layer)

---

## 3. Threat Actors

Assume adversaries may include:

- **On-path network attackers**
  - Can observe, delay, drop, or replay packets.

- **Off-path attackers**
  - Attempt spoofing, session fixation, or resource exhaustion.

- **Active disruptors**
  - Cause transport instability intentionally (jamming, shaping, forcing flaps).

- **NAT/Carrier interference**
  - Unpredictable rebinding and timeout behavior.

- **Infrastructure-level adversaries**
  - Misbehaving middleboxes, enterprise firewalls, DPI devices.

---

## 4. Adversary Capabilities (Assumptions)

The protocol assumes:

- The attacker can observe transport characteristics.
- The attacker can cause packet loss, jitter, and transient outages.
- The attacker can attempt replay of previously observed reconnect material.
- The attacker can attempt to trigger oscillation and switch storms.
- The attacker can probe endpoints for behavioral patterns.

The protocol does **not** assume:
- The attacker has endpoint compromise (see Non-Goals).
- The attacker can break strong cryptography (if properly implemented).

---

## 5. Security Goals

Jumping VPN aims to guarantee:

### G1 — Session continuity is not equal to transport continuity
Transport death must not automatically terminate a valid session.

### G2 — Reattachment requires cryptographic proof
A transport may be bound to an existing session only with valid session-bound proof.

### G3 — Replay resistance during reattachment
Old reattachment material must not be reusable to hijack or downgrade a session.

### G4 — Bounded, policy-controlled adaptation
Transport switching must be limited to prevent:
- oscillation
- abuse-driven switch storms
- silent instability loops

### G5 — Deterministic failure boundaries
If recovery is not possible within bounded rules,
the session must terminate cleanly and explicitly.

### G6 — Observability of critical decisions
State transitions, transport decisions, and security failures
must emit auditable events.

---

## 6. Key Threats & Intended Mitigations (High-Level)

### T1: Session Hijacking on Reattach
Risk:
- Attacker attempts to bind their transport to a victim session.

Mitigation intent:
- Session-bound proof required for reattachment.
- Transport origin is not trusted.
- Reattach acceptance is time/policy bounded.

### T2: Replay Attack on Reattach
Risk:
- Attacker replays previously observed reattach traffic.

Mitigation intent:
- Anti-replay window
- Monotonic counters / nonces (implementation dependent)
- Session lifetime constraints

### T3: Session Fixation
Risk:
- Attacker forces victim into attacker-controlled session context.

Mitigation intent:
- Strong binding between session ID, identity, and key context.
- Explicit session lifecycle controls.

### T4: Switch Storm / Oscillation Abuse
Risk:
- Attacker triggers endless switching to degrade service.

Mitigation intent:
- Switch rate limits
- Dampening / cooldown policy
- Degraded state handling

### T5: State Confusion / Undefined Transitions
Risk:
- Stress conditions cause undefined states or inconsistent recovery.

Mitigation intent:
- Strict state machine
- Deterministic transition rules
- Explicit terminal conditions

---

## 7. Non-Goals (Important)

Jumping VPN does **not** claim to provide:

- Endpoint compromise protection
- Anti-malware protection
- Guaranteed censorship bypass
- Full anonymity guarantees (Tor-like)
- Protection against physical access to devices
- Magic prevention of all traffic analysis

These are separate domains and require additional systems.

---

## 8. Open Security Work (Planned)

Planned security workstreams include:

- Independent security review of reattachment logic
- Formal verification of state machine invariants (optional direction)
- Cryptographic audit after hardened implementation phase
- Attack simulations for replay/oscillation/resource abuse

---

## 9. Summary

Jumping VPN’s threat model is built around one central premise:

**Transport volatility is expected.  
Security must survive it without losing session integrity.**

Reattachment safety, replay resistance, bounded adaptation,
and observability are treated as first-class requirements.