# Core Layer — Jumping VPN (Preview)

The `core/` directory contains the behavioral runtime skeleton
for the Jumping VPN session model.

This is not a full VPN implementation.
It is a deterministic orchestration layer that models:

- session lifecycle
- transport volatility
- bounded recovery
- replay protection
- rate limiting
- policy-driven switching

The goal is architectural clarity, not feature completeness.

---

## Structure

core/ ├── client/                 # client-side behavior skeleton ├── server/                 # server-side session ownership model ├── orchestrator/           # runtime coordination logic ├── policy/                 # deterministic decision engine ├── security/               # anti-replay + rate limiting ├── metrics/                # measurable recovery metrics ├── session/                # state machine └── runtime_demo.py         # minimal behavioral demonstration

---

## What This Core Demonstrates

### 1. Deterministic State Transitions
The session state machine supports:

- BIRTH
- ATTACHED
- VOLATILE
- RECOVERING
- DEGRADED
- TERMINATED

All transitions:
- explicit
- reason-coded
- version-monotonic
- bounded by policy

---

### 2. Bounded Recovery

Transport death does NOT imply session death.

Instead:

ATTACHED → RECOVERING → ATTACHED  
(or → TERMINATED if recovery window exceeded)

Recovery is limited by:

- max_recovery_window_ms
- switch cooldown
- anti-flap limits
- replay protection

No infinite loops.
No silent resets.

---

### 3. Replay & Abuse Protection

Control-plane operations require:

- monotonic nonce
- replay window tracking
- rate-limited switching

Invalid attempts are rejected deterministically.

---

### 4. Deterministic Transport Selection

Only one ACTIVE transport is allowed.

Candidates are ranked by:

(priority, loss, rtt, transport_id)

No dual-active ambiguity.
No uncontrolled propagation.

---

## Runtime Demo

See:

core/runtime_demo.py

This script simulates:

- initial active transport
- transport death
- bounded reattach
- replay rejection
- return to ATTACHED

It demonstrates the core thesis:

Session survives transport death
without identity reset
under bounded constraints.

---

## What This Core Is Not

- Not a production VPN
- Not hardened cryptography
- Not a full transport stack
- Not kernel-integrated
- Not optimized for throughput

This is a behavioral architecture preview.

---

## Review Focus

Engineers reviewing this layer should evaluate:

- State determinism
- Version monotonicity
- Failure boundaries
- Replay protection logic
- Switch gating logic
- Single-owner transport invariant

Performance numbers are intentionally not claimed here.

---

Session is the anchor.  
Transport is volatile.  
Correctness is enforced.