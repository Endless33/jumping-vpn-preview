# Jumping VPN — Scope & Responsibility Model

Status: Architectural Boundary Definition

This document defines the responsibility boundaries
between Jumping VPN and the surrounding infrastructure.

Clear ownership of responsibility reduces ambiguity,
risk, and unrealistic expectations.

---

# 1. Core Responsibility of Jumping VPN

Jumping VPN is responsible for:

- Session lifecycle management
- Transport volatility detection
- Bounded transport switching
- Deterministic recovery logic
- Explicit degradation modeling
- State transition logging
- Policy-bounded adaptation

It defines behavioral continuity under unstable transport conditions.

---

# 2. Transport Layer Responsibility

The underlying transport stack is responsible for:

- Packet delivery
- Congestion control
- Flow control
- Retransmission
- Path MTU handling
- Kernel scheduling

Jumping VPN does NOT replace or override transport internals.

---

# 3. Cryptographic Responsibility

Jumping VPN relies on:

- Proven cryptographic primitives
- Secure key exchange mechanisms
- Strong session binding

Cryptographic correctness is the responsibility of:

- The cryptographic implementation
- The chosen crypto libraries
- The hardened deployment configuration

Jumping VPN defines binding semantics,
not new cryptography.

---

# 4. Infrastructure Responsibility

Infrastructure providers remain responsible for:

- Edge firewall policy
- DDoS mitigation
- Load balancing
- Data center redundancy
- Network peering quality
- Hardware reliability

Jumping VPN does not compensate for:

- Physical infrastructure collapse
- Misconfigured routing
- Upstream provider instability beyond TTL bounds

---

# 5. Application Layer Responsibility

Applications using Jumping VPN remain responsible for:

- Application-level retries
- Data consistency logic
- Business transaction handling
- End-to-end encryption (if applicable)

Jumping VPN preserves session continuity,
but does not enforce application semantics.

---

# 6. Operator Responsibility

Operators are responsible for:

- Policy configuration
- Threshold tuning
- Monitoring and observability integration
- Security key rotation policy
- Audit review procedures

Incorrect configuration may degrade performance or security.

---

# 7. Non-Responsibility Areas

Jumping VPN explicitly does NOT guarantee:

- Infinite uptime
- Immunity to volumetric DDoS
- Zero packet loss
- Unlimited recovery
- Legal compliance in all jurisdictions
- Complete anonymity

These must be addressed at other layers.

---

# 8. Behavioral Contract Summary

Jumping VPN guarantees:

- Explicit state transitions
- Bounded adaptation
- No silent renegotiation
- Deterministic termination
- Auditable recovery

Everything outside this contract
belongs to surrounding systems.

---

# 9. Architectural Position

Jumping VPN sits:

Above: Transport protocols  
Below: Application logic  

It is a session control layer for volatile environments.

---

# Final Statement

Systems fail when responsibility is unclear.

Jumping VPN defines its boundaries explicitly.

It does not attempt to own the entire stack.
It owns volatility management — and nothing beyond it.