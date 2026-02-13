# Production Threat Assumptions — Jumping VPN

This document defines the minimum adversarial assumptions
for a production deployment of Jumping VPN.

Security is defined relative to a threat model.
This document makes those assumptions explicit.

---

# 1. On-Path Adversary

Assumption:

An attacker may observe, delay, drop, reorder,
or inject packets on the active transport path.

The attacker:

- Can disrupt transport.
- Can cause packet loss spikes.
- Can trigger transport death.
- Cannot forge valid proof-of-possession (without key compromise).

Design consequence:

Transport disruption is expected.
Session integrity must survive path manipulation.

---

# 2. Off-Path Adversary

Assumption:

An attacker may send unsolicited control-plane messages.

The attacker:

- Does not know valid session keys.
- May attempt replay.
- May attempt reattach flood.
- May guess session IDs.

Design consequence:

Early rejection is mandatory.
Proof-of-possession required.
Replay window enforced.
Rate limiting required.

---

# 3. Replay Attacker

Assumption:

Attacker replays previously valid reattach or handshake messages.

Required protection:

- Monotonic nonce
- Replay window tracking
- Freshness validation
- Deterministic rejection

Replay must not mutate session state.

---

# 4. Session Hijack Attempt

Assumption:

Attacker attempts to bind new transport to existing session.

Required protection:

- Cryptographic binding between session_id and key context
- Freshness validation
- Version check
- Ownership validation

If ambiguity detected → reject.

Never allow dual-active binding.

---

# 5. Cluster Partition Scenario

Assumption:

Cluster network partition causes multiple nodes
to believe they own the same session.

Required behavior:

- Single authoritative ownership
- Atomic state transitions (CAS)
- Reject ambiguous reattach

Consistency > availability.

Split-brain continuation forbidden.

---

# 6. Control-Plane Flooding

Assumption:

Attacker floods reattach or handshake messages.

Required protections:

- Rate limiter
- Stateless rejection of unknown session IDs
- Bounded replay structures
- No heavy computation before validation

Control-plane must fail closed.

---

# 7. Transport Oscillation Induction

Assumption:

Attacker causes intermittent loss
to trigger repeated switching.

Required behavior:

- Hysteresis thresholds
- Switch rate limits
- Cooldown windows
- Degraded mode

No unbounded switching loops.

---

# 8. Resource Exhaustion

Assumption:

High churn in sessions (malicious or organic).

Required properties:

- Bounded per-session memory
- Deterministic TTL eviction
- No append-only state growth
- O(1)-ish session lookup

Exhaustion must not violate invariants.

---

# 9. Logging / Telemetry Failure

Assumption:

SIEM or logging pipeline unavailable.

Required behavior:

- Logging must be non-blocking
- State transitions independent of telemetry
- Session correctness unaffected

Telemetry failure ≠ protocol failure.

---

# 10. Key Compromise (Out of Scope)

If session keys are compromised:

Jumping VPN does NOT:

- Protect against endpoint compromise
- Guarantee secrecy beyond compromised key scope

Recovery requires explicit new handshake.

---

# 11. Non-Goals (Explicit)

Jumping VPN does NOT assume:

- Nation-state censorship bypass
- Metadata hiding guarantees
- Full anonymity
- Endpoint stealth

Scope is limited to:

Deterministic session continuity under transport volatility.

---

# 12. Security Hierarchy

| Layer            | Protection Type             |
|------------------|----------------------------|
| Session Identity | Cryptographic binding       |
| Transport        | Replaceable                |
| Control Plane    | Deterministic + versioned  |
| Cluster          | Consistency-first          |
| Telemetry        | Non-blocking               |

---

# 13. Safety Over Survival

If correctness cannot be guaranteed:

Terminate.

Ambiguous continuation is forbidden.

---

# Final Principle

Threats target volatility.

Jumping VPN models volatility.

Security is preserved not by hiding instability,
but by constraining it.

Session is the anchor.
Transport is volatile.
Correctness is enforced.