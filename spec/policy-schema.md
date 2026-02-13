# Jumping VPN — Policy Schema

Status: Normative Configuration Model (Public Preview)

This document defines the structure,
constraints, and semantics of Jumping VPN policy configuration.

Policy controls behavioral limits.
Behavior must remain bounded by policy.

---

# 1. Policy Object (Logical YAML Model)

Example:

version: "1.0"

session:
  max_lifetime_ms: 28800000
  transport_lost_ttl_ms: 15000

volatility:
  heartbeat_interval_ms: 500
  heartbeat_volatile_ms: 2000
  loss_window_ms: 2000
  loss_volatile_threshold: 0.20
  max_consecutive_drops: 3
  volatile_to_degraded_ms: 4000

switching:
  max_switches_per_min: 8
  switch_cooldown_ms: 1500
  recovery_window_ms: 8000
  switch_improvement_factor: 1.10

transport:
  allowed_protocols:
    - udp
    - quic
  max_candidate_count: 3
  enforce_hysteresis: true

security:
  reattach_proof_max_age_ms: 5000
  replay_window_size: 128
  strict_validation: true

observability:
  emit_switch_metrics: true
  emit_security_events: true
  include_latency_metrics: true

---

# 2. Schema Constraints

## 2.1 Numeric Bounds

All time values:

- MUST be positive integers
- MUST not exceed system-defined upper limits
- MUST be validated before runtime

Example constraints:

- max_switches_per_min ≥ 0
- loss_volatile_threshold ∈ (0,1]
- max_candidate_count ≥ 1

---

## 2.2 Mandatory Fields

The following fields are REQUIRED:

- session.max_lifetime_ms
- session.transport_lost_ttl_ms
- switching.max_switches_per_min
- switching.recovery_window_ms
- volatility.loss_volatile_threshold
- security.reattach_proof_max_age_ms

If missing → policy invalid.

---

# 3. Policy Versioning

Each policy MUST include:

version: "X.Y"

Policy changes MUST:

- Be logged
- Be applied atomically
- Not retroactively mutate active session history

Optional:

- Graceful policy migration window

---

# 4. Policy Enforcement Semantics

Policy MUST be enforced at:

- Session creation
- Volatility detection
- Switch decision
- Reattach validation
- Termination evaluation

Policy must not be bypassable.

---

# 5. Invalid Policy Handling

If policy fails validation:

- Session creation MUST be denied
- Existing sessions MAY continue under previous valid policy
- Error must be logged

---

# 6. Runtime Policy Changes

If policy updated during active session:

Options:

- Strict Mode:
  Immediately apply new bounds
- Grace Mode:
  Apply at next state transition

Policy behavior must be deterministic.

---

# 7. Safety Guarantees

Policy MUST prevent:

- Infinite recovery loops
- Unlimited switching
- Infinite session lifetime
- Zero replay protection

Policy cannot disable core invariants.

---

# 8. Non-Goals

Policy schema does NOT:

- Define cryptographic primitives
- Replace system-level configuration
- Define deployment topology
- Guarantee optimal thresholds

It defines behavioral boundaries.

---

# 9. Design Principle

Policy defines the limits of adaptation.

Without policy,
volatility becomes chaos.

With bounded policy,
volatility becomes manageable.