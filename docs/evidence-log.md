# Evidence Log — Jumping VPN

This document records observable validation artifacts
for Jumping VPN’s architectural claims.

It is a structured evidence ledger.

No marketing claims.
Only verifiable observations.

---

## Purpose

This log exists to:

- Record reproducible test evidence
- Track behavioral validation progress
- Document failure scenarios and outcomes
- Avoid unverifiable claims

If something is not recorded here,
it is not claimed as validated.

---

## Evidence Categories

Each entry must be classified as one of:

- CONTROL_PLANE_VALIDATION
- TRANSPORT_FAILOVER
- REPLAY_PROTECTION
- RATE_LIMITING
- INVARIANT_ENFORCEMENT
- DEGRADATION_BEHAVIOR
- TERMINATION_CORRECTNESS
- CLUSTER_OWNERSHIP
- BENCHMARK_RUN
- SECURITY_REVIEW

---

## Evidence Entry Template

All entries must follow this format:

Evidence ID: EVT-000X
Category: Date: Implementation Version: Environment: Network Profile: Policy Configuration:
Scenario: Trigger: Expected Behavior: Observed Behavior:
Metrics:
recovery_latency_ms:
switch_count:
invariant_violations:
replay_rejections:
dual_binding_detected:
Result: PASS / FAIL / PARTIAL
Artifacts:
log reference:
commit hash:
reproduction steps:

---

## Evidence Ledger

### Evidence ID: EVT-0001
Category: CONTROL_PLANE_VALIDATION  
Date: TBD  
Implementation Version: preview  
Environment: local UDP prototype  
Network Profile: simulated transport kill  
Policy Configuration: default  

Scenario:
Transport death during active session.

Trigger:
Manual socket closure in `real_udp_prototype.py`.

Expected Behavior:
RECOVERING → REATTACH_REQUEST → ATTACHED  
No identity reset.  
State version increments deterministically.

Observed Behavior:
Session reattached successfully.
No silent reset.
No dual-active binding observed.

Metrics:
- recovery_latency_ms: TBD
- switch_count: 1
- invariant_violations: 0
- replay_rejections: 0
- dual_binding_detected: 0

Result:
PASS (behavioral validation only)

Artifacts:
- poc/real_udp_prototype.py
- event logs (manual review)
- commit hash: TBD

---

### Evidence ID: EVT-0002
Category: REPLAY_PROTECTION  
Date: TBD  
Implementation Version: preview  
Environment: simulated replay injection  
Network Profile: stable  

Scenario:
Duplicate reattach nonce attempt.

Trigger:
Send same nonce twice in REATTACH_REQUEST.

Expected Behavior:
Replay rejected deterministically.
No state mutation.

Observed Behavior:
Replay rejected.
State unchanged.
Logged as security event.

Metrics:
- replay_rejections: 1
- invariant_violations: 0

Result:
PASS (control-plane preview)

Artifacts:
- core/security/anti_replay.py
- simulated test logs

---

## Future Evidence Targets

Planned entries:

- High packet loss spike recovery test
- Anti-flap under oscillating network
- NAT churn recovery validation
- Rate limiter stress test
- Split-brain prevention simulation
- Multi-candidate competition resolution
- 1k session churn benchmark
- 10k session churn benchmark

No claims will be made until evidence entries are logged.

---

## Review Policy

External reviewers are encouraged to:

- Request reproduction steps
- Propose adversarial scenarios
- Suggest invariant stress cases
- Demand log-level evidence

Claims without evidence should be rejected.

---

## Final Principle

Behavioral guarantees must be:

- observable
- reproducible
- measurable
- falsifiable

Architecture is not validated by belief.
It is validated by recorded outcomes.

Session is the anchor.  
Transport is volatile.