# 🧬 Jumping VPN — Session-Anchored Transport Protocol

Jumping VPN is a session-centric protocol architecture designed for environments where transport stability cannot be assumed.

Traditional VPN systems bind identity to transport.

Jumping VPN binds identity to the session.

Transport becomes replaceable.  
Session continuity remains deterministic.

---

# Core Thesis

Modern networks are volatile:

- packet loss spikes
- jitter instability
- NAT rebinding
- mobile network switching
- path degradation
- transport interruption

Jumping VPN explicitly models this volatility instead of assuming stability.

Identity persists.  
Transport changes safely.

---

# Key Property

Jumping VPN implements a:

**session-anchored transport abstraction layer**

This means:

- identity ≠ IP
- identity ≠ socket
- identity = session anchor

Transport becomes a replaceable attachment.

Session continuity survives transport changes.

---

# Demo

This repository includes a deterministic behavioral demo trace and validator.

These artifacts demonstrate that:

- session survives transport degradation
- transport switches explicitly
- identity remains continuous
- no renegotiation occurs
- recovery is deterministic and auditable

## Demo Trace

DEMO_TRACE.jsonl

This file contains an auditable session lifecycle showing:

- SESSION_CREATED
- VOLATILITY_SIGNAL
- TRANSPORT_SWITCH
- STATE_CHANGE
- RECOVERY_COMPLETE

## Demo Validator

demo_engine/replay.py

Validates demo trace correctness.

## How to run

From repository root:

```bash
python demo_engine/replay.py DEMO_TRACE.jsonl

Expected output:

SESSION_CREATED OK
VOLATILITY_SIGNAL OK
TRANSPORT_SWITCH OK
STATE_CHANGE OK
RECOVERY_COMPLETE OK

Trace validated successfully.
Session continuity preserved.

What the Demo Proves
The demo demonstrates the fundamental invariant:
Session identity persists independently of transport attachment.
Transport can degrade, fail, or switch.
Session continuity remains intact.
No identity reset.
No renegotiation.
No silent failure.
Architecture Overview
Jumping VPN defines strict behavioral invariants:
Session identity is stable
Transport is replaceable
State transitions are explicit
Recovery is bounded and deterministic
Replay and injection attempts are rejected
Identity continuity is cryptographically enforced
Core architecture components:

core/
demo_engine/
docs/
spec/
poc/

Behavioral Model
Session lifecycle states:

BIRTH
ATTACHED
VOLATILE
RECOVERING
TERMINATED

Transitions are:
deterministic
reason-coded
auditable
Transport volatility is treated as a modeled condition — not a fatal error.
Security Model (Architectural Level)
Jumping VPN enforces:
session-anchored identity
monotonic authenticated counters
replay rejection
deterministic recovery
no dual-active transport binding
continuity verification
Attack classes mitigated at architectural level:
replay injection
transport hijacking attempts
silent session reset
uncontrolled transport flapping
What This Repository Is
This repository contains:
architectural specification
behavioral demo trace
deterministic replay validator
prototype behavioral model
review-ready engineering artifacts
What This Repository Is NOT
This repository does not yet include:
production cryptographic implementation
kernel-level TUN integration
production deployment tooling
formal verification proof
These are planned future stages.
Intended Audience
This repository is intended for:
protocol engineers
security researchers
infrastructure architects
distributed systems engineers
network protocol designers
Why This Exists
Transport volatility is the default condition of modern networks.
Traditional VPN designs assume transport stability.
Jumping VPN models transport volatility explicitly.
This enables deterministic session continuity.
Demo Trace Link
Direct demo trace:

DEMO_TRACE.jsonl

Validator:

demo_engine/replay.py

Current Status
Current phase:
Architecture validation
Deterministic behavioral demo published
Next phases:
live prototype runtime
cryptographic integration
formal verification
production protocol implementation
Repository Entry Point
Start here:

START_HERE.md

Then review:

docs/
demo_engine/
DEMO_TRACE.jsonl

Final Principle
Session is the anchor.
Transport is volatile.
Identity persists.