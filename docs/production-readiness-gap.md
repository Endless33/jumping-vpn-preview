# Production Readiness Gap — Jumping VPN (Preview)

This document explicitly outlines what is missing
between the current architectural preview
and a production-ready deployment.

The goal is transparency.

---

# 1. Current Stage

Current repository status:

- Formal architectural model defined
- Explicit state machine documented
- Deterministic invariants specified
- Threat model articulated
- Minimal UDP behavioral PoC implemented
- Evaluation framework defined

This is architectural validation stage.

---

# 2. What Is NOT Yet Production-Ready

## 2.1 Cryptographic Hardening

Missing:

- Production-grade key exchange
- Formalized cipher suite selection
- Key rotation implementation
- Secure handshake state machine
- Independent cryptographic review

Current PoC is behavioral only.

---

## 2.2 Production Control Plane

Missing:

- Hardened message framing
- Input validation layer
- Abuse rate-limiting enforcement
- Control-plane DoS mitigation
- Production logging integration

---

## 2.3 Cluster Deployment Model

Missing:

- Distributed session ownership implementation
- Authoritative state synchronization layer
- Split-brain protection in real cluster
- CAS-backed session store
- Failover testing in multi-node topology

---

## 2.4 Performance & Scaling

Missing:

- High concurrency benchmark results (10k+ sessions)
- Memory profiling under churn
- CPU cost of frequent reattach cycles
- Replay window scaling tests
- Backpressure behavior under stress

A benchmark plan exists — results do not yet.

---

## 2.5 Transport Adapters

Missing:

- QUIC transport implementation
- TCP fallback transport
- Multipath candidate selection logic
- Real-world NAT traversal optimization

---

## 2.6 Observability Integration

Missing:

- Structured export to SIEM
- Prometheus metrics
- Production tracing integration
- Alert policy definition

Current model defines events — integration layer not implemented.

---

## 2.7 Security Review

Missing:

- Third-party code audit
- Formal security review
- Penetration testing
- Control-plane abuse simulation at scale

---

# 3. Engineering Milestones Required for Production

To reach production-grade status:

1. Hardened cryptographic layer
2. Authoritative cluster ownership model
3. Benchmark validation under reproducible volatility
4. Abuse & DoS protection layer
5. Observability integration
6. Independent security audit

Only after these are complete
can production claims be responsibly made.

---

# 4. What Is Already Structurally Sound

The following are architecturally stable:

- Deterministic state machine
- Explicit invariants
- Bounded recovery semantics
- No silent identity reset
- No dual-active transport binding
- Policy-driven adaptation
- Explicit failure states

The architecture itself is coherent.
The implementation depth is incomplete.

---

# 5. Why This Document Exists

This repository does not claim production readiness.

It claims:

- Architectural clarity
- Deterministic recovery modeling
- Explicit engineering boundaries

Transparent gap documentation
increases technical trust.

---

# 6. Honest Positioning

Jumping VPN is currently:

Architecturally mature.  
Implementation incomplete.  
Production not yet achieved.

---

Session is the anchor.  
Transport is volatile.  
Production requires discipline.