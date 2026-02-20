# Jumping VPN — Session State Machine

This document defines the authoritative session lifecycle for Jumping VPN.

The state machine is:

- explicit (no hidden transitions)
- deterministic (same inputs → same outputs)
- auditable (every transition is logged)

Transport volatility is treated as normal input.

Session identity persists across transport changes.

---

# Core Principle

Session identity is anchored above the transport layer.

Transport is an attachment.

A transport can degrade, disappear, or change.

The session persists until explicitly terminated.

---

# State Definitions

## BIRTH
Initial state before the session is created.

Entry:
- no session exists yet

Exit:
- SESSION_CREATED

---

## ATTACHED
Healthy state.

A single active transport attachment exists.
Traffic flows normally.
Continuity is stable.

Entry conditions:
- active attachment exists
- counters are continuous
- no policy violations

Typical events:
- TELEMETRY_TICK
- PATH_SELECTED
- FLOW_CONTROL_UPDATE

---

## VOLATILE
A volatility window is active.

Transport is still attached, but conditions are unstable.

Triggered by:
- loss spike
- jitter spike
- RTT surge
- health degradation
- path score collapse

Meaning:
- do not reset identity
- start bounded adaptation

Typical actions:
- reduce cwnd
- adjust pacing
- rescore candidates
- prepare switch

---

## REATTACHING
A transport switch is in progress.

The protocol is changing attachment without changing session identity.

Entry conditions:
- policy allows switch
- new candidate is selected
- cooldown satisfied

Rules:
- must not create a new session
- must not reset identity
- must preserve continuity

Typical events:
- TRANSPORT_SWITCH
- AUDIT_EVENT (binding validation)

---

## RECOVERING
After switch or stabilization, the protocol enters recovery.

Meaning:
- session is healthy enough to resume growth
- state returns to ATTACHED only after stability window passes

Typical actions:
- gradual cwnd growth
- pacing normalization
- stability confirmation

---

## TERMINATED
Final state.

Session is explicitly ended.

Entry reasons:
- explicit shutdown
- fatal invariant violation
- lifetime expiry (policy)
- unrecoverable error

Rules:
- identity ends
- no further events accepted

---

# Allowed Transitions (Authoritative)

BIRTH        -> ATTACHED      (SESSION_CREATED)
ATTACHED     -> VOLATILE      (VOLATILITY_SIGNAL) ATTACHED     -> TERMINATED    (EXPLICIT_TERMINATION | FATAL)
VOLATILE     -> REATTACHING   (PREFERRED_PATH_CHANGED | TRANSPORT_FAILED) VOLATILE     -> RECOVERING    (STABILITY_WINDOW_MET) VOLATILE     -> TERMINATED    (FATAL)
REATTACHING  -> RECOVERING    (SWITCH_COMPLETE) REATTACHING  -> TERMINATED    (FATAL)
RECOVERING   -> ATTACHED      (RECOVERY_COMPLETE) RECOVERING   -> VOLATILE      (VOLATILITY_SIGNAL) RECOVERING   -> TERMINATED    (FATAL)

No other transitions are valid.

---

# Transition Events (Trace Contract)

Every transition MUST emit at least one of the following:

## SESSION_CREATED
Creates a new session and enters ATTACHED.

Required fields:
- session_id
- state_version

---

## VOLATILITY_SIGNAL
Signals instability.

Required fields:
- reason (LOSS_SPIKE / JITTER_SPIKE / RTT_SURGE / HEALTH_DROP)
- observed metrics (loss, jitter, rtt)

Must transition:
ATTACHED → VOLATILE
or
RECOVERING → VOLATILE

---

## TRANSPORT_SWITCH
Switches active transport attachment.

Required fields:
- from_path
- to_path
- reason

Must occur only when:
- in VOLATILE or REATTACHING
- policy allows switch

---

## STATE_CHANGE
Explicit state transition record.

Required fields:
- from
- to
- reason
- state_version

Must appear for every transition.

---

## RECOVERY_COMPLETE
Signals that recovery ended and ATTACHED is restored.

Required fields:
- stability window proof (implicit)
- state_version

Must transition:
RECOVERING → ATTACHED

---

# Safety Rules

## No Silent State Change
State may only change via explicit events.

## No Identity Reset
Switching transport must not recreate session identity.

## Single Active Attachment
At most one transport is active at any time.

## Deterministic Ordering
Events must be totally ordered by session counter or timestamp.

---

# Example Timeline

This is the canonical behavioral story:

1) Session begins
- SESSION_CREATED
- state: ATTACHED

2) Volatility occurs
- VOLATILITY_SIGNAL (loss spike)
- state: VOLATILE
- cwnd reduces, pacing adjusts

3) Switch happens
- TRANSPORT_SWITCH (udp:A → udp:B)
- state: REATTACHING → RECOVERING

4) Recovery completes
- RECOVERY_COMPLETE
- state: ATTACHED

No renegotiation.
No reset.

---

# Validation

A trace is valid if:

- transitions follow the allowed graph
- invariants remain true
- switch obeys policy
- identity remains stable
- session returns to ATTACHED after recovery

Replay tool validates these conditions:

python demo_engine/replay.py DEMO_TRACE.jsonl

---

# Summary

Jumping VPN defines a deterministic session state machine where:

- volatility is modeled
- switching is explicit
- recovery is bounded
- identity persists

Session is the anchor.
Transport is replaceable.

