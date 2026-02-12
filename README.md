# 🧬 Jumping VPN — Architectural Preview

Jumping VPN is a **session-centric VPN architecture** designed for **transport volatility**.

Traditional VPNs assume stable paths and often treat instability as failure.
Jumping VPN treats instability as an expected state — modeled explicitly in the session lifecycle.

This repository is a **public architectural preview**: documentation, mutation logs, and protocol fragments.
It is not a production release.

---

## 🔎 Core Thesis

Most VPNs bind identity and continuity to a transport.

Reality:
- paths fail
- packet loss spikes
- mobile networks flap
- NAT mappings expire
- cross-border routes degrade

Jumping VPN flips the model:

- **Session is the source of truth**
- **Transports are replaceable**
- **Volatility is modeled, not treated as failure**

---

## 🧠 Architectural Principles

### 1) Session-Centric Design
A session exists independently of any specific transport path.
Transport switching does **not** imply identity renegotiation.

### 2) Deterministic Recovery
Transport failover is:
- explicit
- bounded
- logged
- auditable

No silent renegotiation.  
No uncontrolled session resets.

### 3) Volatility as a First-Class State
Transport degradation is represented as a modeled state:

- `ATTACHED`
- `VOLATILE`
- `DEGRADED`
- `RECOVERING`

Switch decisions are intentional and traceable.

### 4) Operator-Grade Observability
Every critical transition can be inspected.
Adaptation is explainable — not heuristic guesswork.

---

## 📂 Repository Structure

. ├── docs/ │   ├── MutationLogs/ │   ├── architecture.md │   ├── onepager.md │   ├── faq.md │   ├── threat-model.md │   ├── state-machine.md │   ├── design-decisions.md │   ├── limitations.md │   ├── security-review-plan.md │   ├── roadmap.md │   └── test-scenarios.md ├── spec/ │   └── vrp-preview.md └── poc/ ├── demo.py ├── session.py ├── transport.py ├── policy.py ├── logger.py └── README.md

---

## 🧬 Mutation Logs

Mutation Logs document the architecture’s evolution.

Recommended starting points:
- `MutationLog21.md` — *Drift Begins Where Routing Ends*
- `MutationLog22.md` — *Why VRP Refuses to Stabilize*

Each log describes intent, state modeling, and behavioral guarantees.

---

## 🛰 Protocol Layer: VRP (Veil Routing Protocol)

Jumping VPN is built on top of VRP — an experimental routing concept designed for drift-aware behavior rather than static topology assumptions.

This repository contains preview notes only.
The hardened implementation layer is not published here.

---

## 🧪 Conceptual Demo (Legacy)

A safe mock session lifecycle demo is available:

```bash
cd docs/demo
chmod +x mock-session.sh
./mock-session.sh

The demo simulates:
session birth
transport attachment
volatility phase
degradation handling
deterministic recovery
No real routing or cryptographic primitives are exposed.
✅ Behavioral PoC (Session survives transport death)
A minimal Proof of Concept exists under /poc/ to demonstrate the core claim: a session remains alive while a transport dies and a backup transport is available.
Run (local environment):
Bash
Копировать код
python -m poc.demo
Output:
out/poc_run.jsonl (JSONL event log)
Look for:
TransportKilled
TransportSwitch
SessionStateChange
⚠️ Status
Jumping VPN is currently in architectural validation and staged development.
This repository is:
not a full implementation
not a production release
not a commercial distribution
It is an architectural window into the system’s design philosophy.
🎯 Who This Is For
This project may be relevant to:
infrastructure teams operating in volatile mobile environments
fintech platforms experiencing session collapse during failover
security architects designing deterministic recovery systems
operators exploring transport abstraction and deterministic recovery
🤝 Collaboration & Technical Discussions
Open to technical discussions with teams exploring:
deterministic transport recovery
session persistence under volatility
transport abstraction models
observability/audit requirements for adaptive systems
📧 Contact: riabovasvitalijus@gmail.com
📌 Disclaimer
This repository does not contain full source code for Jumping VPN or VRP.
It represents architectural direction, behavioral modeling concepts, and staged documentation of system evolution.
Implementation details are released in controlled phases.
Session remains the anchor.
Transports come and go.