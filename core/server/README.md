# Server Control-Plane — Reference Architecture (Preview)

This directory contains the server-side control-plane skeleton for Jumping VPN.

It models how a server:

- Owns session identity
- Enforces deterministic state transitions
- Validates reattach requests
- Prevents dual-active transport binding
- Applies TTL and policy constraints
- Preserves safety under volatility

This is a behavioral reference layer — not a full production VPN server.

---

## Architectural Role

The server side is the **authoritative session owner**.

It is responsible for:

- Maintaining session state
- Binding and unbinding transports
- Enforcing invariants
- Rejecting ambiguous continuation
- Emitting auditable transitions

Consistency is preferred over availability.

---

## Main Components

### 1. SessionStore

Authoritative ownership layer.

Responsibilities:

- Store `SessionRecord`
- Enforce session TTL
- Enforce transport-loss TTL
- Perform CAS-style updates (version-safe)
- Prevent state rollback
- Guarantee single active binding

In clustered deployments this must be replaced by:
- Sticky routing (SessionID → node), OR
- Atomic distributed state store with versioned CAS semantics

---

### 2. StateMachine

Deterministic transition engine.

All transitions must:

- Be explicit
- Increment `state_version`
- Be reason-coded
- Preserve invariants

Illegal transitions raise deterministic errors.

No implicit transitions are allowed.

---

### 3. Gateway

Control-plane orchestrator.

Responsibilities:

- Handle session creation
- Process transport death signals
- Validate reattach requests
- Bind new transport
- Enforce TTL
- Reject expired sessions deterministically

Gateway logic ensures:

- No dual-active binding
- No silent identity reset
- No uncontrolled oscillation
- No ambiguous reattachment

---

## Transport Binding Rules

A session may have:

- Multiple candidate transports (conceptually)
- Exactly one ACTIVE transport at a time

Rules:

- Binding is atomic
- Reattach replaces active binding
- Dual-active binding is forbidden
- Binding after TTL expiration is rejected

---

## TTL Semantics

Two independent timers exist:

### Session TTL

Bounds maximum lifetime of a session identity.

If expired:

→ TERMINATED

### Transport-Loss TTL

Bounds how long a session may survive without active transport.

If exceeded:

→ TERMINATED

Recovery must occur within this window.

---

## Deterministic Failure Model

Failures are classified explicitly:

- TRANSPORT_DEAD
- TTL_EXPIRED
- INVALID_STATE_TRANSITION
- REATTACH_REJECTED
- DUAL_ACTIVE_BINDING_ATTEMPT

Ambiguity results in rejection or termination.

Never silent continuation.

---

## Observability Principle

All critical transitions must be:

- reason-coded
- versioned
- auditable

Logging failures must NOT break protocol correctness.

Telemetry is optional.
Determinism is mandatory.

---

## What This Is NOT

This server layer does NOT include:

- Production crypto
- Kernel-level networking
- Data-plane encryption
- High-performance IO loops
- Horizontal scaling logic

It models behavioral correctness only.

---

## Intended Review Focus

Engineers reviewing this layer should evaluate:

- CAS-based state safety
- Version monotonicity
- TTL enforcement boundaries
- Reattach validation boundaries
- Invariant enforcement

The goal is not feature richness.

The goal is safety under volatility.

---

## Design Principle

The server must never guess.

It must decide deterministically
or reject explicitly.

Session is the anchor.
Transport is volatile.