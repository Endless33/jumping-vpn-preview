# Jumping VPN — Comparison Model (Conceptual)

This document outlines architectural differences between
traditional VPN models and the Jumping VPN session-centric model.

This is not a performance comparison.
It is a behavioral model comparison.

---

## 1) Identity Binding Model

### Traditional Model (Transport-Bound)

In many VPN implementations:

- Identity and session are tightly coupled to the transport tunnel.
- When the tunnel fails, renegotiation may occur.
- Session continuity often depends on transport stability.

Transport instability can trigger:
- renegotiation
- session reset
- identity re-authentication

---

### Jumping VPN Model (Session-Centric)

In Jumping VPN:

- Identity belongs to the session.
- Transport is a replaceable binding.
- Reattachment is explicit and validated.

Transport instability is modeled as a state transition,
not as an implicit identity reset.

---

## 2) Volatility Handling

### Traditional Assumption

Many systems assume:

- stable network paths
- relatively consistent endpoints
- limited mobility

Volatility is treated as an exception.

---

### Jumping VPN Assumption

Jumping VPN assumes:

- transport paths fail
- IP addresses change
- packet loss spikes occur
- mobile networks flap

Volatility is treated as a normal operating condition.

---

## 3) Recovery Semantics

### Traditional Recovery

Recovery often involves:

- renegotiation
- tunnel rebuild
- possible session interruption

Behavior may be implementation-dependent.

---

### Jumping VPN Recovery

Recovery is:

- explicitly modeled in the state machine
- bounded by policy
- auditable
- reason-coded

Reattachment is deterministic, not heuristic.

---

## 4) Observability

### Traditional Approach

Some implementations prioritize simplicity
and may not expose detailed internal transitions.

---

### Jumping VPN Approach

Jumping VPN prioritizes:

- explicit `TransportSwitch` events
- deterministic session state transitions
- operator-grade auditability

Adaptation must be explainable.

---

## 5) Scope Differences

Jumping VPN does not attempt to:

- replace all VPN use cases
- outperform established protocols in raw throughput
- redefine cryptographic primitives

Its focus is:

**deterministic session continuity under transport volatility**

---

## Summary

This comparison is conceptual.

Traditional VPN designs often assume transport stability.

Jumping VPN assumes transport instability.

The difference lies not in cryptographic primitives,
but in how identity, recovery, and volatility are modeled.