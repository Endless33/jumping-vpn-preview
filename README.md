# 🧬 Jumping VPN — Architectural Preview

Jumping VPN is a session-centric VPN architecture designed for transport volatility.

Unlike traditional VPNs that assume stable paths and renegotiate on failure,  
Jumping VPN models transport instability as an expected state — not an exception.

This repository is a public architectural preview of the concepts, mutation logs,
and protocol fragments behind the system.

---

## 🔎 Core Thesis

Most VPNs treat transport as stable.

In reality:
- paths fail
- packet loss spikes
- mobile networks flap
- cross-border routes degrade

Jumping VPN flips the model:

> The session is the source of truth.  
> Transports are replaceable.  
> Volatility is modeled, not treated as failure.

---

## 🧠 Architectural Principles

### 1. Session-Centric Design
The session exists independently of any specific transport path.  
Transport switching does not imply identity renegotiation.

### 2. Deterministic Recovery
Transport failover is:
- explicit
- bounded
- logged
- auditable

No silent renegotiation.  
No uncontrolled session resets.

### 3. Volatility as a First-Class State
Transport degradation is represented as a modeled state:
- ATTACHED
- VOLATILE
- DEGRADED
- RECOVERING

Switch decisions are intentional and traceable.

### 4. Operator-Grade Observability
Every transition can be inspected.  
Adaptation is explainable — not heuristic guesswork.

---

## 📂 Repository Structure

```
jumping-vpn/
├── docs/
│   ├── MutationLogs/
│   ├── architecture.md
│   ├── onepager.md
│   └── demo/
├── spec/
│   └── vrp-preview.md
└── README.md
```

---

## 🧬 Mutation Logs

The Mutation Logs document the evolutionary steps of the architecture.

Recommended starting points:

- `MutationLog21.md` — Drift Begins Where Routing Ends  
- `MutationLog22.md` — Why VRP Refuses to Stabilize  

Each log describes architectural intent, state modeling, and behavioral guarantees.

---

## 🛰 Protocol Layer: VRP (Veil Routing Protocol)

Jumping VPN is built on top of VRP — an experimental routing concept
designed for drift-aware behavior rather than static topology assumptions.

This repository contains preview notes only.  
The hardened implementation layer is not published here.

---

## 🧪 Conceptual Demo

A safe mock session lifecycle demo is available:

```
cd docs/demo
chmod +x mock-session.sh
./mock-session.sh
```

The demo simulates:

- session birth
- transport attachment
- volatility phase
- degradation handling
- deterministic recovery

No real routing or cryptographic primitives are exposed.

---

## ⚠️ Status

Jumping VPN is currently in architectural validation and staged development.

This repository is:
- not a full implementation
- not a production release
- not a commercial distribution

It is an architectural window into the system’s design philosophy.

---

## 🎯 Who This Is For

This project may be relevant to:

- infrastructure teams operating in volatile mobile environments
- fintech platforms experiencing session collapse during failover
- security architects designing deterministic recovery systems
- operators exploring next-generation transport abstraction models

---

## 🤝 Collaboration & Technical Discussions

I am open to technical discussions with:

- infrastructure providers
- cybersecurity firms
- mobile network operators
- resilience-focused engineering teams

If you are working on systems affected by transport instability
and want to explore deterministic recovery models,
feel free to reach out.

📧 **Contact:**  
riabovasvitalijus@gmail.com

---

## 📌 Disclaimer

This repository does not contain full source code for Jumping VPN or VRP.

It represents architectural direction, behavioral modeling concepts,
and staged documentation of system evolution.

Implementation details are released in controlled phases.

---

Session remains the anchor.  
Transports come and go.