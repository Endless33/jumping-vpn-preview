# Jumping VPN — Deployment Model (Public Preview)

Status: Architectural Integration Outline

This document describes how Jumping VPN is intended to be deployed
within real-world infrastructure environments.

This is not a packaging document.
It defines integration architecture.

---

# 1. Deployment Position in Stack

Jumping VPN sits:

Client
↓
Session Control Layer (Jumping VPN)
↓
Transport Layer (UDP / QUIC / TCP)
↓
Network Infrastructure

It does not replace the transport.
It governs session behavior above it.

---

# 2. Client-Side Deployment

Jumping VPN client:

- Maintains session identity
- Monitors transport health
- Executes bounded switching logic
- Emits observability events

Client can operate:

- On end-user device
- On managed enterprise workstation
- On embedded/mobile device
- On infrastructure edge node

---

# 3. Server-Side Deployment

Server component:

- Maintains session table
- Validates reattach proof
- Enforces policy constraints
- Emits state transition logs

Server must be deployed:

- In hardened environment
- Behind firewall policy
- With rate limiting for reattach attempts
- With audit logging enabled

---

# 4. Horizontal Scaling Model

Session control layer supports:

- Stateless transport binding logic
- Session table lookup by SessionID
- Explicit termination policy

Scaling approaches:

- Sticky session routing
- Shared session store (bounded)
- Session-aware load balancing

Cluster consistency must prevent:

- Split-brain session state
- Dual active session binding

---

# 5. Observability Integration

Jumping VPN must export:

- SessionStateChange events
- TransportSwitch events
- TransportSwitchDenied events
- SessionTerminated events

Integration targets:

- SIEM systems
- SOC pipelines
- Centralized logging
- Metrics dashboards

Observability is mandatory in enterprise deployments.

---

# 6. Policy Configuration Layer

Deployment must define:

- Switch thresholds
- Recovery windows
- Session TTL
- Switch rate limits
- Allowed transport classes

Policy may vary by:

- Environment type
- Risk profile
- Regulatory constraints
- Infrastructure quality

---

# 7. Mobile & Edge Environments

Special considerations:

- NAT rebinding frequency
- Variable latency
- Interface switching (WiFi ↔ LTE)
- Carrier-grade NAT

Jumping VPN is optimized for:

- Volatile mobility
- Intermittent degradation
- Cross-border route instability

---

# 8. Failure Domain Isolation

Deployment must ensure:

- Session state corruption does not propagate
- Transport failure in one node does not cascade
- Recovery logic is bounded

Transport volatility is isolated per session.

---

# 9. Upgrade & Versioning Model

Deployment must support:

- Protocol version negotiation
- Backward-compatible session handling
- Graceful migration across minor versions
- Hard termination across incompatible versions

No silent protocol mutation allowed.

---

# 10. Deployment Risks

Operators must consider:

- Misconfigured thresholds
- Excessive switch rate limits
- Insufficient observability
- Inadequate security binding

Incorrect deployment reduces system guarantees.

---

# Final Position

Jumping VPN is not a plug-and-play tunnel.

It is a session control layer
that requires deliberate deployment.

Correct integration ensures:

- Deterministic recovery
- Bounded adaptation
- Transparent observability
- Controlled termination