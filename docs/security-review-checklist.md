# Jumping VPN — Security Review Checklist (Public Preview)

Status: Architectural Validation

This document outlines the security assumptions,
attack surfaces, and review checkpoints
for Jumping VPN's session-centric architecture.

This is not a marketing document.
It is a structured review baseline.

---

# 1. Threat Model Assumptions

The system assumes:

- The attacker can observe transport-level traffic.
- The attacker can induce packet loss.
- The attacker can force path degradation.
- The attacker can attempt replay of reattach messages.
- The attacker may attempt session hijacking during volatility.
- NAT mappings may expire unpredictably.

The system does NOT assume:

- Stable IP addresses.
- Honest transport conditions.
- Reliable packet delivery.

---

# 2. Attack Surfaces Introduced by Volatility

Transport volatility increases:

- Reattach attempts
- Identity binding transitions
- Transport rebinding operations

Each transition must be secured.

Review questions:

- Is reattach proof cryptographically bound to session identity?
- Is reattach bound to previous cryptographic context?
- Are replay attempts bounded by nonce/window?
- Is downgrade attack possible during RECOVERING?

---

# 3. Session Integrity Controls

Security reviewers must verify:

- SessionID cannot be guessed or enumerated.
- Reattach requires proof-of-possession of session keys.
- Session fixation is impossible.
- No implicit identity reset occurs during switch.
- Transport binding includes integrity validation.

---

# 4. Replay Protection

Checklist:

- Is there a bounded replay window?
- Are reattach messages nonce-protected?
- Is timestamp validation enforced?
- Can an attacker replay an old successful reattach?

If yes → FAIL.

---

# 5. Transport Hijacking Risk

Scenario:
Attacker observes volatility and injects fake reattach.

Required guarantees:

- Strong cryptographic binding between:
  SessionID
  Identity
  Active keys
- Reattach must fail without valid key material.

Reviewer question:
Can an attacker bind a new transport without session keys?

If yes → FAIL.

---

# 6. Volatility Abuse (Flapping Attack)

Scenario:
Attacker induces artificial loss to force repeated switching.

Required defenses:

- MAX_SWITCHES_PER_MIN
- SWITCH_COOLDOWN_MS
- Degradation state modeling
- Explicit switch denial

Reviewer question:
Can switching be triggered unboundedly?

If yes → FAIL.

---

# 7. Resource Exhaustion

Scenario:
Repeated volatility triggers cause state churn.

Required controls:

- Bounded recovery window
- Candidate transport limit
- Memory bounded by session policy
- Hard TTL on transportless state

Reviewer question:
Can attacker cause unbounded memory growth?

If yes → FAIL.

---

# 8. Session Lifecycle Boundaries

Checklist:

- Is session lifetime bounded?
- Are expired sessions fully invalidated?
- Is state cleaned deterministically?
- Is key rotation tied to session policy?

---

# 9. Observability & Audit

Security requirement:

Every state transition MUST produce:

- timestamp
- session_id
- reason_code
- previous_state
- new_state

Reviewer question:
Can SOC reconstruct a session timeline?

If no → FAIL.

---

# 10. Non-Goals (Security Scope Clarity)

Jumping VPN does NOT attempt to:

- Replace TLS
- Replace application-layer encryption
- Guarantee anonymity by itself
- Replace firewall policy
- Hide traffic volume patterns

Security review must evaluate it strictly
as a behavioral session layer.

---

# 11. Red Team Checklist

Questions a red team should attempt to answer:

- Can we hijack during RECOVERING?
- Can we force silent identity reset?
- Can we bypass switch rate limits?
- Can we replay an old reattach?
- Can we cause split-brain session state?
- Can we cause session to remain ATTACHED when transport is dead?

Any positive answer → design revision required.

---

# Final Statement

Adaptation increases complexity.

Complexity increases attack surface.

Jumping VPN explicitly models both.

Security must validate:

- bounded behavior
- deterministic transitions
- cryptographic binding
- explicit termination

Volatility is not a feature.
It is a liability unless formally constrained.