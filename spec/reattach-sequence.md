# Jumping VPN — Reattach Sequence Specification (Public Preview)

Status: Normative Behavioral Flow (Cryptography Abstracted)

This document defines the logical sequence
for transport reattachment to an existing session.

Cryptographic primitives are abstracted.
Validation semantics are defined.

---

# 1. Preconditions

Reattach may be attempted only if:

- Session state ∈ {VOLATILE, DEGRADED}
- Session NOT in TERMINATED
- Candidate transport available
- Switch rate within policy bounds
- Recovery window active

---

# 2. High-Level Goal

Bind a new transport to an existing session
WITHOUT:

- Full renegotiation
- Identity reset
- Silent state mutation

---

# 3. Reattach Sequence

## Step 1 — Reattach Request (Client → Server)

Client sends:

{
  session_id,
  transport_metadata,
  reattach_proof,
  freshness_marker,
  protocol_version
}

Where:

- session_id identifies existing session
- reattach_proof proves possession of session keys
- freshness_marker prevents replay
- transport_metadata identifies new binding candidate

---

## Step 2 — Server Validation

Server performs:

1. Session lookup by session_id
2. Check session NOT TERMINATED
3. Verify proof-of-possession
4. Verify freshness window
5. Verify policy allows reattach
6. Verify transport not blacklisted

If any check fails:

→ Send ReattachDenied
→ Transition RECOVERING → DEGRADED

---

## Step 3 — Binding Decision

If validation succeeds:

Server:

- Marks candidate transport as pending
- Updates session binding
- Emits TransportSwitch event
- Emits SessionStateChange (RECOVERING → ATTACHED)

Server sends:

{
  reattach_status: SUCCESS,
  binding_confirmation,
  updated_policy_hint (optional)
}

---

## Step 4 — Client Confirmation

Client:

- Confirms binding
- Marks new transport active
- Stops using previous transport

Old transport is retired explicitly.

---

# 4. Failure Conditions

Reattach MUST fail if:

- Proof invalid
- Freshness expired
- Session TTL exceeded
- Transport TTL exceeded
- Switch rate exceeded
- Recovery window expired

No partial binding allowed.

---

# 5. Replay Protection Requirement

Reattach MUST include:

- Unique freshness value
- Time-bound validity
- Nonce or counter enforcement
- Replay window tracking

Replay MUST NOT succeed.

---

# 6. Atomicity Requirement

Reattach MUST be atomic:

- Either new transport becomes active
- Or no state mutation occurs

Partial state is forbidden.

---

# 7. Observability Requirements

Successful reattach MUST emit:

- TransportSwitch
- SessionStateChange
- reason_code: reattach_success

Failed reattach MUST emit:

- TransportSwitchDenied
- SessionStateChange
- reason_code: reattach_validation_failed

---

# 8. State Transition Summary

VOLATILE → RECOVERING → ATTACHED

DEGRADED → RECOVERING → ATTACHED

Failure:

RECOVERING → DEGRADED

Hard failure:

RECOVERING → TERMINATED (if TTL exceeded)

---

# 9. Security Guarantees

Reattach MUST:

- Preserve session identity
- Reject unauthorized binding
- Prevent replay
- Prevent downgrade
- Maintain deterministic state

---

# 10. Non-Goals

Reattach does NOT:

- Perform full key renegotiation
- Recreate session from zero
- Implicitly rotate identity
- Allow silent fallback

---

# Final Position

Reattach is not a reconnect.

It is a bounded transport rebinding
within an existing session identity.

This distinction defines Jumping VPN’s model.