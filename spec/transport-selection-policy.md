# Jumping VPN — Transport Selection Policy

Status: Normative Behavioral Policy (Public Preview)

This document defines how candidate transports are evaluated,
ranked, and selected during volatility and recovery phases.

Transport selection MUST be deterministic and bounded.

---

# 1. Purpose

Transport selection governs:

- Which candidate becomes active
- When switching is allowed
- How oscillation is prevented
- How degraded state is entered

Selection logic MUST:

- Be policy-driven
- Be bounded
- Be observable
- Avoid heuristic chaos

---

# 2. Candidate Set Definition

A candidate transport must satisfy:

- Not blacklisted
- Policy-allowed protocol type
- Within acceptable loss/latency bounds
- Not recently rejected within cooldown window

Candidate set MUST be bounded in size.

---

# 3. Transport Health Metrics

Each transport may maintain:

- loss_ratio(window)
- consecutive_drops
- p95_latency_ms(window)
- last_successful_packet_ms
- jitter_estimate (optional)
- stability_duration_ms

Metrics must use bounded sliding windows.

---

# 4. Selection Strategy (Deterministic Model)

Example deterministic selection model:

1. Filter invalid candidates.
2. Remove transports within SWITCH_COOLDOWN_MS.
3. Remove transports exceeding loss threshold.
4. Rank remaining candidates by:

   Primary key:
     lowest loss_ratio

   Secondary key:
     lowest latency

   Tertiary key:
     longest stability_duration

Selection MUST produce a single candidate.

If no candidate passes filters:
→ Remain DEGRADED.

---

# 5. Switch Conditions

Switch MAY occur only if:

- Current state ∈ {VOLATILE, DEGRADED}
- Candidate set non-empty
- switch_rate < MAX_SWITCHES_PER_MIN
- recovery window active

Switch MUST NOT occur from ATTACHED without instability trigger.

---

# 6. Anti-Flapping Controls

To prevent oscillation:

- Enforce SWITCH_COOLDOWN_MS
- Enforce MAX_SWITCHES_PER_MIN
- Apply minimum stability requirement before reusing recently failed transport

Optional:

- Apply hysteresis thresholds
  (e.g., new candidate must outperform current transport by X%)

---

# 7. Hysteresis (Optional but Recommended)

To avoid rapid oscillation:

Define:

SWITCH_IMPROVEMENT_FACTOR

Switch allowed only if:

candidate_score > current_score × SWITCH_IMPROVEMENT_FACTOR

Prevents marginal switching.

---

# 8. Deterministic Tie-Breaking

If multiple candidates equal in score:

Use deterministic ordering:

- Lowest transport_id
OR
- Earliest successful validation timestamp

Never random selection.

Randomness reduces auditability.

---

# 9. Degraded State Entry

If:

- No valid candidate
OR
- Switch denied by policy
OR
- Repeated instability

Then:

Session enters DEGRADED.

DEGRADED is protective,
not failure.

---

# 10. Observability Requirements

Every switch decision MUST log:

{
  previous_transport,
  selected_transport,
  candidate_count,
  loss_ratio,
  latency_estimate,
  reason_code
}

Switch denial MUST log:

{
  reason: switch_rate_limited | cooldown_active | no_valid_candidate
}

---

# 11. Non-Goals

Transport selection does NOT attempt:

- Predict future network conditions
- Perform machine learning
- Guess congestion state
- Override congestion control

It reacts deterministically to bounded metrics.

---

# 12. Design Philosophy

Transport selection is not magic routing.

It is:

- Measurable
- Policy-driven
- Bounded
- Deterministic

Volatility requires structure.
Structure requires constraints.