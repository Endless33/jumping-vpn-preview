# 🧬 Jumping VPN — Architectural Preview

Jumping VPN is a **session-centric VPN architecture** designed for environments where transport volatility is the norm.

Traditional VPNs assume stable paths and treat instability as failure.  
Jumping VPN models instability as an expected state within a bounded, deterministic lifecycle.

This repository is a **public architectural preview** of the system’s behavioral model, documentation, and conceptual validation artifacts.

It is not a production release.

---

## 🔎 Core Thesis

Most VPNs bind identity and continuity directly to transport.

In reality:

- paths fail  
- packet loss spikes  
- mobile networks flap  
- NAT mappings expire  
- cross-border routes degrade  

Jumping VPN separates concerns:

- **Session is the source of truth**
- **Transports are replaceable**
- **Volatility is modeled explicitly**
- **Failure boundaries are deterministic**

---

## 🧠 Architectural Model

### Session-Centric Design

A session exists independently of any single transport path.  
Transport switching does **not** imply identity renegotiation.

### Deterministic Recovery

Transport failover is:

- explicit  
- bounded  
- rate-limited  
- logged  
- auditable  

No silent renegotiation.  
No uncontrolled session resets.

### Volatility as a State

Transport degradation is represented formally:

- `BIRTH`
- `ATTACHED`
- `VOLATILE`
- `DEGRADED`
- `RECOVERING`
- `TERMINATED`

State transitions are defined, bounded, and reason-coded.

### Operator-Grade Observability

All critical transitions emit structured events.

Adaptation is explainable.  
Behavior is auditable.  
Failure is deterministic.

---

## 📂 Repository Structure

```
.
├── docs/
│   ├── MutationLogs/
│   ├── architecture.md
│   ├── onepager.md
│   ├── faq.md
│   ├── threat-model.md
│   ├── state-machine.md
│   ├── design-decisions.md
│   ├── limitations.md
│   ├── security-review-plan.md
│   ├── roadmap.md
│   └── test-scenarios.md
├── spec/
│   └── vrp-preview.md
└── poc/
    ├── demo.py
    ├── session.py
    ├── transport.py
    ├── policy.py
    ├── logger.py
    └── README.md
```

---

## 🧬 Mutation Logs

Mutation Logs document the architectural evolution of the system.

Suggested starting points:

- `MutationLog21.md` — Drift Begins Where Routing Ends  
- `MutationLog22.md` — Why VRP Refuses to Stabilize  

Each log describes design intent, state modeling, and behavioral guarantees.

---

## 🛰 Protocol Layer — VRP (Veil Routing Protocol)

Jumping VPN is conceptually built on top of VRP — an experimental routing model designed for drift-aware behavior rather than static topology assumptions.

This repository contains preview documentation only.  
The hardened implementation layer is not published here.

---

## 🧪 Behavioral Proof of Concept

A minimal PoC exists under `/poc/` to demonstrate the core architectural claim:

> A session can survive transport death if an alternative transport is available.

Run locally:

```bash
python -m poc.demo
```

Output:

- `out/poc_run.jsonl` (structured JSONL log)

Expected behavior:

- `TransportKilled` event occurs  
- `TransportSwitch` event occurs  
- Session returns to `ATTACHED`  
- No `TERMINATED` state while a viable backup transport exists  

This PoC validates behavioral modeling, not production security guarantees.

---

## 🌐 Real UDP Prototype (Minimal Transport-Level Proof)

A minimal real UDP client/server prototype is available to demonstrate
session reattachment over an actual transport:

- `poc/real_udp_prototype.py`
- `poc/README_udp.md`

This prototype shows:

- Session created once (`session_id`)
- Active transport dies (socket closed / port changes)
- Client reattaches a new transport using session-bound proof
- Server emits explicit `TransportSwitch`
- Session continues without reset (within TTL)

This is behavioral validation only — not production security.

---

## 🛡 Threat Model & Boundaries

See:

- `docs/threat-model.md`
- `docs/state-machine.md`
- `docs/design-decisions.md`
- `docs/limitations.md`

Jumping VPN explicitly defines:

- adversary assumptions  
- allowed/forbidden transitions  
- bounded adaptation rules  
- deterministic failure conditions  

It does **not** claim:

- endpoint compromise protection  
- full anonymity guarantees  
- censorship bypass capability  
- production-grade cryptographic hardening (in this preview)

---

## 📈 Development Roadmap

The roadmap outlines staged evolution:

1. Architectural validation  
2. Core session engine implementation  
3. Volatility handling & observability  
4. Security hardening & review  
5. Controlled pilot deployment  

See `docs/roadmap.md`.

---

## ⚠️ Status

Jumping VPN is currently in **architectural validation phase**.

This repository:

- is not a full implementation  
- is not production-ready  
- is not commercially distributed  
- does not expose hardened cryptographic logic  

It represents behavioral modeling and staged architectural direction.

---

## 🎯 Intended Audience

This project may be relevant to:

- infrastructure teams operating in volatile mobile environments  
- fintech platforms experiencing session collapse during failover  
- security architects designing deterministic recovery systems  
- operators exploring transport abstraction models  

---

## 🤝 Technical Discussions

Open to technical discussions with teams exploring:

- deterministic transport recovery  
- session persistence under volatility  
- bounded adaptation models  
- observability for adaptive systems  

📧 **Contact:** riabovasvitalijus@gmail.com

---

## Final Principle

Transport instability is not an anomaly.

It is the default state of modern networks.

Jumping VPN treats volatility as modeled behavior —
not as fatal error.

**Session remains the anchor.  
Transports come and go.**