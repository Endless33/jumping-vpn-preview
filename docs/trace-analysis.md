# Trace Analysis: Deterministic Session Continuity

This document analyzes a public demo trace of Jumping VPN, showcasing its core invariant: **session identity continuity under transport volatility**.

---

## 🧪 Scenario: Explicit Transport Switch Under Loss Spike

**Event:**  
At `t=12.4s`, the primary transport experiences a 37% packet loss spike.

**Reaction:**  
- Flow control detects volatility (cwnd drops from 12 to 4)
- Pacing adjusts to 60ms intervals
- Transport switch initiated at `t=12.6s`

**Result:**  
- No renegotiation triggered  
- Session identity preserved  
- Monotonic counters continue without reset  
- Peer accepts new transport as valid continuation

---

## 🔐 Invariant: Identity Anchored to Session, Not Transport

- Session ID remains stable across transport switch  
- Replay attempts on old transport rejected (counter mismatch)  
- No observable identity reset or key renegotiation

---

## 🧭 Observability

- State transitions are logged and auditable  
- Transport switch is visible as a signed lineage event  
- Behavioral envelope remains consistent (RTT, pacing, jitter profile)

---

## 📊 Suggested Next Steps

- Add `trace-visualization.png` to `docs/assets/` (optional)  
- Link this file from `README.md` or `MutationLogIndex.md`  
- Consider adding `trace-analysis/` folder for future traces

---

## 🧬 Conclusion

This trace demonstrates that Jumping VPN:

- Maintains **cryptographic continuity** across transport mutations  
- Detects and rejects **stale or replayed attachments**  
- Preserves a **verifiable narrative** of the session’s evolution