# Invariant Test Cases — Jumping VPN (Preview)

Status: Draft  
Purpose: Define formal test cases that validate architectural invariants  

This document specifies deterministic test cases that must pass
for the session lifecycle engine to be considered correct.

These are model-level tests, not cryptographic tests.

---

# 1. Invariant: Single Active Transport

## Definition

At any time:
A session MUST have at most one ACTIVE transport.

---

## Test Case 1.1 — Normal Reattach

Initial:
State = ATTACHED  
Active = transport_A  

Event:
TRANSPORT_DEAD  

Expected:
State → RECOVERING  
Active = None  

Event:
REATTACH_REQUEST (transport_B)

Expected:
State → ATTACHED  
Active = transport_B  

Assertion:
transport_A is not active  
transport_B is active  
Exactly one active transport  

---

## Test Case 1.2 — Dual Reattach Attempt

Initial:
State = RECOVERING  
Active = None  

Two concurrent REATTACH_REQUEST events arrive.

Expected:
Only one accepted.
Second rejected (version mismatch or ownership conflict).

Assertion:
Single active binding.

---

# 2. Invariant: Monotonic State Version

## Definition

state_version MUST increment by +1 on every successful transition.
It MUST NOT decrement.

---

## Test Case 2.1 — Valid Transition

Initial:
state_version = 3  

Event:
TRANSPORT_DEAD  

Expected:
state_version = 4  

---

## Test Case 2.2 — Stale Update

Initial:
state_version = 4  

Incoming REATTACH_REQUEST carries state_version = 3  

Expected:
Rejected.  
state_version remains 4.  

---

# 3. Invariant: No Silent Identity Reset

## Definition

SessionID MUST NOT change during transport reattachment.

---

## Test Case 3.1 — Valid Reattach

Initial:
session_id = X  

Event:
REATTACH_REQUEST  

Expected:
session_id remains X  

---

## Test Case 3.2 — Forced Reset Attempt

Simulate:
Server attempts to issue new session_id during reattach.

Expected:
Rejected as invalid transition.

---

# 4. Invariant: Bounded Recovery Window

## Definition

Recovery MUST complete within max_recovery_window_ms  
OR session MUST terminate.

---

## Test Case 4.1 — Successful Recovery Within Bound

Transport death at t0.  
Reattach at t0 + 500ms.  
Policy bound = 1000ms.

Expected:
Session ATTACHED.  

---

## Test Case 4.2 — Recovery Timeout

Transport death at t0.  
No reattach until t0 + 2000ms.  
Policy bound = 1000ms.

Expected:
State → TERMINATED.  

No silent continuation.

---

# 5. Invariant: Replay Protection

## Definition

Reused nonce MUST be rejected.  
Replay rejection MUST NOT mutate state.

---

## Test Case 5.1 — Valid Nonce

Nonce = 1  

Expected:
Accepted  
state_version increments  

---

## Test Case 5.2 — Replay Nonce

Nonce = 1 reused  

Expected:
Rejected  
state_version unchanged  

---

# 6. Invariant: Deterministic Transitions

## Definition

Given identical:
- state
- message
- policy

Transition MUST be identical.

---

## Test Case 6.1 — Deterministic Behavior

Run same test twice:

Initial:
State = ATTACHED  
Event = TRANSPORT_DEAD  

Expected both runs:
ATTACHED → RECOVERING  
state_version +1  

No randomness allowed.

---

# 7. Invariant: No Infinite Switch Oscillation

## Definition

Switch frequency MUST be bounded.

---

## Test Case 7.1 — Excessive Switches

Trigger:
Rapid sequence of transport death events.

Policy:
MaxSwitchesPerMinute = 5  

Expected:
After limit reached:
State → DEGRADED or TERMINATED  

No further switching.

---

# 8. Invariant: Ownership Authority

## Definition

Only authoritative node may mutate session.

---

## Test Case 8.1 — Split-Brain Simulation

Two nodes attempt reattach simultaneously.

Expected:
One succeeds.
Other rejects due to version conflict.

No dual-active continuation.

---

# 9. Invariant: Explicit Termination

## Definition

Termination MUST be reason-coded.

---

## Test Case 9.1 — TTL Expiry

Session TTL exceeded.

Expected:
State → TERMINATED  
reason_code = SESSION_TTL_EXPIRED  

No implicit drop.

---

# 10. Reviewer Notes

These test cases:

- Validate architectural correctness
- Define mutation boundaries
- Enforce deterministic behavior
- Expose concurrency risks
- Prevent silent corruption

A production build must convert these into:

- Automated test harness
- Fuzz testing inputs
- Concurrency simulation
- Churn stress testing

---

# Final Principle

Invariants are stronger than features.

Features may evolve.
Invariants must not.

Session is the anchor.  
Transport is volatile.  
Correctness is enforced.