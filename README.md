# 🧬 Jumping VPN — Architectural Preview

Jumping VPN is a **session‑centric VPN architecture** built for environments where **transport volatility is the norm, not the exception**.

Traditional VPNs bind identity to a single transport.  
Jumping VPN binds identity to a **persistent session**, while transports remain **replaceable, volatile attachments**.

---

## 📦 Repository Contents

This repository contains:

- 📐 Architectural documentation  
- 🧠 Behavioral models  
- 📃 Contract‑first demo specification  
- 🧬 Mutation logs  
- 🧪 Minimal behavioral prototypes  
- 🎥 Full demo engine (deterministic, observable, reproducible)

> This is not a production release.  
> This is a protocol organism under active mutation.

Repository:  
[github.com/Endless33/jumping-vpn-preview](https://github.com/Endless33/jumping-vpn-preview)

---

## 📚 Documentation

- [Session Identity Architecture](docs/identity.md)  
- [Trace Analysis: Deterministic Session Continuity](docs/trace-analysis.md)  
- [Audience Analysis](docs/audience.md)  
- [Clone Spike: February 2026](docs/clone-spike.md)  
- [Mutation Log Index](docs/MutationLogIndex.md)  
- [Acquisition & Integration Pathways](docs/acquisition.md)  
- [Architectural Overview](docs/README_ARCH.md)

---

## 🧭 Who’s Watching

Jumping VPN is attracting attention from:

- VPN engineers ([OpenVPN](https://openvpn.net), [Nord Security](https://nordsecurity.com))  
- Cybersecurity professionals (Fortinet, Sonar, JayDevs)  
- FinTech & Infrastructure (Revolut, LMAX Group, Credo Bank)  
- Privacy-focused builders (AveryBit)  
- Government & Healthcare (uHealth, Digital Services)  
- Overlay protocol engineers (uNetwork)  
- Geographic clusters: Zürich, Vilnius, London, Berlin, Singapore, Toronto

📊 [See full audience profile](docs/audience.md)

---

## 📊 Signals

- [Clone Spike: February 2026](docs/clone-spike.md)  
- [Audience Analysis](docs/audience.md)  
- [Session Identity Architecture](docs/identity.md)

---

## 🎥 Demo Engine (Contract‑First)

Jumping VPN uses a **contract‑first demo model**: behavior is defined before implementation.

Demo artifacts:

- `DEMO_SPEC.md`  
- `DEMO_OUTPUT_FORMAT.md`  
- `DEMO_SCENARIO.md`  
- `DEMO_TIMELINE.jsonl`  
- `STATUS.md`  
- `REVIEW_CHECKLIST.md`

The demo contract validates:

- Identity anchoring  
- Volatility modeling  
- Multipath scoring  
- Bounded adaptation  
- Deterministic transport switch  
- Recovery back to ATTACHED

> Session is the anchor.  
> Transport is volatile.

---

## 🚀 Quick Demo Run

**Requirements:** Python 3.10+

```bash
python run_demo.py

This generates:

- demo_output.jsonl  
- DEMO_METRICS.json  
- DEMO_DASHBOARD.json  
- DEMO_ECOSYSTEM/  
- DEMO_PACKAGE.zip

The demo is deterministic, observable, and reproducible.

---

🔎 Core Thesis

Modern networks are inherently unstable:

- Mobile networks flap  
- NAT mappings expire  
- Cross‑border routes degrade  
- Packet loss spikes  
- Paths die unpredictably

Most VPNs treat this as failure.  
Jumping VPN treats it as modeled behavior.

---

🧠 Architectural Model

Jumping VPN is defined by behavior over time, not static configuration.

Session‑Centric Identity

- Session is the source of truth  
- Identity belongs to the session  
- Transport is an attachment  
- Reattachment preserves continuity

Deterministic Recovery

Transport failover is:

- Explicit  
- Reason‑coded  
- Rate‑limited  
- Policy‑bounded  
- Auditable

No silent renegotiation.  
No uncontrolled resets.

Volatility as State

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

📂 Repository Structure (Simplified)

`
docs/  
demo_engine/  
poc/  
core/  
run_demo.py  
README.md
`

Full structure is documented inside /docs.

---

🧬 Mutation Logs

Mutation Logs document the evolution of:

- Session lifecycle  
- Volatility modeling  
- Bounded adaptation  
- Reconnect semantics  
- Protocol invariants

They serve as architectural archaeology.

---

🌐 Real UDP Prototype (Behavioral Validation)

A minimal UDP prototype demonstrates:

- Session creation  
- Transport death  
- Explicit reattach  
- Proof‑based validation  
- Server‑side TransportSwitch  
- Continuity without identity reset

See:

This is behavioral validation, not production cryptography.

---

🛡 Threat Model & Boundaries

Jumping VPN defines:

- Adversary assumptions  
- Deterministic failure boundaries  
- Allowed transitions  
- Bounded adaptation policies

---

🚫 Explicit Non‑Goals

Jumping VPN does not aim to provide:

- Anonymity  
- Censorship bypass  
- Endpoint compromise protection  
- Anti‑forensics  
- Universal VPN replacement

> Scope is intentionally narrow:  
> Session continuity under transport volatility.

---

🔬 Open Engineering Questions

Active research areas:

- Distributed session ownership  
- Clustered state replication  
- Formal verification  
- QUIC‑based transport experiments  
- Performance under high churn

> Behavioral correctness takes priority.

---

🎯 Intended Audience

Relevant for:

- Mobile infrastructure teams  
- FinTech platforms with session collapse issues  
- Security architects designing deterministic recovery  
- Operators exploring transport abstraction

---

🧭 Philosophy

Jumping VPN is an architectural thesis:

- Behavior first  
- Contracts first  
- Rigor over hype

> Architecture does not require permission.  
> It requires consistency.

---

📈 Status

Jumping VPN is in architectural validation.

This repository:

- Is not production‑ready  
- Does not include hardened cryptography  
- Exposes staged documentation  
- Focuses on behavioral modeling

---

🤝 Technical Discussions

Open to discussions on:

- Deterministic recovery  
- Bounded adaptation  
- Session persistence  
- Operator‑grade observability

Contact:  
riabovasvitalijus@gmail.com

---

✅ Demo Trace Validator

A deterministic demo trace is included to verify session continuity behavior.

Trace file:  
DEMO_TRACE.jsonl  
Validator script:  
demo_engine/replay.py

Run validator:

`bash
python demoengine/replay.py DEMOTRACE.jsonl
`

Expected output:

`
SESSION_CREATED OK  
VOLATILITY_SIGNAL OK  
TRANSPORT_SWITCH OK  
STATE_CHANGE OK  
RECOVERY_COMPLETE OK  
`

> Trace validated successfully.  
> Session continuity preserved.

---

🔒 Easter Egg (for reviewers)

If you found this: yes — the roadmap is real.

SESSION_ANCHOR > TRANSPORT

Next milestones:

- Deterministic replay validator  
- Live transport adapter prototype  
- Protocol hardening & formalization

> If you’re reading this as a CTO/CEO:  
> Ping me — I can walk you through the invariants in 5 minutes.
`

---

