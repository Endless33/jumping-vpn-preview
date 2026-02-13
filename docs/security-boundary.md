# Security Boundary Definition — Jumping VPN

This document defines the explicit security boundary of Jumping VPN.

It clarifies:

- What the protocol guarantees
- What the protocol does NOT guarantee
- Where responsibility shifts to the operator or environment

Clarity of boundary is a core design principle.

---

# 1) Protocol Security Objective

Primary objective:

Preserve deterministic session continuity under transport volatility
without violating identity integrity.

This includes:

- Controlled reattach
- Anti-replay guarantees
- Bounded recovery windows
- Single-active transport invariant
- Explicit state transitions

It does NOT include global anonymity or endpoint protection.

---

# 2) Trust Assumptions

The model assumes:

- The endpoint is not compromised
- The server gateway is trusted infrastructure
- On-path attackers can observe and disrupt traffic
- Transport-level disruption is expected behavior

The protocol is designed to tolerate disruption —
not endpoint compromise.

---

# 3) Identity Boundary

Session identity is:

- Cryptographically bound
- Stable across transport changes
- Invalidated only by explicit termination

Identity is NOT:

- Anonymous by design
- Decoupled from endpoint compromise
- Resistant to local key theft

If endpoint keys are stolen,
identity compromise is out of scope for this layer.

---

# 4) Transport Threat Model

Assumed attacker capabilities:

- Packet loss injection
- Delay injection
- Transport reset attempts
- NAT churn interference
- Path disruption

Not assumed:

- Ability to forge proof-of-possession
- Ability to bypass freshness validation

Transport instability alone must not grant identity takeover.

---

# 5) Replay & Reattach Boundary

Reattach requires:

- Valid SessionID
- Proof-of-possession
- Freshness validation (anti-replay window)

Replay attacks:

- Must be rejected deterministically
- Must not mutate session state
- Must emit security event

Failure to validate freshness must never result in silent fallback.

---

# 6) Cluster Safety Boundary

In distributed deployments:

Single-active ownership must be guaranteed.

Without authoritative ownership:

- Reattach must be rejected
- Dual-active binding must not occur

Consistency is preferred over ambiguous availability.

---

# 7) Observability Boundary

Logging and telemetry:

- Must not block state transitions
- Must not influence correctness
- Must not cause session termination

If telemetry pipeline fails:

- Protocol continues
- Visibility degrades
- Correctness remains intact

---

# 8) Explicit Non-Guarantees

Jumping VPN does NOT guarantee:

- Anonymity against global adversaries
- Resistance to endpoint malware
- Censorship bypass under nation-state filtering
- Data confidentiality beyond transport encryption layer
- Side-channel resistance at hardware level

Those are separate system layers.

---

# 9) Failure Boundary

When instability exceeds defined policy bounds:

Session must:

- Enter DEGRADED
OR
- TERMINATE

Silence is forbidden.
Implicit fallback is forbidden.
Undefined states are forbidden.

Failure must be deterministic and reason-coded.

---

# 10) Abuse Boundary

Protection mechanisms must prevent:

- Infinite reattach loops
- Switch amplification attacks
- Replay floods causing state mutation
- Session table exhaustion

Mitigations include:

- Rate limiting
- TTL enforcement
- Bounded replay windows
- Deterministic rejection

---

# 11) Security Design Philosophy

Security is defined by:

- Explicit invariants
- Bounded behavior
- Deterministic transitions
- Clear termination rules
- No hidden heuristics

Ambiguity is a vulnerability.
Implicit behavior is a risk.

---

# 12) Responsibility Separation

Protocol layer:
- Session continuity
- Identity binding
- Bounded recovery

Transport layer:
- Encryption primitives
- Packet delivery

Operator layer:
- Infrastructure hardening
- Cluster safety
- Key management lifecycle
- Deployment configuration

Endpoint layer:
- Local system security
- Credential protection

---

Security boundary clarity is mandatory
for serious engineering evaluation.

Session is the anchor.
Transport is volatile.
Security must be bounded.