Prototype — Jumping VPN Live Session Continuity Demonstration

This directory contains a minimal live prototype demonstrating the core architectural principle of Jumping VPN:

Session-anchored identity with transport-volatile attachments.

This prototype is not a production VPN.
It is a behavioral and architectural validation tool.

It demonstrates that a session can survive transport changes without identity reset or renegotiation.

---

Purpose

The prototype proves the following properties:

• Session identity is independent of transport
• Transport paths can change dynamically
• Session continuity is preserved across path switches
• Deterministic trace can be generated and validated
• Transport volatility does not break cryptographic continuity model

This is the foundation of the Jumping VPN architecture.

---

Components

This directory contains the following modules:

client.py
Client simulator that attaches to server, generates session traffic, and performs transport switches.

server.py
Server simulator that accepts transport attachments and maintains session continuity.

session_manager.py
Session identity manager. Tracks session state independent of transport.

transport_layer.py
Transport abstraction layer. Allows transport attachment and detachment without affecting session identity.

---

Architecture Model

Jumping VPN separates identity from transport.

Traditional model:

identity → transport → socket → IP

Jumping VPN model:

identity → session anchor → transport attachment → socket → IP

Transport becomes replaceable.

Session remains persistent.

---

Behavioral Flow

Typical prototype execution:

1. Session is created
2. Client attaches via transport A
3. Traffic flows normally
4. Transport degradation occurs
5. Client switches to transport B
6. Session continues without reset
7. Continuity is preserved

This behavior is recorded in a deterministic trace file.

---

Running the Prototype

From the repository root directory:

python live_demo.py

This will:

• start the prototype server
• start the prototype client
• simulate transport volatility
• perform transport switch
• generate a deterministic trace

Output file:

DEMO_TRACE.jsonl

---

Trace Validation

To validate continuity:

python demo_engine/replay.py DEMO_TRACE.jsonl

Expected output:

SESSION_CREATED OK
VOLATILITY_SIGNAL OK
TRANSPORT_SWITCH OK
STATE_CHANGE OK
RECOVERY_COMPLETE OK

Trace validated successfully.
Session continuity preserved.

---

What This Prototype Is

This prototype is:

• architectural proof
• behavioral model
• deterministic simulation
• protocol continuity validation tool

---

What This Prototype Is Not

This prototype is not:

• production VPN
• encrypted tunnel
• anonymity tool
• privacy product

It is an architectural validation layer.

Cryptographic integration is part of future phases.

---

Core Principle

Session is the anchor.

Transport is volatile.

Transport can change.
Identity cannot break.

---

Future Evolution

Next stages include:

• real encrypted transport layer
• authenticated session anchors
• key schedule integration
• replay protection enforcement
• production transport abstraction

---

Relationship to Jumping VPN

This prototype demonstrates the behavioral core of Jumping VPN.

The full protocol extends this model with:

• cryptographic binding
• forward-only key schedule
• authenticated session continuity
• replay protection
• adaptive transport selection

---

Final Note

This prototype exists to prove one architectural fact:

Session continuity can survive transport volatility.

This is the foundation of Jumping VPN.