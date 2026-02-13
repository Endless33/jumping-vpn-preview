# Deployment Model — Jumping VPN (Preview)

This document describes how Jumping VPN can be deployed
in real-world environments while preserving
deterministic session continuity.

This is a control-plane deployment model.
Data-plane optimization is out of scope.

---

# 1. Deployment Goals

A production deployment must guarantee:

- Single authoritative session ownership
- Deterministic recovery behavior
- Bounded failover windows
- Explicit rejection under ambiguity
- Horizontal scalability
- Failure isolation

Deployment architecture must not violate invariants.

---

# 2. Core Components

A minimal production deployment includes:

Client Agent
Gateway Node (Edge)
Session Ownership Layer
Policy Engine
Observability Pipeline

Optional:
Load Balancer
Distributed Session Store
Rate Limiting Layer
Monitoring Stack

---

# 3. Deployment Topologies

## 3.1 Single-Node Deployment (Development / Pilot)

Client → Gateway

Characteristics:

- In-memory session store
- No cluster ownership complexity
- Suitable for:
  - Early testing
  - Controlled pilots
  - Architecture validation

Limitations:

- No horizontal scaling
- Single point of failure
- Limited recovery guarantees if node crashes

---

## 3.2 Sticky Routing Cluster (Recommended Early Production)

Client → Load Balancer → Gateway Cluster

Session routing:

SessionID → consistent hash → specific gateway

Properties:

- Session ownership is deterministic
- No shared mutable state required
- Horizontal scaling possible
- High performance
- Low operational complexity

Failure behavior:

If gateway node dies:
Sessions owned by that node must terminate
or
Recover via explicit re-handshake

No silent migration.

---

## 3.3 Shared Atomic Session Store (Advanced Deployment)

Client → Load Balancer → Gateway Cluster
                           ↓
                    Shared Session Store (CAS)

Session store requirements:

- Atomic compare-and-set
- Versioned writes
- Ownership tracking
- TTL enforcement

Properties:

- Reattach can occur across nodes
- Deterministic ownership preserved
- More operational complexity
- Higher latency

Tradeoff:

Scalability vs simplicity.

Consistency preferred over availability.

---

# 4. Session Ownership Rules

At any time:

One and only one gateway is authoritative
for a given SessionID.

Ownership must be:

- Explicit
- Versioned
- Conflict-detectable

If ownership ambiguity is detected:

Reject or terminate.

Never allow dual-active binding.

---

# 5. Load Balancing Considerations

Load balancer must support:

- Consistent hashing
- Session stickiness
- Low-latency routing

Not required:

- Deep packet inspection
- Session introspection

The control-plane must remain gateway-bound.

---

# 6. Horizontal Scaling Strategy

Scale by:

- Increasing gateway instances
- Sharding session ownership
- Isolating per-session mutation

Avoid:

- Global locks
- Shared mutable global state
- Cross-session coupling

Each session must be independently mutable.

---

# 7. Failure Domains

Deployment must isolate:

Gateway failure
Transport failure
Logging failure
Session store failure
Rate limiter overload

Failure in one domain must not corrupt session state in another.

Example:

If logging pipeline fails:
Session continues.
Only telemetry degraded.

---

# 8. Rate Limiting Strategy

Rate limiting may occur at:

Client agent (local)
Gateway (per session)
Gateway (global)
Edge firewall

Rate limits must:

- Be bounded
- Be deterministic
- Fail closed

Flood must not cause uncontrolled switching.

---

# 9. Observability Deployment

Observability must be:

- Asynchronous
- Non-blocking
- Buffered
- Backpressure-aware

Recommended stack:

- Structured logs
- Event stream export
- SIEM integration
- Timeline viewer

Protocol correctness must not depend on observability availability.

---

# 10. High-Volatility Environments

Mobile networks
Cross-border fintech
Edge environments
Satellite links

Deployment requirements:

- Short TTL bounds
- Clear recovery deadlines
- Tight anti-flap constraints
- Explicit degraded state behavior

Deployment must tune policy,
not mutate protocol invariants.

---

# 11. Security Deployment Notes

Production must include:

- Hardened key management
- Secure entropy source
- Replay window enforcement
- Version monotonicity validation
- TLS or equivalent secure channel

Control-plane must fail closed.

Ambiguity must terminate session.

---

# 12. Production Safety Checklist

Before declaring production readiness:

- Reattach under loss tested
- Reattach storm tested
- Cluster ownership validated
- Replay protection validated
- Anti-flap behavior validated
- Partition tolerance evaluated
- Memory leak testing completed

Deployment must prove invariants hold under stress.

---

# 13. What This Model Does Not Claim

This document does NOT define:

- Container orchestration
- Cloud vendor specifics
- Kubernetes configuration
- CI/CD pipelines
- OS-level tuning
- Kernel offload strategies

It defines behavioral safety boundaries only.

---

# 14. Operational Philosophy

Deployment must preserve:

Determinism over convenience.
Consistency over availability.
Explicit failure over silent corruption.

Transport instability is expected.

Identity ambiguity is unacceptable.

---

# Final Principle

Deployment complexity may grow.

Session identity must not.

Session is the anchor.  
Transport is volatile.