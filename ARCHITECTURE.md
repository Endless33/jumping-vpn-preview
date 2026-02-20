# Jumping VPN — Architecture (Preview)

This document is the **single architectural map** of the Jumping VPN preview repository.

It is written for engineers reviewing:
- session continuity claims
- deterministic recovery semantics
- transport volatility model
- safety / rejection rules

This is **not** production cryptography.
This is a **behavior-first protocol architecture**.

---

## 1) What this system is

Jumping VPN explores a transport architecture where:

> **Session identity persists above transport attachments.**  
> Transport is volatile. Session is the anchor.

Traditional VPNs often bind continuity to a single socket/path.
Jumping VPN binds continuity to a **session anchor**, and treats paths as replaceable carriers.

---

## 2) Core architectural invariant

### Path Independence Principle

**Session existence must not depend on path continuity.**

Transport can:
- degrade
- switch
- disappear

The session must:
- remain valid (within policy/TTL)
- preserve continuity state
- accept only verifiable reattachments
- never silently reset identity

---

## 3) Entities

### 3.1 Session Anchor (Identity Layer)

A **Session** owns:
- stable `session_id`
- monotonic continuity counter state
- state machine + versioning
- policy/TTL
- replay window

The session anchor is the source of truth.

### 3.2 Transport Attachment (Carrier Layer)

A **Transport Attachment** is a temporary binding:
- UDP path A / UDP path B
- TCP path (optional)
- any replaceable path candidate

Attachments are always:
- validated
- continuity-checked
- auditable
- single-active (no dual-active identity)

Transport is disposable. Session is not.

---

## 4) Continuity model (security + correctness)

### 4.1 Replay / injection protection (architectural model)

Each frame/event is expected to carry:
- **session-scoped monotonic counter**
- authentication binding to session identity (AEAD/MAC in next milestone)

Receiver acceptance rule:
- counters must progress within a **bounded sliding window**
- duplicates are rejected
- stale/out-of-window counters are rejected
- invalid authentication is rejected **before** any state mutation

### 4.2 Key schedule (next milestone)
Keys must be:
- derived from a session root secret
- advanced forward-only
- old keys rejected after rotation

Transport switch must not reset identity or key schedule.

### 4.3 Zombie / stale attachment rejection
If a second attachment appears:
- it must prove continuity (counter + binding)
- otherwise it is rejected as stale/zombie

---

## 5) State machine model

Jumping VPN models volatility explicitly.

Common states in this preview repo:

- `BIRTH`
- `ATTACHED`
- `VOLATILE`
- `RECOVERING`
- `TERMINATED`

State transitions must be:
- explicit
- reason-coded
- monotonic-versioned
- logged (auditable)

No silent downgrade.
No identity reset without TERMINATE.

---

## 6) Deterministic recovery semantics

When the current transport becomes unhealthy:

1) system emits a volatility signal
2) enters a volatility state (`VOLATILE`)
3) applies bounded adaptation (cwnd/pacing changes)
4) selects a better path candidate
5) performs explicit transport switch
6) enters recovery window
7) returns to `ATTACHED` if stability criteria is met

The output is a deterministic trace that reviewers can replay.

---

## 7) What “done” means in the preview repo

This repository is considered successful if it provides:

- a clear architecture contract (this document)
- a deterministic trace format
- a validator/replay engine
- a scenario showing:
  loss spike → adaptation → transport switch → recovery → still ATTACHED

It does **not** claim:
- production crypto
- TUN integration
- production hardening
- censorship bypass / anonymity

---

## 8) Where to look in this repo

Start points (typical):

- `README.md` — entry point
- `ARCHITECTURE.md` — this map
- `DEMO_TRACE.jsonl` — example trace
- `demo_engine/replay.py` — validator
- `docs/` — invariants, state machine, demo package

---

## 9) Final principle

Transport instability is normal.

Jumping VPN is built around the idea that:

> **Volatility is a state. Not a failure.**  
> **Session is the anchor. Transport is volatile.**