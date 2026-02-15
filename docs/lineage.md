# Signed Lineage Events

This document describes the lineage mechanism used in Jumping VPN to ensure session continuity across transport mutations.

---

## 🧬 What Is Lineage?

Lineage is a **signed, verifiable chain of transport transitions** that preserves session identity across:

- Transport switches  
- NAT rebinding  
- Path drift  
- Failover and recovery  
- Adversarial replay or injection attempts

Each lineage event is a **cryptographically signed statement** that encodes:

- Previous transport fingerprint  
- New transport fingerprint  
- Session ID  
- Monotonic counter state  
- Reason code (e.g., VOLATILITY, REATTACH, REBIND)  
- Timestamp  
- Signature (HMAC or digital signature)

---

## 🔐 Why Lineage Matters

Lineage enables:

- **Continuity without renegotiation**  
- **Replay resistance across transports**  
- **Auditability of session evolution**  
- **Proof of legitimate transport switch**  
- **Rejection of stale or injected transports**

---

## 🧪 Example Lineage Event (Simplified)

```json
{
  "session_id": "0xA1B2C3D4",
  "from_transport": "udp://192.168.1.10:51820",
  "to_transport": "udp://10.0.0.5:51820",
  "reason": "VOLATILITY",
  "counter": 98234,
  "timestamp": 1834567890,
  "signature": "0xdeadbeef..."
}