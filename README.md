# 🧬 Jumping VPN — Architectural Preview

Jumping VPN is a session‑centric VPN architecture built for environments where transport volatility is the norm, not an exception.

Traditional VPNs bind identity to a single transport.  
Jumping VPN binds identity to a persistent session, while transports remain replaceable, volatile attachments.

This repository contains:

- architectural documentation  
- behavioral models  
- contract‑first demo  
- mutation logs  
- minimal behavioral prototypes  
- full demo engine (deterministic, observable, reproducible)

This is not a production release.

Repository:  
https://github.com/Endless33/jumping-vpn-preview

---

## 🎥 Demo Engine (Contract‑First)

Jumping VPN uses a contract‑first demo model: behavior is defined before implementation.

Demo documents:

- DEMO_SPEC.md  
- DEMO_OUTPUT_FORMAT.md  
- DEMO_SCENARIO.md  
- DEMO_TIMELINE.jsonl  
- STATUS.md  
- REVIEW_CHECKLIST.md  

The demo contract validates:

- identity anchoring  
- volatility modeling  
- multipath scoring  
- bounded adaptation  
- deterministic transport switch  
- recovery back to ATTACHED  

Session is the anchor.  
Transport is volatile.

---

## 🚀 Quick Demo Run

Requirements: Python 3.10+

Run the demo:

python run_demo.py

This generates:

- demo_output.jsonl  
- DEMO_METRICS.json  
- DEMO_DASHBOARD.json  
- DEMO_ECOSYSTEM/  
- DEMO_PACKAGE.zip  

The demo is deterministic, observable, reproducible.

---

## 🔎 Core Thesis

Modern networks are inherently unstable:

- mobile networks flap  
- NAT mappings expire  
- cross‑border routes degrade  
- packet loss spikes  
- paths die unpredictably  

Most VPNs treat this as failure.  
Jumping VPN treats it as modeled behavior.

### Separation of Concerns

- Session identity — persistent, cryptographically anchored  
- Transport binding — volatile, replaceable, auditable  

Transport death ≠ session death (within bounded policy).

---

## 🧠 Architectural Model

Jumping VPN is defined by behavior over time, not static configuration.

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

- BIRTH  
- ATTACHED  
- VOLATILE  
- DEGRADED  
- REATTACHING  
- RECOVERING  
- TERMINATED  

Transitions are deterministic and logged.

---

## 📂 Repository Structure (Simplified)

docs/ demo_engine/ poc/ core/ run_demo.py README.md

Full structure is documented inside /docs.

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
- server‑side TransportSwitch  
- continuity without identity reset  

See:

- poc/realudpprototype.py  
- poc/README_udp.md  

This is behavioral validation, not production cryptography.

---

## 🛡 Threat Model & Boundaries

Jumping VPN defines:

- adversary assumptions  
- deterministic failure boundaries  
- allowed transitions  
- bounded adaptation policies  

Recommended reading:

- docs/core/threat-model.md  
- docs/core/security-boundary.md  
- docs/core/invariants.md  
- docs/core/state-machine.md  

---

## 🚫 Explicit Non‑Goals

Jumping VPN does not aim to provide:

- anonymity  
- censorship bypass  
- endpoint compromise protection  
- anti‑forensics  
- universal VPN replacement  

Scope is intentionally narrow:

Session continuity under transport volatility.

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

Jumping VPN is in architectural validation.

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

Email:  
riabovasvitalijus@gmail.com

---

## Final Principle

Transport instability is not an anomaly —  
it is the default condition of modern networks.

Jumping VPN treats volatility as modeled behavior, not as failure.

Session remains the anchor.  
Transports come and go.

---

## ✅ Demo Trace Validator

A deterministic demo trace is included to verify session continuity behavior.

Trace file:

DEMO_TRACE.jsonl

Validator script:

demo_engine/replay.py

Run validator from repository root:

python demo_engine/replay.py DEMO_TRACE.jsonl

Expected output:

SESSION_CREATED OK  
VOLATILITY_SIGNAL OK  
TRANSPORT_SWITCH OK  
STATE_CHANGE OK  
RECOVERY_COMPLETE OK  

Trace validated successfully.  
Session continuity preserved.

This proves that session identity remains stable while transport attachment changes.