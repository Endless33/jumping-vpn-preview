# Jumping VPN — Production Core (Reference Skeleton)

This directory contains the production-oriented control-plane skeleton
for Jumping VPN.

It defines the behavioral core responsible for:

- Session identity ownership
- Deterministic state transitions
- Transport binding and replacement
- Bounded recovery under volatility
- Version-safe mutation logic
- Explicit invariant enforcement

This is not a complete VPN implementation.
It is a behavioral core architecture preview.

---

# Core Philosophy

Jumping VPN is defined by behavior over time.

The core enforces one primary contract:

- Session is the identity anchor
- Transport is replaceable
- Recovery is bounded
- Ambiguity is rejected

The system must prefer deterministic failure
over silent inconsistency.

---

# Directory Structure

core/ ├── common/ │   ├── models.py │   ├── reason_codes.py │   ├── errors.py │   └── invariants.py ├── session/ │   └── state_machine.py ├── server/ │   ├── session_store.py │   ├── gateway.py │   └── README.md ├── client/ │   ├── agent.py │   └── README.md └── README.md

---

# Layer Responsibilities

## 1. common/

Shared primitives:

- Session models
- Enumerated state definitions
- Reason codes
- Deterministic error classes
- Invariant enforcement functions

These are the system's formal vocabulary.

---

## 2. session/

State machine layer.

Defines:

- Legal transitions
- State version increments
- Deterministic transition enforcement
- Illegal transition rejection

All state mutation must pass through this layer.

---

## 3. server/

Authoritative control-plane ownership.

Includes:

- SessionStore (CAS + TTL)
- Gateway (control-plane orchestration)

Server responsibilities:

- Bind / unbind transport
- Enforce single active binding
- Validate reattach
- Enforce TTL bounds
- Reject ambiguous continuation

---

## 4. client/

Client-side control-plane skeleton.

Responsibilities:

- Maintain session context
- Detect transport volatility
- Initiate reattach
- Enforce local cooldown and anti-flap bounds

Client never silently resets identity.

---

# Core Guarantees (Target Invariants)

The system aims to enforce:

- No dual-active transport binding
- No silent session reset
- No implicit state transition
- No version rollback
- No unbounded switching
- No ambiguous ownership

If any invariant cannot be satisfied:

→ reject or terminate explicitly.

---

# What This Core Does NOT Contain

This directory does NOT include:

- Production-grade cryptography
- Data-plane encryption
- Kernel networking
- QUIC/TCP/UDP implementations
- Performance optimizations
- Horizontal scaling logic
- Persistent distributed store

This is a behavioral core reference.

---

# Why This Exists

Before performance.
Before scaling.
Before optimization.

Behavior must be correct.

A volatile network is not an edge case.
It is the default.

This core models:

- Volatility as state
- Recovery as bounded
- Identity as stable
- Transport as ephemeral

---

# Review Focus

Engineers reviewing this layer should assess:

- Transition safety
- Version monotonicity
- CAS correctness
- TTL enforcement logic
- Deterministic rejection paths
- Safety under concurrent mutation attempts

The core must remain small, explicit, and testable.

---

# Design Rule

If behavior cannot be explained deterministically,
it must not exist in the system.

Session remains the anchor.
Transport is volatile.