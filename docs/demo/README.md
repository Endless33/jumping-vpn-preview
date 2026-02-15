# Jumping VPN — Deterministic Demo Package

This directory defines and documents the deterministic demo trace for Jumping VPN.

The purpose of this demo is to prove a single architectural property:

**Session continuity independent of transport stability.**

Transport may degrade, fail, or switch.  
Session identity remains intact.

---

# What this demo proves

The demo demonstrates that Jumping VPN:

• preserves session identity across transport switches  
• does not renegotiate identity during transport failure  
• maintains deterministic state transitions  
• enforces cryptographic continuity at the session layer  
• prevents ambiguous or dual-active transport binding  

This is the core property of session-anchored transport abstraction.

---

# Demo trace file

Primary demo artifact:

DEMO_TRACE.jsonl

Location:

repo root / DEMO_TRACE.jsonl

Format:

JSONL (one event per line)

Each event represents a deterministic state transition or protocol decision.

Example:

```json
{"ts_ms":1700000000810,"event":"STATE_CHANGE","from":"ATTACHED","to":"VOLATILE"}
{"ts_ms":1700000001100,"event":"TRANSPORT_SWITCH","from_path":"udp:A","to_path":"udp:B"}
{"ts_ms":1700000001810,"event":"STATE_CHANGE","from":"RECOVERING","to":"ATTACHED"}

Expected behavioral phases
The demo contains four deterministic phases:
Phase 1 — Stable attachment
Session established
Transport attached
Normal operation
State:

ATTACHED

Phase 2 — Transport degradation
Transport becomes unstable:
• packet loss spike
• jitter increase
• latency increase
State transition:

ATTACHED → VOLATILE

Phase 3 — Transport switch
Protocol selects better transport candidate.
Transport binding switches.
Session identity remains unchanged.
State transition:

VOLATILE → RECOVERING

Phase 4 — Recovery complete
Transport stabilizes.
Session returns to stable state.
State transition:

RECOVERING → ATTACHED

Critical invariants validated by demo
The demo must never show:
• session reset
• identity renegotiation
• ambiguous ownership
• dual-active transport binding
The demo must show:
• explicit transport switch
• explicit recovery
• deterministic state transitions
Verification
Verification script:

demo_engine/continuity_verifier.py

Run locally:

python demo_engine/continuity_verifier.py DEMO_TRACE.jsonl

Expected output:

PASS: continuity preserved
PASS: no identity reset
PASS: deterministic recovery verified

What this demo is NOT
This demo is not:
• a production VPN client
• a full cryptographic implementation
• a network tunnel
This demo validates behavioral correctness of the protocol model.
What this demo IS
This demo is:
• deterministic protocol trace
• architectural proof artifact
• engineering review material
• session continuity validation
Why this matters
Traditional VPN systems bind identity to transport.
Jumping VPN binds identity to session.
This allows transport mobility without breaking identity continuity.
This property is critical for:
• mobile environments
• volatile networks
• NAT rebinding scenarios
• adaptive routing systems
Engineering interpretation
This demo proves the existence of a deterministic session-anchored transport model.
Transport becomes a replaceable attachment.
Session remains the identity anchor.
Final principle
Session is the anchor.
Transport is volatile.

