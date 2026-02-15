# 🧬 Jumping VPN — Architectural Preview

Jumping VPN is a session-centric VPN architecture built for environments where transport volatility is the norm, not the exception.

Traditional VPNs bind identity to a single transport.  
Jumping VPN binds identity to a persistent session, while transports remain replaceable, volatile attachments.

---

# 🚀 Quick Demo Run

Requirements: Python 3.10+

Run:

python run_demo.py

Expected output:

[Jumping VPN] Starting deterministic demo...
Trace validated successfully. Session continuity preserved.
Output written: DEMO_OUTPUT.jsonl

Generated files:

DEMO_OUTPUT.jsonl  
DEMO_ECOSYSTEM/  
DEMO_PACKAGE.zip  

---

# 📚 Documentation

Session Identity Architecture  
docs/identity.md  

Trace Analysis  
docs/trace-analysis.md  

Audience Analysis  
docs/audience.md  

Clone Spike Analysis  
docs/clone-spike.md  

Mutation Log Index  
docs/MutationLogIndex.md  

---

# 🎥 Demo Trace Validator

Trace file:

DEMO_TRACE.jsonl

Validator:

demo_engine/replay.py

Run validator:

python demo_engine/replay.py DEMO_TRACE.jsonl

---

# 🧠 Core Thesis

Modern networks are inherently unstable.

Mobile networks flap.  
Routes degrade.  
Paths die.

Traditional VPNs fail.

Jumping VPN adapts.

Session is the anchor.  
Transport is volatile.

---

# 🧬 Architectural Model

Session identity persists.  
Transport is replaceable.

Transport failure does not terminate session identity.

All transitions are:

Explicit  
Auditable  
Deterministic  

---

# 🌐 Prototype

See prototype implementation:

poc/realudpprototype.py  

Documentation:

poc/README_udp.md  

---

# 📂 Repository Structure

docs/  
demo_engine/  
core/  
poc/  
run_demo.py  

---

# 📈 Status

Architectural validation stage.

Not production ready.

Protocol behavior is stable.  
Implementation is evolving.

---

# 🤝 Contact

Email:

riabovasvitalijus@gmail.com

---

# Final Principle

Session remains.

Transport changes.