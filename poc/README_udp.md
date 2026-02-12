# Jumping VPN — Real UDP Prototype

## Session Survives Transport Death (Minimal Behavioral Implementation)

This prototype demonstrates a real UDP client/server interaction where:

- A session is created once (`session_id`)
- The active transport dies (UDP socket closed)
- A new transport is created (new source port)
- The client reattaches using a session-bound proof
- The server performs an explicit `TransportSwitch`
- The session continues without reset or renegotiation

This is a behavioral validation prototype.

It is NOT:
- a production VPN
- hardened cryptography
- a secure key exchange implementation

It exists to validate session-centric behavior over real UDP sockets.

---

## What This Demonstrates

1. Session identity is independent of transport binding.
2. Transport volatility is handled explicitly.
3. Reattachment is validated using session-bound proof.
4. The server logs the transport switch.
5. The session does not terminate while valid and within TTL.

---

## Requirements

- Python 3.8+
- Two terminals (or two separate machines)
- No external dependencies

---

## How To Run (Localhost)

### Step 1 — Start Server

From repository root:

```bash
python poc/real_udp_prototype.py server --bind 0.0.0.0:9999
```

Expected server log events:

- `ServerStart`
- `SessionCreated`
- `TransportSwitch`

---

### Step 2 — Start Client

In another terminal:

```bash
python poc/real_udp_prototype.py client --server 127.0.0.1:9999
```

Expected sequence:

1. `HANDSHAKE_INIT`
2. `SessionEstablished`
3. Multiple `DataRoundtrip`
4. `SimulateTransportDeath`
5. New UDP socket created (new local port)
6. `REATTACH_REQUEST`
7. Server emits `TransportSwitch`
8. Continued `DataRoundtrip` without new session creation

---

## How Transport Death Is Simulated

The client deliberately:

- Closes its UDP socket
- Creates a new socket (new ephemeral port)
- Sends a `REATTACH_REQUEST` using the same `session_id`

This mimics:

- NAT rebinding
- Mobile network switch
- Transport failover
- UDP path change

---

## Reattachment Mechanism (PoC Level)

The client sends:

- `session_id`
- `nonce`
- `proof = HMAC(secret, session_id || nonce)`

The server:

- Verifies proof
- Updates `bound_addr`
- Logs `TransportSwitch`
- Returns `REATTACH_ACK`

This is a minimal proof-of-possession demonstration.

Production systems would require:

- Secure handshake
- Proper key derivation
- Anti-replay window management
- Formal cryptographic validation

---

## Session TTL

The server maintains session state for:

```
SESSION_TTL_SEC = 30
```

If no traffic is received within this window:

- The session expires
- Reattach attempts will fail

This models bounded persistence.

---

## What To Verify

On server output:

- `SessionCreated`
- `TransportSwitch`
  - `from_transport`
  - `to_transport`
  - `explicit: true`
  - `auditable: true`

On client output:

- `SessionEstablished`
- `SimulateTransportDeath`
- `ReattachResult`
- Continued `DataRoundtrip`

The key invariant:

Transport death ≠ session death (within TTL and valid proof).

---

## Scope Boundaries

This prototype does NOT:

- Encrypt payload data
- Implement forward secrecy
- Provide anonymity
- Claim censorship resistance
- Provide production security guarantees

It strictly validates behavioral modeling of session-centric transport reattachment.

---

## Architectural Context

Related documentation:

- `docs/state-machine.md`
- `docs/threat-model.md`
- `docs/security-review-plan.md`
- `docs/test-scenarios.md`
- `docs/use-case-fintech-failover.md`

---

## Summary

This prototype validates a core principle:

The session is the anchor.  
Transport is volatile.  
Volatility is modeled — not treated as fatal failure.