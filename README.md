# 🧬 Jumping VPN — Architectural Preview

Jumping VPN is a **session-centric VPN architecture** built for environments where **transport volatility is the norm, not the exception**.

Traditional VPNs bind identity to a single transport.  
Jumping VPN binds identity to a **persistent session**, while transports remain **replaceable, volatile attachments**.

---

## 🚀 Quick Demo Run (1 command)

**Requirements:** Python 3.10+

```bash
python run_demo.py

Expected output (example):

[Jumping VPN] Starting deterministic demo...
Trace validated successfully. Session continuity preserved.
Output written: DEMO_OUTPUT.jsonl

Outputs:

DEMO_OUTPUT.jsonl (generated trace in repo root)

DEMO_ECOSYSTEM/

DEMO_PACKAGE.zip

---

🎥 Demo Trace Validator

Trace file: DEMO_TRACE.jsonl

Validator: demo_engine/replay.py

Run:

python demo_engine/replay.py DEMO_TRACE.jsonl

---

📚 Documentation (clickable)

Session Identity Architecture

Trace Analysis: Deterministic Session Continuity

Audience Analysis

Clone Spike: February 2026

Mutation Log Index

---

🧭 Who’s Watching

Jumping VPN is attracting attention from:

VPN engineers (OpenVPN, Nord Security)

Cybersecurity professionals (Fortinet, Sonar, JayDevs)

FinTech & Infrastructure (Revolut, LMAX Group, Credo Bank)

Privacy-focused builders

Government & Healthcare

Geographic clusters: Zürich, Vilnius, London, Berlin, Singapore, Toronto

📊 See: Audience Analysis

---

🧠 Core Thesis

Modern networks are inherently unstable:

Mobile networks flap

NAT mappings expire

Cross-border routes degrade

Packet loss spikes

Paths die unpredictably

Most VPNs treat this as failure.

Jumping VPN treats it as modeled behavior.

Transport death ≠ session death (within bounded policy).

---

🧬 Architectural Model

Session-Centric Identity

Session is the source of truth

Identity belongs to the session

Transport is an attachment

Reattachment preserves continuity

Deterministic Recovery

Transport failover is:

Explicit

Reason-coded

Rate-limited

Policy-bounded

Auditable

No silent renegotiation.

No uncontrolled resets.

Volatility as State

Instability is represented explicitly:

BIRTH

ATTACHED

VOLATILE

DEGRADED

REATTACHING

RECOVERING

TERMINATED

Transitions are deterministic and logged.

---

🌐 Real UDP Prototype (Behavioral Validation)

A minimal UDP prototype demonstrates:

Session creation

Transport death

Explicit reattach

Continuity without identity reset

See:

poc/realudpprototype.py

poc/README_udp.md

Behavioral validation, not production cryptography.

---

🛡 Threat Model & Boundaries

Recommended reading:

docs/core/threat-model.md

docs/core/security-boundary.md

docs/core/invariants.md

docs/core/state-machine.md

---

🚫 Explicit Non-Goals

Jumping VPN does not aim to provide:

Anonymity

Censorship bypass

Endpoint compromise protection

Anti-forensics

Universal VPN replacement

Scope is intentionally narrow:
Session continuity under transport volatility.

---

🔬 Status

Jumping VPN is in architectural validation.

This repository:

Is not production-ready

Does not include hardened cryptography

Focuses on behavioral modeling

---

🤝 Technical Discussions

Email:
riabovasvitalijus@gmail.com

---

Final Principle

Transport instability is not an anomaly — it is the default condition of modern networks.

Session remains the anchor.
Transports come and go.