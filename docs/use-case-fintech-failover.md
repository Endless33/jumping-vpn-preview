# Use Case — Fintech Failover Under Packet Loss (Session Collapse Scenario)

## Context

A European fintech platform experiences session collapse during transport failover under packet loss spikes.

This is common in:
- mobile users (Wi-Fi ↔ LTE)
- cross-border routing changes
- NAT rebinding and carrier-grade NAT timeouts
- congestion events that cause transient loss/jitter

## Observed Problem (Traditional VPN Behavior)

During a failover event:
- active transport degrades (loss/jitter spikes)
- tunnel becomes unstable
- the VPN treats the failure as fatal or semi-fatal

Typical outcome:
1) Transport degrades → tunnel stalls  
2) VPN renegotiates or resets  
3) Session drops  
4) Users re-authenticate / re-establish identity  
5) Application-level sessions may be disrupted  

Operational impact:
- user experience breaks
- auth churn increases
- incident response is noisy
- monitoring sees repeated reconnect loops

## Jumping VPN Model (Session-Centric Behavior)

Jumping VPN separates:
- **Session identity** (persistent)
- **Transport binding** (replaceable)

Transport volatility is treated as an expected state.

### Expected behavior under the same event

1) Transport degrades → session enters `VOLATILE`
2) Policy thresholds are evaluated (loss, jitter, stability score)
3) If thresholds exceeded → explicit transition to `RECOVERING`
4) A new transport is attached using session-bound validation
5) Session returns to `ATTACHED`
6) All decisions are logged and reason-coded

Key outcome:
- No session reset
- No identity loss
- No silent renegotiation
- Recovery is deterministic and auditable

## Why This Matters for Fintech

Fintech systems have:
- strict uptime expectations
- authentication and compliance requirements
- cross-border user mobility
- high cost of session churn

A bounded, auditable recovery model reduces:
- downtime
- re-auth events
- incident noise
- operational unpredictability

## How This Repository Supports the Use Case

Relevant docs:
- `docs/state-machine.md` — allowed transitions and invariants
- `docs/threat-model.md` — assumptions and adversary model
- `docs/test-scenarios.md` — packet loss spike and transport death scenarios
- `poc/` — behavioral proof that session can survive transport death (concept)
- `poc/real_udp_prototype.py` — minimal real UDP reattach prototype (no production crypto)

## Summary

This use case highlights the architectural difference:

Traditional VPNs often bind identity to transport.
Jumping VPN binds identity to session and treats transport as disposable.

Session remains the anchor.
Transports come and go.