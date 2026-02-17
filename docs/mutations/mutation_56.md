# 🧬 Mutation_56.md — The Refusal to Die

**Date:** 2026-02-18  
**Status:** Draft  
**Author:** Vitalijus Riabovas  
**Category:** Behavioral Invariant  
**Scope:** Session Continuity under Transport Death

---

## 🧠 Summary

This mutation formalizes a core behavioral invariant:

> **A session must not die when its transport dies.**

Jumping VPN treats transport death not as failure — but as a **mutation event**.  
The session persists. The transport is replaced. The lineage is signed.

---

## 🔄 Before

In traditional VPNs:

- Session identity is bound to a specific transport (e.g., TCP socket, UDP 5-tuple)
- Transport death = session death
- Recovery requires renegotiation, re-authentication, or full reset

This leads to:

- Fragile mobile experiences  
- Session collapse under NAT rebinding  
- Unobservable resets  
- Replay vulnerabilities

---

## 🔁 After

With this mutation:

- Session identity is anchored in a cryptographic spine  
- Transport is a volatile, replaceable attachment  
- On transport death:
  - Session enters `VOLATILE` state  
  - A new transport is attached  
  - A signed `TransportSwitch` lineage event is emitted  
  - Session returns to `ATTACHED` without identity reset

---

## 🔐 Invariants Introduced

- **Session continuity is independent of transport continuity**  
- **All transport switches are signed and auditable**  
- **No implicit resets are allowed**  
- **Replay attempts on dead transports are rejected**

---

## 📊 Trace Example

```json
{
  "event": "TransportSwitch",
  "session_id": "0xA7F3...",
  "from_transport": "udp://192.168.1.4:51820",
  "to_transport": "udp://10.0.0.5:51820",
  "reason": "NAT_REBIND_DETECTED",
  "timestamp": 2026-02-18T10:42:13.812Z,
  "signature": "ed25519:..."
}
`

---

📈 Observed Effects

- Session continuity preserved across 3 transport deaths  
- No renegotiation triggered  
- Behavioral trace remained deterministic  
- Replay attempts on dead transports rejected with REPLAYWINDOWEXCEEDED

---

🧪 Demo Validation

Validated in:

- DEMO_SCENARIO.md  
- DEMO_TIMELINE.jsonl  
- demo_engine/replay.py

Trace hash: 0x56c9...deadbeef

---

🧭 Commentary

This mutation is not a feature.  
It is a refusal — to accept that volatility must mean collapse.

Jumping VPN does not restart.  
It mutates.  
It survives.

> “The session is not what dies.  
> The session is what survives the dying.”

---

🔜 Next

- spec/session-continuity.md  
- lineage.md  
- Mutation_57.md — Behavioral Anchoring under Multipath Drift
`

---