# Demo Review Checklist

This checklist helps reviewers validate the demo output against the contract.

---

## Identity & Session

- [ ] SessionID is constant across entire run  
- [ ] No identity reset  
- [ ] No silent renegotiation  
- [ ] No dual-active binding  

---

## State Machine

- [ ] State transitions are explicit  
- [ ] `state_version` is monotonic  
- [ ] `ATTACHED -> VOLATILE -> RECOVERING -> ATTACHED`  
- [ ] No illegal transitions  

---

## Multipath Behavior

- [ ] `MULTIPATH_SCORE_UPDATE` events appear  
- [ ] Candidate ranking changes during volatility  
- [ ] Switch reason is explicit (`PREFERRED_PATH_CHANGED`)  
- [ ] No oscillation outside policy bounds  

---

## Flow Control

- [ ] `FLOW_CONTROL_UPDATE` appears during volatility  
- [ ] cwnd decreases on loss spike  
- [ ] pacing adjusts accordingly  

---

## Telemetry

- [ ] `TELEMETRY_TICK` events appear  
- [ ] RTT/jitter/loss metrics change realistically  
- [ ] Metrics stabilize after recovery  

---

## Transport Switch

- [ ] `TRANSPORT_SWITCH` event exists  
- [ ] `details.from` and `details.to` are valid  
- [ ] Audit events:
  - [ ] `NO_IDENTITY_RESET: PASS`
  - [ ] `NO_DUAL_ACTIVE_BINDING: PASS`

---

## Pass/Fail

PASS if all above conditions are satisfied.  
FAIL if any critical invariant is violated.