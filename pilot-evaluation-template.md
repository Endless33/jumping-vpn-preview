# Jumping VPN — Pilot Evaluation Template (Preview)

This document defines a structured evaluation template for partners
interested in validating deterministic session recovery
under transport instability.

This is not a marketing document.
It is a technical pilot framework.

---

## 1. Pilot Objective

Evaluate whether Jumping VPN:

- Preserves session identity during transport failure
- Performs bounded and auditable recovery
- Avoids silent renegotiation
- Prevents dual-active transport binding
- Terminates deterministically when invariants cannot be preserved

Primary question:

Does session continuity survive transport volatility
under controlled and reproducible conditions?

---

## 2. Environment Description

### 2.1 Network Profile

Provide measurable parameters:

- Packet loss range (%)
- Latency range (ms)
- Jitter range (ms)
- NAT churn frequency
- IP change frequency
- Transport flap rate
- Cross-border routing instability (if applicable)

Example:

Packet loss spikes: 5%–25% bursts  
Latency variance: 30ms–250ms  
NAT rebind interval: 30–120 seconds  

---

### 2.2 Deployment Topology

Specify:

- Single-node or clustered gateway
- Ownership model (sticky vs shared store)
- Transport types tested (UDP/TCP/QUIC)
- Load profile (concurrent sessions)

---

## 3. Test Scenarios

### Scenario A — Transport Death

Trigger:

- Hard socket close
- Forced route drop
- Firewall block

Expected:

- ATTACHED → RECOVERING
- REATTACH_REQUEST
- Deterministic REATTACH_ACK
- RECOVERING → ATTACHED
- No session ID change
- No silent renegotiation

Metrics:

- Recovery time (ms)
- State version increment
- Audit events emitted

---

### Scenario B — Packet Loss Spike

Trigger:

- 20–40% packet loss burst

Expected:

- ATTACHED → VOLATILE or DEGRADED
- No immediate termination
- No uncontrolled switching
- Bounded switch rate

Metrics:

- Switch count per minute
- Time spent in VOLATILE
- No dual-active binding

---

### Scenario C — Replay Attempt

Trigger:

- Reuse old REATTACH_REQUEST nonce

Expected:

- REATTACH_REJECT
- Explicit reason code
- No state mutation
- No transport binding

---

### Scenario D — TTL Expiry

Trigger:

- Exceed TransportLossTtlMs

Expected:

- RECOVERING → TERMINATED
- Explicit reason code
- No silent continuation

---

## 4. Measured Metrics

Minimum required metrics:

- Recovery latency (P50 / P95 / P99)
- Switch frequency
- Recovery success ratio
- Termination rate under volatility
- Replay rejection rate
- State transition correctness

Optional advanced metrics:

- CPU overhead during reattach storms
- Memory per active session
- Anti-replay structure growth
- Version conflict rate

---

## 5. Hard Invariants (Must Hold)

- At most one ACTIVE transport per session
- SessionID remains constant across reattach
- No silent state transitions
- No dual-active binding
- Recovery bounded by policy
- Ambiguity results in rejection or termination

Violation of any invariant = pilot failure.

---

## 6. Evaluation Outcome Categories

### PASS

- All invariants preserved
- Recovery bounded and measurable
- No identity loss during allowed window

### CONDITIONAL

- Recovery succeeds but tuning required
- Policy thresholds require adjustment

### FAIL

- Identity resets silently
- Dual-active binding observed
- Unbounded switching
- Ambiguous ownership allowed

---

## 7. Required Inputs From Partner

To execute pilot meaningfully, partner must provide:

- Reproducible network instability profile
- Clear success criteria
- Environment description
- Session load expectations
- Desired recovery time objective (RTO)

Without defined instability parameters,
results are not meaningful.

---

## 8. Deliverables

Pilot output should include:

- Full state transition logs
- Recovery metrics
- Switch timeline
- Failure reasons (if any)
- Configuration snapshot
- Reproducibility notes

---

## 9. Scope Clarification

This pilot does NOT evaluate:

- Data-plane encryption strength
- Anonymity guarantees
- Censorship bypass
- Endpoint compromise protection

Focus is strictly:

Deterministic session continuity
under transport instability.

---

## 10. Final Principle

If correctness cannot be guaranteed,
the system must terminate explicitly.

Recovery must be bounded.
Transitions must be auditable.
Ambiguity must be rejected.

Session is the anchor.
Transport is volatile.