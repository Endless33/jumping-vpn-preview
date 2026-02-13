# Integration Guide — Jumping VPN (Preview)

This document describes how external systems may integrate
with a Jumping VPN deployment.

This is a behavioral integration guide,
not a production networking manual.

---

## 1. Integration Philosophy

Jumping VPN separates:

- Session identity (persistent anchor)
- Transport binding (replaceable)
- Observability (non-blocking)

External systems must integrate at the **control-plane boundary**,
not by inspecting data-plane packets.

Integration must not violate core invariants:

- No dual-active binding
- No silent state transitions
- No implicit recovery
- No ownership ambiguity

---

## 2. Integration Layers

### 2.1 Client-Side Integration

Use cases:

- Mobile apps
- Enterprise VPN clients
- SDK consumers

Client responsibilities:

- Maintain session context
- Trigger REATTACH_REQUEST on transport death
- Respect cooldown and rate limits
- Track state_version
- Enforce freshness

Client must not:

- Reset identity implicitly
- Retry infinitely
- Ignore policy limits

---

### 2.2 Server / Edge Integration

Deployment options:

- Single-node gateway
- Sticky routing cluster
- Shared atomic session store cluster

Requirements:

- Authoritative session ownership
- CAS/versioned updates
- Bounded replay tracking
- Deterministic rejection on ambiguity
- Structured event logging

Cluster deployments must define:

- Ownership model
- Reattach authority rule
- Split-brain prevention strategy

---

### 2.3 Observability Integration

External systems (SIEM, NOC, dashboards)
may subscribe to structured events:

Example event types:

- SESSION_CREATED
- STATE_CHANGE
- TRANSPORT_SWITCH
- REATTACH_SUCCESS
- REATTACH_REJECT
- SECURITY_EVENT
- RATE_LIMIT_TRIGGER

Event structure must follow the control-plane contract.

Observability must be:

- Non-blocking
- Structured
- Reason-coded
- Deterministic

Logging failures must not affect correctness.

---

## 3. Control-Plane Message Integration

All integrations must respect:

- Monotonic state_version
- Deterministic rejection rules
- Replay protection semantics
- TTL enforcement
- Single active transport invariant

Message envelope format defined in:

docs/control-plane-protocol.md

Integrators must not mutate state
outside defined message flows.

---

## 4. Transport Integration Model

Jumping VPN is transport-agnostic.

Possible transport adapters:

- UDP
- TCP
- QUIC
- Future custom transport layers

Integration rules:

- Only one ACTIVE transport at a time
- Candidate transports may compete
- Switching must be bounded
- Cooldown must be enforced

Multi-hop transport chains must preserve:

- Single session anchor
- Deterministic ownership
- Explicit switch semantics

---

## 5. Failure Handling Integration

External systems must expect:

- VOLATILE state during instability
- DEGRADED state under bounded instability
- TERMINATED state when policy limits exceeded

Recovery must be:

- Explicit
- Reason-coded
- Logged
- Versioned

No implicit state downgrades allowed.

---

## 6. Integration Safety Checklist

Before deploying:

- [ ] Session TTL defined
- [ ] Transport-loss TTL defined
- [ ] MaxSwitchesPerMinute configured
- [ ] Replay window size configured
- [ ] Ownership model documented
- [ ] Rate limiter configured
- [ ] Logging pipeline tested
- [ ] Failure injection tested

---

## 7. Pilot Integration Path

Recommended evaluation path:

1. Deploy single-node reference
2. Run controlled failover tests
3. Validate invariants
4. Enable observability export
5. Stress-test recovery bounds
6. Document evidence
7. Expand to cluster model

No production deployment
without evidence log entries.

---

## 8. Non-Goals for Integrators

This integration layer does NOT:

- Provide anonymity guarantees
- Replace Tor
- Guarantee censorship bypass
- Hide endpoint compromise
- Provide stealth networking

Scope is strictly:

Deterministic session continuity under transport volatility.

---

## 9. Review Expectations

Engineers evaluating integration should verify:

- Clear control-plane boundaries
- No hidden state transitions
- No identity reset shortcuts
- No unsafe fallback logic
- Clear audit trail

Ambiguity must result in rejection or termination.

---

## Final Principle

Integration must preserve behavioral determinism.

If correctness cannot be maintained,
the session must terminate explicitly.

Session is the anchor.  
Transport is volatile.