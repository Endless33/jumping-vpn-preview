# Multi-Hop Behavior Model — Deterministic Constraints (Preview)

This document defines how multi-hop transport chains are treated
within the Jumping VPN behavioral model.

Multi-hop is possible.

But only under strict invariants.

---

# 1. Problem Statement

Traditional multi-hop VPN chains introduce:

- Multiple active relays
- Potential dual identity exposure
- Ambiguous session ownership
- Increased failover complexity
- Non-deterministic propagation

Jumping VPN does not reject multi-hop.

It constrains it.

---

# 2. Core Principle

Multi-hop must not violate:

- Single session identity anchor
- Single active binding invariant
- Deterministic recovery bounds
- Auditable transition rules

If multi-hop introduces ambiguity,
it is rejected by policy.

---

# 3. Multi-Hop as Transport Composition

In Jumping VPN:

Multi-hop is treated as a composed transport.

Example:

Client → Relay A → Relay B → Gateway

This entire chain is considered:

ONE active transport binding.

The session does not bind to intermediate relays individually.

It binds to a logical transport endpoint.

---

# 4. Identity Ownership Rule

Session identity must remain:

- Single-owner
- Single-active
- Versioned

Even in multi-hop:

- Only one gateway node can be authoritative
- Intermediate relays are stateless forwarders
- Relays cannot mutate session state

Session state lives only at the ownership layer.

---

# 5. Multi-Hop Failover Semantics

Failure cases:

## Case A — Relay Failure (internal hop)

If intermediate relay fails:

- Transport declared DEAD
- Session enters RECOVERING
- Full chain re-evaluated
- Reattach performed

No partial mutation allowed.

---

## Case B — Gateway Failure

If gateway unreachable:

- Reattach must target authoritative owner
- Ownership ambiguity must be rejected
- Dual-active binding forbidden

---

## Case C — Path Degradation

If multi-hop chain degrades:

- Session may enter VOLATILE or DEGRADED
- Candidate chain selection evaluated
- Switch bounded by policy

No automatic cascading propagation.

---

# 6. Deterministic Chain Selection

Multi-hop candidate evaluation must be:

- Deterministic
- Policy-driven
- Bounded in complexity

Allowed factors:

- Measured latency
- Packet loss
- Stability window
- Geographic constraints (optional)
- Operator policy

Not allowed:

- Heuristic guess loops
- Unbounded re-evaluation
- Implicit cascading

---

# 7. Dual-Active Prevention

Multi-hop increases risk of:

- Two chains active simultaneously
- Two gateways believing ownership
- Split-brain identity continuation

Mitigation:

- Strict version matching
- Ownership validation before binding
- Atomic session store (if clustered)
- Sticky routing when possible

If ambiguity detected:

REJECT or TERMINATE.

Never allow dual identity.

---

# 8. Anti-Flap Considerations

Multi-hop environments amplify instability.

Therefore:

- Switch rate must remain bounded
- Cooldown windows enforced
- Recovery windows enforced
- Chain churn must not exceed policy

If churn persists beyond threshold:

Session enters DEGRADED or TERMINATED.

Scalability must not collapse due to chain instability.

---

# 9. Observability Requirements

Multi-hop must emit:

- Chain selection event
- Switch reason
- Degradation signal
- Recovery latency
- Rejection reason

Operators must see:

- Why chain changed
- Which invariant was enforced
- Whether bounded policy triggered

Opaque multi-hop behavior is forbidden.

---

# 10. Security Considerations

Multi-hop increases:

- Replay attack surface
- Relay impersonation risk
- Route poisoning vectors
- Amplified DoS surface

Therefore:

- Reattach always validated at gateway
- Intermediate relays never trusted for identity mutation
- Freshness validation required
- Rate limits applied at entry point

Multi-hop must not weaken identity binding.

---

# 11. Non-Goals

This document does NOT claim:

- Onion-routing anonymity
- Traffic obfuscation
- Relay secrecy guarantees
- Resistance against global adversary

Multi-hop here is transport composition,
not anonymity layer.

---

# 12. When Multi-Hop Should Be Disabled

Policy may forbid multi-hop if:

- Regulatory constraints apply
- Deterministic recovery budget too tight
- Operational complexity unacceptable
- Latency budget exceeded

Multi-hop is optional.
Session determinism is mandatory.

---

# 13. Behavioral Guarantee

If multi-hop can preserve:

- Single identity anchor
- Single active binding
- Deterministic version progression
- Bounded recovery

Then it is allowed.

If it cannot —

It must be rejected by design.

---

# Final Principle

Multi-hop is a transport detail.

Session identity is the invariant.

Transport may grow complex.

Identity must remain simple.

Session is the anchor.  
Transport — single or chained — remains volatile.