# Client Control-Plane — Reference Skeleton (Preview)

This directory contains the client-side control-plane skeleton for Jumping VPN.

It models how a client:

- Maintains session identity
- Detects transport volatility
- Initiates deterministic reattach
- Enforces local anti-flap bounds
- Preserves session continuity under transport death

This is a behavioral reference implementation — not a production networking stack.

---

## Responsibilities of the Client Agent

The `ClientAgent` is responsible for:

### 1. Session Context

- Maintain `SessionID`
- Maintain local policy snapshot
- Track `state` and `state_version`
- Track freshness counter (nonce)

Identity belongs to the session — not to the transport.

---

### 2. Transport Health Monitoring

The agent exposes hooks for:

- Packet loss
- Latency
- Jitter
- Delivery failure

These signals may cause state transitions:

- `ATTACHED → VOLATILE`
- `ATTACHED → RECOVERING`
- `RECOVERING → ATTACHED`

Health signals do not directly terminate the session.
They trigger deterministic behavior.

---

### 3. Transport Death Handling

When transport delivery is impossible within a bounded window:

ATTACHED → RECOVERING

The client:

- Drops active transport
- Increments state_version
- Emits explicit event
- Initiates reattach request

No silent reset.
No implicit renegotiation.

---

### 4. Reattach Request Construction

A reattach request contains:

- `session_id`
- monotonic `nonce`
- proof-of-possession (placeholder in preview)
- candidate transport metadata

In production:
- proof would be MAC/signature bound to session keys
- freshness must be validated server-side

---

### 5. Anti-Flap Policy

The client enforces:

- switch cooldown window
- bounded reattach frequency
- monotonic nonce progression

Switches are rate-limited.
Volatility is modeled — not reacted to impulsively.

---

## What This Is NOT

This client layer does NOT include:

- Packet encryption
- Real UDP/TCP/QUIC stack
- Cryptographic primitives
- Data-plane framing
- Network IO loops

It models control-plane behavior only.

---

## Intended Review Focus

Engineers reviewing this layer should evaluate:

- State consistency
- Deterministic transitions
- Cooldown enforcement
- Freshness monotonicity
- Recovery boundedness

The design goal is:

Session continuity under volatility,
without dual-active ambiguity
and without uncontrolled oscillation.

---

## Next Steps (Future Expansion)

Future work for the client layer may include:

- Real transport adapter interfaces
- Event-stream emission to observability layer
- Real crypto-bound proof-of-possession
- Replay window tracking
- Adaptive multi-candidate selection logic

---

## Design Principle

The client is not reactive chaos.

It is a deterministic participant in a bounded adaptation system.

Session is the anchor.
Transport is volatile.