# Formal Verification Plan (Preview)

Status: Architectural Planning  
Scope: Behavioral correctness of session lifecycle and recovery logic  
Non-goal: Formal proof of cryptographic primitives  

This document outlines how Jumping VPN’s behavioral model
could be formally verified.

The focus is deterministic session continuity under transport volatility.

---

# 1. Verification Objectives

We aim to formally reason about:

- State transition correctness
- Invariant preservation
- Absence of dual-active transport binding
- Deterministic recovery behavior
- Absence of silent identity reset
- Version monotonicity enforcement
- Bounded recovery guarantees

This plan targets control-plane correctness.

---

# 2. Core Properties to Verify

## 2.1 Safety Properties

Must ALWAYS hold:

1. At most one active transport per session.
2. Session identity never changes during reattach.
3. No state transition occurs without explicit reason code.
4. state_version is strictly monotonic.
5. Dual-active binding is impossible.
6. Reattach cannot succeed with stale version.
7. Replay does not mutate session state.

Formal category: Safety invariants.

---

## 2.2 Liveness Properties

Must EVENTUALLY hold (under valid conditions):

1. If a valid reattach request is received within TTL,
   session returns to ATTACHED.
2. If volatility stabilizes within recovery window,
   system leaves RECOVERING.
3. If recovery window expires,
   session transitions to TERMINATED.

Formal category: Bounded liveness.

---

# 3. Candidate Formal Methods

## 3.1 TLA+ (Recommended Starting Point)

Why:

- Strong support for state machines
- Good for concurrency modeling
- Good for invariant checking
- Widely used in distributed systems verification

Model targets:

- Session state machine
- state_version increment logic
- Reattach logic
- Replay rejection
- CAS-based session store

---

## 3.2 Ivy / Dafny / Coq (Advanced)

Potential future options:

- Machine-checked invariants
- Proof of no dual-active binding
- Formal proof of version monotonicity

Not required for preview stage.

---

# 4. Model Scope Definition

The formal model must include:

- Session states
- Transport states
- Reattach events
- TTL expiry
- Replay attempts
- Concurrent reattach attempts
- Cluster ownership ambiguity

The model must exclude:

- Packet encryption
- Framing details
- Network timing simulation
- Kernel interactions

---

# 5. State Model Formalization Target

State variables:

- session_state
- state_version
- active_transport
- recovery_deadline
- replay_window
- ownership_node
- ttl_expiry

Transitions:

- HANDSHAKE
- TRANSPORT_DEAD
- REATTACH_REQUEST
- REATTACH_ACCEPT
- REATTACH_REJECT
- TTL_EXPIRE
- TERMINATE

Every transition must be:

- Explicit
- Versioned
- Guarded by invariants

---

# 6. Key Invariants to Encode

Invariant 1:
active_transport_count <= 1

Invariant 2:
state_version strictly increases

Invariant 3:
If state == ATTACHED → active_transport exists

Invariant 4:
If state == TERMINATED → no future transitions allowed

Invariant 5:
If replay_detected → state_version unchanged

Invariant 6:
Ownership must be unique per session

---

# 7. Failure Scenarios to Model

1. Concurrent reattach attempts
2. Stale reattach with old state_version
3. Replay nonce reuse
4. TTL expiration during reattach
5. Node ownership conflict
6. Rapid churn causing flap attempts

Model must prove:

- No invariant violation
- Deterministic rejection on ambiguity
- No silent fallback paths

---

# 8. Determinism Guarantee

For identical inputs and policy configuration,
the state machine must produce identical outputs.

This includes:

- Same transition path
- Same reason_code
- Same state_version increments

Formal verification should assert determinism under:

- Ordered event streams
- Concurrent attempts with ordering rules

---

# 9. Verification Milestones

Stage 1:
TLA+ state machine model
- Encode states
- Encode invariants
- Model reattach
- Model TTL
- Model replay window

Stage 2:
Model concurrent reattach attempts

Stage 3:
Model distributed ownership logic

Stage 4:
Stress invariant testing with adversarial sequences

---

# 10. Expected Outcomes

Formal verification should prove:

- No dual-active binding possible
- No silent identity reset
- No version rollback
- Deterministic rejection paths
- Bounded recovery enforcement

It should NOT attempt:

- Cryptographic proof
- Network simulation
- Real-world performance modeling

---

# 11. Why Formal Verification Matters

The core claim of Jumping VPN is behavioral determinism.

Without formal reasoning,
the guarantees risk being narrative rather than structural.

Formal modeling converts:

"architectural intention"
into
"provable state correctness".

---

# 12. Status

Formal verification has not yet been implemented.

This document defines the roadmap for doing so.

---

Session is the anchor.  
Transport is volatile.  
Correctness must be provable.