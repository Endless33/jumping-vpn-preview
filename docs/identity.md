# Session Identity Architecture

This document outlines how Jumping VPN defines, maintains, and verifies session identity — independent of transport volatility or network instability.

---

## 🧬 Identity as a Session Spine

Jumping VPN treats identity not as a property of a transport, but as a **persistent cryptographic spine** that survives across:

- Transport switches  
- NAT rebinding  
- Path drift  
- Packet loss and reordering  
- Replay attempts  
- Adversarial injection

---

## 🔐 Core Identity Components

- **Session ID**: A stable, cryptographically derived identifier anchored at session initiation  
- **Monotonic Counters**: Strictly increasing counters for message sequencing and replay rejection  
- **Key Material**: Derived once per session; not renegotiated on transport change  
- **Lineage Chain**: Signed events that record transport transitions and validate continuity  
- **Behavioral Envelope**: Timing, jitter, and pacing profiles that reinforce session authenticity

---

## 🔄 Identity Continuity Across Transports

When a transport switch occurs:

- The session ID remains unchanged  
- No renegotiation or re-authentication is triggered  
- The new transport is accepted only if:
  - It presents a valid lineage signature  
  - It continues the monotonic counter  
  - It matches behavioral expectations

---

## 🧱 Replay & Injection Resistance

- Old transports are rejected via counter mismatch  
- Replayed packets are discarded deterministically  
- Injection attempts fail due to:
  - Counter discontinuity  
  - Invalid lineage  
  - Behavioral anomalies

---

## 🧭 Observability & Auditing

- All identity-relevant events are signed and logged  
- Lineage transitions are verifiable by both peers  
- Session continuity can be externally audited without decrypting payloads

---

## 🧠 Why This Matters

Traditional VPNs bind identity to a socket or IP tuple.  
Jumping VPN binds identity to a **cryptographic session spine** — enabling:

- Seamless roaming  
- Stateless recovery  
- Transport-agnostic continuity  
- Resistance to replay, hijack, and drift

---

## 📌 Related Documents

- [`trace-analysis.md`](trace-analysis.md) — Demonstrates continuity under transport loss  
- [`MutationLogIndex.md`](MutationLogIndex.md) — Evolution of identity handling  
- [`clone-spike.md`](clone-spike.md) — Interest surge following identity trace publication