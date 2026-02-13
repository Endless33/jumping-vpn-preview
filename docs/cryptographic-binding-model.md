# Cryptographic Binding Model — Jumping VPN (Preview)

This document defines how session identity
is cryptographically bound to transport transitions.

It describes:

- Session key lifecycle
- Proof-of-possession model
- Reattach authentication
- Replay resistance
- Binding guarantees

This is a behavioral crypto model.
It does not define specific algorithms.

---

# 1. Design Goal

Guarantee:

Session identity cannot be hijacked,
duplicated, or mutated during transport volatility.

Transport may change.
Identity must remain cryptographically anchored.

---

# 2. Core Concepts

Let:

SessionID = stable logical identity
SessionKey = symmetric session secret
POP = proof-of-possession
Nonce = freshness marker
V = state_version

The session is defined by:

(SessionID, SessionKey, state_version)

---

# 3. Initial Handshake

During HANDSHAKE_INIT:

Client and server establish:

- SessionID
- SessionKey
- Initial state_version = 0

The SessionKey must:

- Be generated with sufficient entropy
- Be bound to SessionID
- Never be reused across sessions

---

# 4. Proof-of-Possession Model

Reattach requires:

POP = HMAC(SessionKey, (SessionID, Nonce, state_version))

Server verifies:

- Session exists
- Nonce freshness
- POP validity
- Version match

If any check fails → reject.

No partial acceptance allowed.

---

# 5. Replay Protection

Replay defense requires:

- Monotonic nonce (client-side)
- Sliding replay window (server-side)
- Rejection of stale nonce
- Rejection of reused nonce

Replay validation must occur:

Before state mutation.

Replay rejection must:

- Not increment state_version
- Not alter session state
- Emit security event

---

# 6. Transport Rebinding

When REATTACH_REQUEST validated:

Server performs:

1. Ownership validation
2. POP validation
3. Freshness validation
4. Version match check
5. Atomic state mutation

Then:

state_version++
active_transport = new_transport

Binding must be atomic.

---

# 7. Key Lifecycle

SessionKey lifecycle is bounded by:

- Session TTL
- Explicit rekey policy
- Policy-triggered rotation

Optional future extension:

Rekey on transport change.

However:

Rekey must not invalidate session continuity
without explicit state transition.

---

# 8. Security Guarantees

Cryptographic model ensures:

- Transport change cannot hijack identity
- Replay cannot mutate session
- Old transport cannot remain active
- Identity cannot fork

Guarantee relies on:

Strong key secrecy
Freshness enforcement
Version enforcement

---

# 9. What This Model Does Not Define

This document does NOT specify:

- HMAC algorithm
- Cipher suites
- TLS integration
- Forward secrecy mechanism
- Data-plane encryption format

Those belong to implementation layer.

This document defines binding semantics only.

---

# 10. Adversary Model

Assume attacker can:

- Observe traffic
- Drop packets
- Inject replayed messages
- Attempt reattach hijack
- Induce transport churn

Assume attacker cannot:

- Break cryptographic primitives
- Extract SessionKey from memory
- Compromise endpoint host

If SessionKey compromised,
identity safety cannot be guaranteed.

Endpoint security is out of scope.

---

# 11. Binding Invariant

At any time:

Session identity is bound to exactly one active transport
through valid proof-of-possession.

Transport mutation does not mutate identity.

Identity mutation is forbidden.

---

# 12. Failure Policy

If cryptographic validation cannot be completed:

Session → TERMINATED

Never:

Downgrade validation.
Allow ambiguous binding.
Fallback silently.

Correctness > Continuity.

---

# Final Principle

Cryptography protects identity.

State machine protects behavior.

Together:

Transport volatility cannot corrupt session continuity.

Session is the anchor.
Transport is volatile.