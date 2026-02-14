# 🧬 Jumping VPN — Architectural Preview

Jumping VPN is a **session-centric VPN architecture** designed for environments where **transport volatility** is the default state of the network.

Traditional VPN systems often assume transport stability.  
Jumping VPN assumes instability — and models it explicitly.

This repository contains **architectural documentation**, **behavioral models**, **demo contract**, and **minimal proof-of-concept prototypes**.

It is **not** a production release.

---

## 🎥 Demo Package (Contract‑First)

Jumping VPN uses a **contract‑first demo model**:  
behavior is defined before implementation.

Demo documents:

- [`DEMO_SPEC.md`](docs/demo/DEMO_SPEC.md) — what the demo must show  
- [`DEMO_OUTPUT_FORMAT.md`](docs/demo/DEMO_OUTPUT_FORMAT.md) — JSONL event format  
- [`STATUS.md`](docs/demo/STATUS.md) — what exists today / what is not public  
- [`REVIEW_CHECKLIST.md`](docs/demo/REVIEW_CHECKLIST.md) — how to validate the demo  

The demo contract defines:

- identity anchoring  
- volatility handling  
- flow‑control reaction  
- multipath scoring  
- deterministic transport switch  
- recovery back to `ATTACHED`  

Session is the anchor.  
Transport is volatile.

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

`
.
├── docs/
│   ├── index.md
│   ├── reviewer-guide.md
│   ├── architecture-overview.md
│   ├── state-machine.md
│   ├── invariants.md
│   ├── threat-model.md
│   ├── non-goals.md
│   ├── limitations.md
│   ├── reason-codes.md
│   ├── MutationLogs/
│   └── demo/
│       ├── DEMO_SPEC.md
│       ├── DEMOOUTPUTFORMAT.md
│       ├── STATUS.md
│       └── REVIEW_CHECKLIST.md
├── spec/
│   └── vrp-preview.md
├── poc/
│   ├── demo.py
│   ├── session.py
│   ├── transport.py
│   ├── policy.py
│   ├── logger.py
│   ├── realudpprototype.py
│   └── README_udp.md
└── core/
    └── README.md
`

`core/` is a **production-oriented skeleton** intended to encode invariants and module boundaries.

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

---

## 🔬 Open Engineering Questions

Active research areas:

- distributed session ownership  
- clustered state synchronization  
- formal verification  
- performance under high churn  
- QUIC-based transport experiments  

This repository prioritizes **behavioral correctness** over feature completeness.

---

## 🎯 Intended Audience

Relevant for:

- infrastructure teams in volatile mobile environments  
- fintech platforms suffering session collapse  
- security architects designing deterministic recovery  
- operators exploring transport abstraction  

---

## 🧭 Project Philosophy

Jumping VPN is not driven by market cycles.  
It is an architectural thesis.

Behavior first.  
Contracts first.  
Rigor over hype.

Architecture does not require permission to exist.  
It requires consistency.

---

## 📈 Status

Jumping VPN is in **architectural validation** phase.

This repository:

- is not production-ready  
- does not contain hardened cryptography  
- does not expose full protocol internals  
- represents staged documentation and behavioral modeling  

---

## 🤝 Technical Discussions

Open to discussions on:

- deterministic transport recovery  
- bounded adaptation  
- session persistence  
- operator-grade observability  

📧 Contact: **riabovasvitalijus@gmail.com**

---

## Final Principle

Transport instability is not an anomaly.  
It is the default condition of modern networks.

Jumping VPN treats volatility as modeled behavior — not as fatal error.

**Session remains the anchor.  
Transports come and go.**