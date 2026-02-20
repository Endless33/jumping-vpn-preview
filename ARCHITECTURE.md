# Jumping VPN — Architecture Overview

Jumping VPN is a session-anchored transport architecture designed to preserve identity continuity under transport volatility.

Traditional VPNs bind identity to transport.

Jumping VPN binds identity to the session.

Transport becomes a replaceable attachment.

---

# Core Architectural Principle

Identity must survive transport failure.

Formally:

identity = session_anchor transport = attachment(session_anchor)

Transport is not the source of identity.

The session is.

---

# Structural Separation

Jumping VPN explicitly separates:

| Layer | Responsibility |
|------|----------------|
| Session Layer | identity continuity, lifecycle |
| Transport Layer | packet delivery |
| Adaptation Layer | path selection, switching logic |
| Audit Layer | invariant enforcement |

This separation prevents transport instability from destroying identity continuity.

---

# Session Anchor Model

The session anchor is the root object.

Properties:

- unique session identifier
- cryptographic binding (planned production phase)
- explicit lifecycle state
- attachment registry
- deterministic state transitions

The session anchor persists independently of transport validity.

---

# Transport Attachment Model

Transport is an attachment object.

Attachment properties:

- path identity (udp:A, udp:B, etc.)
- telemetry metrics (RTT, jitter, loss)
- health score
- attachment state
- attach timestamp

Attachment can be:

- created
- degraded
- replaced
- removed

without terminating the session.

---

# State Machine

Session lifecycle follows explicit deterministic states:

BIRTH ↓ ATTACHED ↓ VOLATILE ↓ REATTACHING ↓ RECOVERING ↓ ATTACHED ↓ TERMINATED

State transitions are:

- explicit
- reason-coded
- auditable
- deterministic

No implicit renegotiation is allowed.

---

# Transport Volatility Model

Transport is assumed unstable by default.

Instability includes:

- packet loss spikes
- RTT spikes
- jitter spikes
- NAT rebinding
- path disappearance

Volatility is modeled as a normal state, not an exception.

Transport volatility does not terminate the session.

---

# Transport Switch Mechanism

Switching is explicit.

Steps:

1. Volatility signal detected
2. Alternative path evaluated
3. Switch executed
4. Recovery state entered
5. Session returns to ATTACHED

Identity remains unchanged.

---

# Deterministic Recovery

Recovery is deterministic.

Recovery properties:

- no identity reset
- no renegotiation required
- no session recreation
- no hidden implicit state

Recovery is modeled as a state transition.

---

# Invariants

Jumping VPN enforces architectural invariants.

Critical invariants include:

### Identity Continuity Invariant

Session identity must never change during transport replacement.

session_id(t0) == session_id(t1)

---

### Single Active Attachment Invariant

At most one active transport attachment exists at any time.

Prevents ambiguity and race conditions.

---

### No Silent Identity Reset Invariant

Identity reset must be explicit termination + recreation.

Implicit reset is forbidden.

---

### Deterministic State Transition Invariant

All state transitions must be explicit and logged.

---

# Observability Model

Jumping VPN is fully observable.

All events are emitted to trace.

Example events:

- SESSION_CREATED
- VOLATILITY_SIGNAL
- TRANSPORT_SWITCH
- STATE_CHANGE
- RECOVERY_COMPLETE

Trace format:

JSONL (line-delimited JSON)

Trace can be replayed and validated deterministically.

---

# Failure Model

Traditional VPN failure model:

transport failure → session failure

Jumping VPN failure model:

transport failure → attachment replacement → session persists

This removes path continuity as a structural dependency.

---

# Demo Trace Proof

Public demo trace:

DEMO_TRACE.jsonl

Validator:

python demo_engine/replay.py DEMO_TRACE.jsonl

This proves:

- session continuity
- explicit volatility detection
- deterministic transport switch
- recovery without identity reset

---

# Architectural Implications

This architecture enables:

- mobility across unstable networks
- deterministic recovery
- auditable transport switching
- transport abstraction layer

Identity becomes transport-independent.

---

# Production Path (Future)

Production implementation layers:

1. Cryptographic session anchor binding
2. UDP / QUIC transport adapters
3. TUN interface integration
4. Multipath attachment pool
5. Production state persistence

Preview repository focuses on architecture and behavioral correctness.

---

# Architectural Summary

Jumping VPN transforms transport from identity anchor into replaceable attachment.

Identity persists.

Transport adapts.

This removes transport continuity as a requirement for session continuity.

This is the foundation of transport-independent session architecture.