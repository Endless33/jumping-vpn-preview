# Jumping VPN — Reviewer Guide

Purpose:
This guide is designed to help engineers evaluate the repository quickly and efficiently.

Estimated review time:
10–20 minutes for architectural understanding.

---

# 1. What This Repository Is

This repository is:

- An architectural specification
- A behavioral model
- A deterministic recovery design
- A minimal proof-of-concept

It is NOT:

- A production VPN release
- A hardened cryptographic implementation
- A marketing page

The goal is architectural validation.

---

# 2. Core Claim to Evaluate

The central thesis:

A session can survive transport death
without identity reset
under bounded and deterministic recovery rules.

If this claim holds under defined constraints,
the architecture is successful.

---

# 3. Where to Start (Recommended Order)

### Step 1 — Architecture Overview

Read:

docs/architecture-overview.md

Understand:
- Session vs Transport separation
- Policy-driven adaptation
- Deterministic recovery concept

---

### Step 2 — State Machine

Read:

docs/state-machine.md  
docs/formal-spec-outline.md

Look for:
- Explicit state transitions
- Deterministic outcomes
- Bounded recovery windows
- Absence of silent transitions

---

### Step 3 — Invariants

Read:

docs/invariants.md

Verify:

- Single active transport rule
- No dual-active binding
- SessionID immutability
- Explicit failure boundaries

These invariants define safety.

---

### Step 4 — Threat Model

Read:

docs/threat-model.md

Check:

- On-path attacker assumptions
- Reattach validation logic
- Replay handling boundaries
- Cluster ownership clarity

---

### Step 5 — Reference Architecture

Read:

docs/reference-implementation-outline.md

Evaluate:

- Module separation
- Ownership boundaries
- Policy engine placement
- Observability non-blocking guarantees

---

### Step 6 — Behavioral PoC

Inspect:

poc/real_udp_prototype.py  
poc/README_udp.md

This PoC demonstrates:

- Session creation
- Transport death
- Explicit reattach
- Deterministic continuation

It does NOT demonstrate production crypto.

---

### Step 7 — Test Scenarios

Read:

docs/test-scenarios.md  
docs/benchmark-plan.md

Look for:

- Defined recovery windows
- Anti-flap controls
- Failure isolation
- Reproducible evaluation criteria

---

# 4. Questions Reviewers Often Ask

You may want to evaluate:

- Are state transitions fully explicit?
- Is recovery bounded and policy-defined?
- Is cluster ownership clearly defined?
- Are failure modes deterministic?
- Are invariants enforceable in code?
- Is there ambiguity in transport replacement?

If ambiguity exists, it must be resolved by termination or rejection.

---

# 5. What This Repo Does NOT Yet Include

- Production-grade crypto implementation
- Full client/server hardened stack
- Benchmark numbers from live deployment
- Distributed production cluster
- Performance guarantees at scale

These are implementation phases, not architectural omissions.

---

# 6. Evaluation Criteria

A positive architectural review should confirm:

- Determinism over heuristics
- Explicit invariants
- Bounded adaptation
- Clear failure semantics
- Auditable transitions
- Non-blocking observability

If these hold, the architecture is internally coherent.

---

# 7. Scope Reminder

This repository focuses narrowly on:

Deterministic session continuity under transport volatility.

It does not attempt to solve all networking problems.

---

# 8. Contact

Technical discussions welcome:

riabovasvitalijus@gmail.com

---

Session is the anchor.  
Transport is volatile.  
Recovery must be bounded.