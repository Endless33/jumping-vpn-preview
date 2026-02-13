# Why Jumping VPN Cannot Be Implemented as a Simple Plugin

Status: Draft  
Audience: Engineers evaluating integration approaches  

This document explains why Jumping VPN’s behavioral model
cannot be safely implemented as a thin wrapper, middleware plugin,
or superficial transport extension.

---

# 1. The Core Issue

Jumping VPN is not:

- A routing tweak
- A retry wrapper
- A transport abstraction layer
- A connection migration helper

It is a **session-level behavioral model**.

The session lifecycle must be authoritative.

---

# 2. Plugin-Level Limitations

A plugin typically:

- Hooks into transport events
- Reacts to disconnect
- Attempts reconnect
- Maintains minimal metadata

This is insufficient because:

- Session ownership must be versioned
- State transitions must be atomic
- Replay windows must be enforced
- Switch bounds must be deterministic
- Dual-active prevention must be guaranteed

These cannot be reliably enforced in a loosely coupled wrapper.

---

# 3. State Authority Problem

A plugin does not control:

- The authoritative session store
- Cross-node ownership arbitration
- Version conflict resolution
- CAS semantics

Without authority, a plugin risks:

- Ambiguous reattach
- Dual-active binding
- Silent rollback
- Race conditions

The invariants require architectural ownership.

---

# 4. Determinism Constraint

Jumping VPN requires:

Given identical:
- state
- input
- policy

The system produces identical transitions.

Plugins often introduce:

- Implicit retries
- Transport-driven heuristics
- Non-deterministic fallback logic

This violates deterministic guarantees.

---

# 5. Multi-Node Deployment

In clustered environments:

Session ownership MUST be:

- authoritative
- atomic
- version-validated

A plugin layered on top of existing VPN logic:

- Cannot prevent split-brain
- Cannot guarantee CAS semantics
- Cannot enforce monotonic state_version

Correctness must be core-level.

---

# 6. Anti-Replay Enforcement

Replay protection requires:

- Monotonic nonce tracking
- Window bounding
- Version-aware rejection
- Atomic state mutation

This cannot be reliably implemented
if the plugin does not control the session store.

---

# 7. Bounded Recovery Semantics

Recovery windows must be:

- measurable
- policy-enforced
- state-bound
- auditable

Plugins often rely on:

- transport callbacks
- timer-based retries
- implicit reconnection loops

This creates:

Unbounded switching  
Non-deterministic escalation  
Silent renegotiation  

Jumping VPN forbids these behaviors.

---

# 8. Observability as Contract

Jumping VPN treats audit events as:

Part of correctness.

State transitions MUST emit reason-coded events.

A plugin may:

- Log inconsistently
- Miss race conditions
- Fail to record ownership conflicts

Core-level integration ensures correctness first,
logging second.

---

# 9. Invariant Enforcement Layer

Hard invariants include:

- Single active transport
- No silent identity reset
- Monotonic state version
- Bounded switch rate
- Deterministic termination

These must be enforced at:

State mutation boundary.

Not after-the-fact.

---

# 10. Why This Requires Architectural Ownership

Jumping VPN is:

A session lifecycle engine.

It defines:

- State authority
- Transition rules
- Recovery boundaries
- Ownership model

These must exist at the core,
not as an extension.

---

# 11. What Can Be Modular

While the behavioral engine must be core-level,
certain components can be modular:

- Transport adapters (UDP/TCP/QUIC)
- Observability exporters
- Policy configuration
- Benchmark harness

The lifecycle engine itself cannot be reduced
to a plugin without violating invariants.

---

# 12. Engineering Conclusion

Jumping VPN is:

Not a patch.
Not a wrapper.
Not a migration helper.

It is a deterministic session-state machine
with transport volatility modeling.

To preserve invariants,
it must own:

- Session lifecycle
- Version control
- Ownership arbitration
- Recovery enforcement

Plugins cannot guarantee these properties.

---

# Final Principle

If determinism is optional,
a plugin is sufficient.

If determinism is required,
architecture must own the lifecycle.

Session is the anchor.  
Transport is volatile.  
Correctness is architectural.