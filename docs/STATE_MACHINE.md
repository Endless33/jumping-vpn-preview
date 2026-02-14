# Jumping VPN — State Machine (Formal Preview)

This document defines the **session lifecycle states** and allowed transitions.

Transport behavior is encoded as explicit state transitions.
No implicit behavior is permitted.

---

## States

- **BIRTH**  
  Session created (identity + policy context exists), transport may not be attached yet.

- **ATTACHED**  
  Session has exactly one ACTIVE transport binding.

- **VOLATILE**  
  Transport is still alive, but quality violates policy thresholds (loss/jitter/latency).
  Switching may be considered if bounded by policy.

- **RECOVERING**  
  Active transport is considered dead/unusable.
  The session is attempting to reattach a replacement transport.

- **DEGRADED**  
  Session continues but under constrained mode due to persistent instability.
  Adaptation is limited; stability is prioritized.

- **TERMINATED**  
  Final state. Session is dead. Requires new session establishment.

---

## Transition Table

### BIRTH → ATTACHED
Trigger:
- handshake completed
- initial transport selected and bound

### ATTACHED → VOLATILE
Trigger:
- quality violation signal (loss/jitter/latency over threshold)
Required:
- reason code
- state_version increment

### VOLATILE → ATTACHED
Trigger:
- stability window detected (metrics return within bounds)

### ATTACHED → RECOVERING
Trigger:
- transport death detected (no delivery within bounded window)
Required:
- explicit reason + state_version increment

### RECOVERING → ATTACHED
Trigger:
- REATTACH succeeds (proof-of-possession + freshness validated)
Required:
- explicit transport switch event
- invariant audit events (no dual-active, no identity reset)

### RECOVERING → DEGRADED
Trigger:
- recovery attempts exceed bounded limits but session TTL not expired

### ANY → TERMINATED
Trigger:
- session TTL expired
- transport-loss TTL expired
- policy hard fail
- security violation (invalid proof / replay / ownership ambiguity)

Termination must be explicit and reason-coded.

---

## Required Emitted Events (for observability)

On each transition, the engine must emit:

- STATE_CHANGE(from, to, reason, state_version)
- if switch occurs: TRANSPORT_SWITCH(from_path, to_path, reason)
- if security: SECURITY_EVENT(reason)
- if invariants checked: AUDIT_EVENT(check, result)

---

Session is the anchor. Transport is volatile.