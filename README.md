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

- VPN engineers (OpenVPN, Nord Security)  
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