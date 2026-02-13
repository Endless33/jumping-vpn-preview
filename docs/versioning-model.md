# Versioning Model — Jumping VPN

Status: Formal Preview  
Scope: State mutation safety and deterministic progression  

This document defines the versioning semantics used to guarantee
deterministic state evolution under transport volatility.

Versioning is the backbone of correctness.

---

# 1. Design Goal

The versioning model must guarantee:

- No state rollback
- No concurrent mutation ambiguity
- No stale reattach acceptance
- Deterministic ordering of transitions
- Protection against race conditions

If versioning fails, session correctness fails.

---

# 2. State Version Definition

Each session maintains:

- state_version (monotonic integer)

Rules:

- Initialized at 0 during BIRTH
- Incremented on every successful state transition
- Never decremented
- Never reused

Example:

BIRTH              → state_version = 0  
ATTACHED           → state_version = 1  
RECOVERING         → state_version = 2  
ATTACHED           → state_version = 3  
TERMINATED         → state_version = 4  

---

# 3. Version Increment Rules

A state_version MUST increment when:

- Session state changes
- Transport binding changes
- Reattach is accepted
- Termination occurs
- Policy forces explicit state transition

A state_version MUST NOT increment when:

- Telemetry event is emitted
- Transport health signal observed (without transition)
- Logging fails
- Observability export succeeds/fails

Version increments reflect state mutation only.

---

# 4. CAS Requirement (Compare-And-Set)

Server-side session store MUST enforce atomic mutation.

Pseudo-rule:

If incoming.state_version != current.state_version  
→ Reject as stale

If CAS(current.state_version, new_state_version) fails  
→ Reject as concurrent mutation

This prevents:

- Dual reattach race
- Split-brain mutation
- State rollback

---

# 5. Client Version Semantics

Client MUST:

- Track latest acknowledged state_version
- Include state_version in REATTACH_REQUEST
- Reject server responses with lower version
- Reject unexpected version jumps

Client must fail closed on ambiguity.

---

# 6. Stale Message Handling

If server receives:

- REATTACH_REQUEST with outdated state_version
- Duplicate message with same nonce
- Message referencing old transport

Then:

- Explicitly reject with reason_code
- Emit SECURITY_EVENT or POLICY_EVENT
- Do not mutate session

Silent ignore is forbidden.

---

# 7. Clustered Deployment Semantics

In multi-node deployments:

Authoritative ownership required:

Option A:
Sticky routing (SessionID → node)

Option B:
Shared atomic session store (versioned)

Version must be globally consistent across nodes.

If ownership ambiguity detected:
→ Reject reattach

Consistency preferred over availability.

---

# 8. Version Wrap-Around Policy

state_version MUST be sufficiently large (e.g., 64-bit).

Wrap-around is forbidden within session lifetime.

If overflow risk detected:
→ Force deterministic TERMINATION

No modulo behavior allowed.

---

# 9. Safety Invariants

For any session S:

1) state_version strictly increases  
2) No two states share same version  
3) Every version corresponds to exactly one state  
4) No accepted message can reduce version  
5) Concurrent accepted mutations are impossible  

---

# 10. Version Drift Protection

Client and server must detect:

- Unexpected version gaps
- Version rollback attempts
- Replay with old version
- Mismatched state_version in ACK

Ambiguity must result in rejection.

---

# 11. Observability Coupling

Every version increment MUST produce:

- STATE_CHANGE event
- Logged state_version value

If version increments without audit event:
Observability contract is violated.

---

# 12. Determinism Guarantee

Given:

- Same initial state
- Same input message
- Same state_version

The output state and new version MUST be identical.

Non-deterministic mutation is forbidden.

---

# 13. Security Rationale

Versioning prevents:

- Replay hijack
- Dual-active binding
- Concurrent transport takeover
- Split-brain acceptance
- State regression

It is a structural defense mechanism.

---

# 14. Formal Principle

State progression must form a strict total order:

S0 < S1 < S2 < S3 < ... < Sn

No branching.
No rollback.
No hidden transitions.

---

# Final Principle

If two nodes disagree on state_version,
the session must not continue.

Correctness is version-bound.

Session is the anchor.  
Transport is volatile.  
Version is the spine of determinism.