# Jumping VPN — Baseline Results Template (Public Preview)

This template is used to publish real benchmark results once available.
No numbers are claimed here.

---

## Run Metadata

- Run ID:
- Date (UTC):
- Scenario:
- Policy Version:
- Platform / OS:
- Notes:

---

## Network Profile

| Parameter | Value |
|----------|-------|
| Packet Loss (%) | |
| Latency (ms) | |
| Jitter (ms) | |
| NAT Rebind | yes/no |
| Interface Switch | yes/no |

---

## Observed Timeline (Key Events)

| Timestamp (ms) | Event | Notes |
|---:|---|---|
| | TransportDead | |
| | SessionStateChange (ATTACHED→VOLATILE) | |
| | TransportSwitch / SwitchDenied | |
| | ReattachAttempt | |
| | ReattachResult | |
| | SessionStateChange (RECOVERING→ATTACHED) | |

---

## Summary Metrics (Fill With Real Data)

| Metric | Value |
|---|---:|
| Time to detect instability (ms) | |
| Time to switch (ms) | |
| Time to reattach (ms) | |
| Switches total | |
| Switch denials total | |
| Replay detected | |
| End state | |

---

## Pass/Fail Criteria

- [ ] No silent session reset occurred
- [ ] No identity reset occurred
- [ ] No dual-active binding observed
- [ ] Switch rate limits enforced (if applicable)
- [ ] Recovery window enforced (if applicable)
- [ ] All state transitions emitted structured events

---

## Notes / Anomalies

-