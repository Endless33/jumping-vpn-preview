# Security Review Checklist — Jumping VPN

This checklist defines the minimum areas that must be reviewed
before any production claim is made.

It is intended for:

- Internal engineering review
- External security auditors
- Partner evaluation teams

This is not a marketing document.
It is a review contract.

---

## 1. Control-Plane Safety

### 1.1 State Machine Integrity

- [ ] All state transitions are explicit
- [ ] No implicit state mutation paths exist
- [ ] No silent session reset paths exist
- [ ] State version is strictly monotonic
- [ ] Stale state updates are rejected

### 1.2 Deterministic Failure Handling

- [ ] Ambiguous ownership → reject or terminate
- [ ] TTL expiration → deterministic termination
- [ ] Transport-loss TTL enforced
- [ ] Recovery window bounded by policy
- [ ] No infinite retry loops possible

---

## 2. Replay & Freshness Protection

- [ ] Monotonic client nonce enforced
- [ ] Replay window bounded
- [ ] Nonce reuse rejected deterministically
- [ ] Freshness validated before transport binding
- [ ] Reattach proof cryptographically bound to session
- [ ] Anti-replay data structures bounded in memory

Preview-only logic must not be mistaken for production crypto.

---

## 3. Dual Binding Prevention

- [ ] Single active transport invariant enforced
- [ ] No race condition allows dual-active state
- [ ] Versioned ownership prevents rollback
- [ ] Split-brain scenario tested
- [ ] CAS / atomic update verified (cluster mode)

Zero tolerance for dual identity binding.

---

## 4. Rate Limiting & Abuse Protection

- [ ] Reattach rate limit per session
- [ ] Global control-plane rate limit
- [ ] Cooldown enforcement
- [ ] DoS attempt simulation performed
- [ ] No unbounded memory growth under flood
- [ ] Retry-after semantics deterministic

Control-plane must not amplify attack surface.

---

## 5. Cryptographic Guarantees (Production Requirement)

- [ ] Authenticated encryption (AEAD)
- [ ] Forward secrecy
- [ ] Rekey strategy defined
- [ ] Downgrade attack resistance
- [ ] Key lifecycle documented
- [ ] Key rotation under transport change defined
- [ ] Cryptographic audit completed

Preview repository does not fulfill this section.

---

## 6. Data Plane Boundaries

- [ ] Clear separation of control-plane vs data-plane
- [ ] No control-plane decision depends on packet payload
- [ ] Packet framing validated
- [ ] No parsing ambiguity in control messages
- [ ] Reject malformed control messages deterministically

---

## 7. Observability Safety

- [ ] Logging is non-blocking
- [ ] Logging failure does not affect session correctness
- [ ] State transitions logged before external emission
- [ ] Sensitive material never logged in plaintext
- [ ] Audit events structured and reason-coded

---

## 8. Memory & Resource Safety

- [ ] Session store bounded
- [ ] Replay window bounded
- [ ] Rate limiter memory bounded
- [ ] No unbounded candidate transport growth
- [ ] Expired sessions evicted deterministically
- [ ] No memory leak under churn test

---

## 9. Failure Injection Coverage

Tested scenarios:

- [ ] Packet loss spike
- [ ] NAT rebinding
- [ ] Path oscillation
- [ ] Reattach flood
- [ ] Split-brain attempt
- [ ] Node crash during reattach
- [ ] TTL expiration under load

All failures must produce explicit transitions.

---

## 10. Policy Safety

- [ ] Policy parameters documented
- [ ] Safe defaults defined
- [ ] MaxSwitchesPerMinute bounded
- [ ] Recovery window bounded
- [ ] Policy misconfiguration fails closed

---

## 11. Threat Model Alignment

- [ ] On-path attacker assumption validated
- [ ] Disruption does not imply identity takeover
- [ ] Replay does not mutate state
- [ ] Ownership ambiguity cannot escalate privilege
- [ ] Control-plane cannot be used for amplification

---

## 12. Non-Goals Confirmed

Reviewers must confirm that the system does NOT claim:

- Anonymity guarantees
- Censorship bypass guarantees
- Endpoint compromise protection
- Traffic obfuscation guarantees
- Kernel-level invisibility

Claims must match documented scope.

---

## 13. Review Sign-Off

Before production release:

- [ ] Internal engineering sign-off
- [ ] External security review completed
- [ ] Benchmark evidence recorded
- [ ] No open critical vulnerabilities
- [ ] Documentation consistent with implementation

Production claims without completed checklist
must be considered invalid.

---

## Final Principle

Security is not a feature.
It is a constraint.

If a guarantee cannot be upheld,
the session must terminate explicitly.

Session is the anchor.  
Transport is volatile.