# 🧬 Jumping VPN — Architectural Preview

Jumping VPN is a **session-centric VPN architecture** designed for environments where **transport volatility** is the default state of the network.

Traditional VPN systems often assume transport stability.  
Jumping VPN assumes instability — and models it explicitly.

This repository contains **architectural documentation**, **behavioral models**, and **minimal proof-of-concept prototypes**.

It is **not** a production release.

---

## 🔎 Core Thesis

Modern networks are volatile:

- paths fail
- packet loss spikes
- mobile networks flap
- NAT mappings expire
- cross-border routes degrade

Many VPN systems bind identity to transport.

Jumping VPN separates:

- **Session identity (persistent)**
- **Transport binding (replaceable)**

Transport death does not imply session death (within defined bounds).

---

## 🧠 Architectural Model

Jumping VPN is defined by **behavior over time**.

### Session-Centric Identity

The session is the source of truth:

- Identity belongs to the session
- Transport is an attachment
- Reattachment preserves identity continuity

### Deterministic Recovery

Transport failover is:

- explicit
- policy-bounded
- rate-limited
- logged
- auditable

No silent renegotiation.  
No uncontrolled session resets.

### Volatility as State

Transport instability is represented in the state machine:

- `BIRTH`
- `ATTACHED`
- `VOLATILE`
- `DEGRADED`
- `RECOVERING`
- `TERMINATED`

Transitions are deterministic and reason-coded.

---

## 📂 Repository Structure

. ├── docs/ │   ├── index.md │   ├── reviewer-guide.md │   ├── architecture-overview.md │   ├── architecture-overview.md │   ├── state-machine.md │   ├── invariants.md │   ├── formal-invariants-machine.md │   ├── formal-spec-outline.md │   ├── formal-properties.md │   ├── security-boundary.md │   ├── security-boundary-model.md │   ├── security-model-deep-dive.md │   ├── threat-model.md │   ├── attack-scenarios.md │   ├── control-plane-sequence.md │   ├── performance-model.md │   ├── benchmark-plan.md │   ├── integration-evaluation.md │   ├── production-readiness-checklist.md │   ├── production-readiness-gap.md │   ├── protocol-rationale.md │   ├── comparative-analysis.md │   ├── whitepaper-draft.md │   ├── design-decisions.md │   ├── limitations.md │   ├── non-goals.md │   ├── comparison-model.md │   ├── use-case-fintech-failover.md │   ├── test-scenarios.md │   ├── roadmap.md │   ├── reason-codes.md │   ├── security-review-plan.md │   └── MutationLogs/ ├── spec/ │   └── vrp-preview.md ├── poc/ │   ├── demo.py │   ├── session.py │   ├── transport.py │   ├── policy.py │   ├── logger.py │   ├── real_udp_prototype.py │   ├── README.md │   └── README_udp.md └── core/ └── README.md

> Note: `core/` is a **production-oriented skeleton** (control-plane structure),
> intended to encode invariants and module boundaries in code.

---

## 🧬 Mutation Logs

Mutation Logs document architectural evolution and behavioral modeling.

They describe how session lifecycle, volatility handling, and bounded adaptation matured over time.

---

## 🌐 Real UDP Prototype (Behavioral Validation)

A minimal real UDP client/server prototype demonstrates:

- Session creation (`session_id`)
- Transport death (socket close / port change)
- Explicit `REATTACH_REQUEST`
- Verified session-bound proof
- Server-side `TransportSwitch`
- Continued session without reset (within TTL)

See:

- `poc/real_udp_prototype.py`
- `poc/README_udp.md`

This is behavioral validation only.  
It is not production-grade cryptography.

---

## 🛡 Threat Model & Boundaries

Jumping VPN explicitly defines:

- adversary assumptions
- allowed state transitions
- deterministic failure boundaries
- bounded adaptation policies

Recommended:

- `docs/threat-model.md`
- `docs/security-boundary.md`
- `docs/invariants.md`
- `docs/state-machine.md`
- `docs/security-review-plan.md`

---

## 🚫 Explicit Non-Goals

Jumping VPN does not claim:

- Tor-level anonymity
- censorship bypass guarantees
- endpoint compromise protection
- anti-forensics capabilities
- universal VPN replacement

Scope is intentionally constrained to:

**session continuity under transport volatility**

See:

- `docs/non-goals.md`
- `docs/limitations.md`

---

## 🔬 Open Engineering Questions

The following areas remain under exploration:

- Distributed session ownership model
- Clustered state synchronization
- Formal verification feasibility
- Performance under high churn (10k+ sessions)
- QUIC-based transport experiments

These are not omissions.  
They are active research directions.

This repository prioritizes **behavioral correctness**
over feature completeness.

---

## 🎯 Intended Audience

This project may be relevant to:

- infrastructure teams operating in volatile mobile environments
- fintech platforms experiencing session collapse during failover
- security architects designing deterministic recovery systems
- operators exploring transport abstraction models

---

## 🧭 Project Philosophy

Jumping VPN is not driven by market validation cycles
or short-term visibility.

It is an architectural thesis.

The system evolves based on behavioral correctness,
formal constraints, and internal consistency —
not external approval.

Ideas compete in the open.
Architectures mature over time.

This repository documents that evolution.

Architecture does not require permission to exist.
It requires rigor.

---

## 📈 Status

Jumping VPN is currently in **architectural validation** phase.

This repository:

- is not production-ready
- does not contain hardened cryptographic implementation
- does not expose full protocol internals
- represents staged documentation and behavioral modeling

---

## 🤝 Technical Discussions

Open to technical discussions with teams exploring:

- deterministic transport recovery
- bounded adaptation models
- session persistence under volatility
- operator-grade observability for adaptive systems

📧 Contact: **riabovasvitalijus@gmail.com**

---

## Final Principle

Transport instability is not an anomaly.

It is the default condition of modern networks.

Jumping VPN treats volatility as modeled behavior —
not as fatal error.

**Session remains the anchor.  
Transports come and go.**
```0