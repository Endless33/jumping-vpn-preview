# 🧬 Jumping VPN — Architectural Preview

Jumping VPN is a **session‑centric VPN architecture** built for environments where **transport volatility is the norm**, not an exception.

Traditional VPNs bind identity to a single transport.  
Jumping VPN binds identity to a **persistent session**, while transports remain **replaceable, volatile attachments**.

This repository contains:

- architectural documentation  
- behavioral models  
- demo contract (contract‑first)  
- mutation logs  
- minimal behavioral prototypes  

It is **not** a production release.

---

## 🎥 Demo Package (Contract‑First)

Jumping VPN uses a **contract‑first demo model**:  
behavior is defined before implementation.

Demo documents:

- [`DEMO_SPEC.md`](docs/demo/DEMO_SPEC.md)
- [`DEMO_OUTPUT_FORMAT.md`](docs/demo/DEMO_OUTPUT_FORMAT.md)
- [`DEMO_SCENARIO.md`](docs/demo/DEMO_SCENARIO.md)
- [`DEMO_TIMELINE.jsonl`](docs/demo/DEMO_TIMELINE.jsonl)
- [`STATUS.md`](docs/demo/STATUS.md)
- [`REVIEW_CHECKLIST.md`](docs/demo/REVIEW_CHECKLIST.md)

The demo contract validates:

- identity anchoring  
- volatility modeling  
- multipath scoring  
- bounded adaptation  
- deterministic transport switch  
- recovery back to `ATTACHED`  

**Session is the anchor.  
Transport is volatile.**

---

## 🔎 Core Thesis

Modern networks are inherently unstable:

- mobile networks flap  
- NAT mappings expire  
- cross‑border routes degrade  
- packet loss spikes  
- paths die unpredictably  

Most VPNs treat this as failure.  
Jumping VPN treats it as **modeled behavior**.

### Separation of Concerns

- **Session identity** — persistent, cryptographically anchored  
- **Transport binding** — volatile, replaceable, auditable  

Transport death ≠ session death (within bounded policy).

---

## 🧠 Architectural Model

Jumping VPN is defined by **behavior over time**, not by static configuration.

### Session‑Centric Identity

The session is the source of truth:

- identity belongs to the session  
- transport is an attachment  
- reattachment preserves continuity  

### Deterministic Recovery

Transport failover is:

- explicit  
- reason‑coded  
- rate‑limited  
- policy‑bounded  
- auditable  

No silent renegotiation.  
No uncontrolled resets.

### Volatility as State

Instability is represented explicitly:

- `BIRTH`  
- `ATTACHED`  
- `VOLATILE`  
- `DEGRADED`  
- `REATTACHING`  
- `RECOVERING`  
- `TERMINATED`  

Transitions are deterministic and logged.

---

## 📂 Repository Structure

. ├── docs/ │   ├── index.md │   ├── architecture-overview.md │   ├── reviewer-guide.md │   ├── core/ │   │   ├── state-machine.md │   │   ├── invariants.md │   │   ├── reconnect.md │   │   ├── reason-codes.md │   │   ├── security-boundary.md │   │   ├── threat-model.md │   │   ├── limitations.md │   │   ├── non-goals.md │   │   ├── design-decisions.md │   │   ├── protocol-rationale.md │   │   ├── performance-model.md │   │   ├── benchmark-plan.md │   │   ├── integration-evaluation.md │   │   ├── production-readiness-checklist.md │   │   └── production-readiness-gap.md │   ├── MutationLogs/ │   └── demo/ │       ├── DEMO_SPEC.md │       ├── DEMO_OUTPUT_FORMAT.md │       ├── DEMO_SCENARIO.md │       ├── DEMO_TIMELINE.jsonl │       ├── STATUS.md │       └── REVIEW_CHECKLIST.md ├── spec/ │   └── vrp-preview.md ├── poc/ │   ├── demo.py │   ├── session.py │   ├── transport.py │   ├── policy.py │   ├── logger.py │   ├── realudpprototype.py │   └── README_udp.md └── core/ └── README.md

`core/` defines **production‑oriented boundaries and invariants**.  
`docs/` defines **architecture, behavior, and demo contract**.  
`poc/` provides **behavioral validation**, not production crypto.

---

## 🧬 Mutation Logs

Mutation Logs document the evolution of:

- session lifecycle  
- volatility modeling  
- bounded adaptation  
- reconnect semantics  
- protocol invariants  

They serve as architectural archaeology.

---

## 🌐 Real UDP Prototype (Behavioral Validation)

A minimal UDP prototype demonstrates:

- session creation  
- transport death  
- explicit reattach  
- proof‑based validation  
- server‑side `TransportSwitch`  
- continuity without identity reset  

See:

- `poc/realudpprototype.py`  
- `poc/README_udp.md`  

This is **behavioral validation**, not production cryptography.

---

## 🛡 Threat Model & Boundaries

Jumping VPN defines:

- adversary assumptions  
- deterministic failure boundaries  
- allowed transitions  
- bounded adaptation policies  

Recommended reading:

- `docs/core/threat-model.md`  
- `docs/core/security-boundary.md`  
- `docs/core/invariants.md`  
- `docs/core/state-machine.md`  

---

## 🚫 Explicit Non‑Goals

Jumping VPN does **not** aim to provide:

- anonymity  
- censorship bypass  
- endpoint compromise protection  
- anti‑forensics  
- universal VPN replacement  

Scope is intentionally narrow:

**session continuity under transport volatility**

---

## 🔬 Open Engineering Questions

Active research areas:

- distributed session ownership  
- clustered state replication  
- formal verification  
- QUIC‑based transport experiments  
- performance under high churn  

Behavioral correctness takes priority.

---

## 🎯 Intended Audience

Relevant for:

- mobile infrastructure teams  
- fintech platforms with session collapse issues  
- security architects designing deterministic recovery  
- operators exploring transport abstraction  

---

## 🧭 Philosophy

Jumping VPN is an architectural thesis:

- behavior first  
- contracts first  
- rigor over hype  

Architecture does not require permission.  
It requires consistency.

---

## 📈 Status

Jumping VPN is in **architectural validation**.

This repository:

- is not production‑ready  
- does not include hardened cryptography  
- exposes staged documentation  
- focuses on behavioral modeling  

---

## 🤝 Technical Discussions

Open to discussions on:

- deterministic recovery  
- bounded adaptation  
- session persistence  
- operator‑grade observability  

📧 **riabovasvitalijus@gmail.com**

---

## Final Principle

Transport instability is not an anomaly —  
it is the default condition of modern networks.

Jumping VPN treats volatility as modeled behavior, not as failure.

**Session remains the anchor.  
Transports come and go.**