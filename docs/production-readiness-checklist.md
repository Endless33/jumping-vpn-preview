# Production Readiness Checklist — Jumping VPN (Preview)

This document defines what must be true
before Jumping VPN can be considered production-ready.

This repository does NOT claim production readiness.
This is a structured checklist for future evaluation.

---

## 1) Protocol Correctness

- [ ] All state transitions are deterministic and reason-coded
- [ ] No dual-active transport binding is possible
- [ ] No silent session reset under transport volatility
- [ ] SessionID continuity preserved across reattach
- [ ] Versioned state mutations prevent rollback
- [ ] Explicit failure outcomes for all policy boundaries

---

## 2) Security Guarantees

- [ ] Proof-of-possession required for reattach
- [ ] Anti-replay window implemented and bounded
- [ ] Freshness validation enforced
- [ ] Control-plane rate limiting in place
- [ ] Ownership conflict handling deterministic
- [ ] Fail-closed behavior under ambiguity

---

## 3) Control-Plane Stability

- [ ] Reattach validation time bounded
- [ ] No unbounded memory growth per session
- [ ] Session TTL enforced
- [ ] TransportLossTTL enforced
- [ ] Recovery window bounded and measurable
- [ ] Switch rate limits enforced

---

## 4) Observability

- [ ] Every state transition produces an event
- [ ] Reason codes stable and documented
- [ ] Recovery timeline reconstructable from logs
- [ ] Observability failures do not break correctness
- [ ] Security events separated from telemetry noise

---

## 5) Scalability

- [ ] Session table lookup remains bounded (target O(1)-ish)
- [ ] Memory per session measured
- [ ] CPU usage per 1k sessions measured
- [ ] No per-packet heavy control-plane operations
- [ ] No unbounded candidate transport sets

---

## 6) Cluster Safety (If Distributed)

- [ ] Single authoritative session ownership
- [ ] Atomic reattach update (CAS/transactional)
- [ ] No split-brain dual-active identity
- [ ] Clear conflict resolution strategy
- [ ] Explicit denial on ambiguous authority

---

## 7) Failure Handling

- [ ] Transport death handled without implicit reset
- [ ] Degraded mode clearly defined
- [ ] Explicit termination when bounds exceeded
- [ ] No infinite reattach loops
- [ ] Policy cooldown enforced after switch

---

## 8) Benchmark Validation

- [ ] Recovery latency measured
- [ ] Switch frequency histogram captured
- [ ] Degraded entry rate measured
- [ ] Termination rate measured
- [ ] Resource usage documented
- [ ] Test conditions disclosed with results

---

## 9) Operational Safety

- [ ] Configuration validation at startup
- [ ] Safe defaults for policy bounds
- [ ] Explicit versioning of schema and reason codes
- [ ] Upgrade path defined
- [ ] Backward compatibility strategy documented

---

## 10) Explicit Non-Production Disclaimer (Until Complete)

Until all above items are verified:

- This is architectural validation
- Not a production release
- Not a hardened cryptographic stack
- Not a commercial VPN product

---

Production readiness is a measurable state —
not a marketing statement.

Session is the anchor.  
Transport is volatile.