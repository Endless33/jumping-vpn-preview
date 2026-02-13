# Security Review Checklist — Jumping VPN (Preview)

This document defines the internal security review framework
for validating Jumping VPN's behavioral guarantees.

This is not a marketing artifact.
It is an engineering checklist.

---

# 1. State Machine Validation

☐ All transitions are deterministic  
☐ No implicit state changes  
☐ TERMINATED is absorbing  
☐ Recovery windows are bounded  
☐ No unbounded retry loops  

---

# 2. Identity Binding Review

☐ SessionID is cryptographically bound  
☐ Reattach requires proof-of-possession  
☐ No session fixation vectors  
☐ Identity cannot be reset silently  
☐ Session TTL enforced  

---

# 3. Transport Switching Controls

☐ MaxSwitchesPerMinute enforced  
☐ Cooldown windows implemented  
☐ Hysteresis for volatility detection  
☐ Switch decisions are reason-coded  
☐ No dual-active transport binding  

---

# 4. Replay Protection

☐ Reattach messages include freshness markers  
☐ Replay window is bounded  
☐ Duplicate reattach rejected deterministically  
☐ Replay attempts logged  

---

# 5. Cluster Consistency

☐ Authoritative ownership model defined  
☐ CAS-based atomic update model  
☐ Split-brain rejection behavior tested  
☐ No ambiguous continuation allowed  
☐ Consistency preferred over availability  

---

# 6. Session Table Hardening

☐ Per-session resource bounds  
☐ TTL-based eviction  
☐ Rate limits per identity  
☐ No unbounded memory growth  

---

# 7. Observability Safety

☐ All state transitions emit events  
☐ Audit events are explicit  
☐ Logging failure does not affect protocol correctness  
☐ Telemetry cannot mutate state  

---

# 8. Failure Handling

☐ Transport death handled deterministically  
☐ Policy-limit exceedance handled explicitly  
☐ Security violation triggers termination  
☐ No undefined “zombie” sessions  

---

# 9. Benchmark Validation

☐ RecoveryLatencyMs measured  
☐ SwitchRate measured  
☐ SessionResetCount validated = 0 under bounded volatility  
☐ DualBindingIncidents validated = 0  

---

# 10. Explicit Non-Goals Confirmed

☐ No anonymity guarantees claimed  
☐ No censorship bypass guarantees claimed  
☐ No endpoint security claims made  
☐ Scope limited to transport volatility modeling  

---

# Review Philosophy

If a property cannot be:

- Measured
- Bounded
- Logged
- Audited

It is not considered secure.

---

Security is not a feature.
It is constrained, deterministic behavior under pressure.