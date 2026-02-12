# Jumping VPN — Limitations (Public Preview)

This document outlines known limitations and explicit non-guarantees
of the Jumping VPN architecture.

Clarity of limitations is essential for responsible deployment.

---

## 1. No Endpoint Compromise Protection

Jumping VPN does not protect against:

- Malware on the client device
- Compromised operating systems
- Rooted or jailbroken environments
- Malicious local administrators

If the endpoint is compromised,
session continuity guarantees are irrelevant.

---

## 2. No Absolute Anonymity Guarantee

Jumping VPN does not claim:

- Tor-level anonymity
- Protection against global passive adversaries
- Guaranteed metadata elimination
- Untraceability across multiple independent networks

Anonymity requires separate infrastructure layers.

---

## 3. No Physical Layer Control

The protocol does not control:

- Radio interference
- ISP throttling
- Total network blackout
- Physical cable disruptions

If no viable transport exists,
the session must terminate.

---

## 4. Requires At Least One Viable Transport

Jumping VPN preserves session continuity
only if at least one candidate transport is available.

If all transports are dead beyond policy bounds,
termination is deterministic.

---

## 5. Performance Trade-Offs

Explicit transport switching and bounded adaptation may introduce:

- Slight recovery latency
- Additional control-plane overhead
- Increased logging output
- Policy-driven switching delays

These are intentional trade-offs for predictability and auditability.

---

## 6. Not a Censorship Bypass System

Jumping VPN does not inherently:

- Evade state-level DPI
- Obfuscate traffic fingerprints
- Guarantee bypass of national firewalls

Additional obfuscation layers would be required.

---

## 7. Not Designed for Ultra-Low-Latency Trading

The architecture prioritizes:

- Deterministic behavior
- Recovery guarantees
- Policy compliance

It is not optimized for microsecond-level trading systems.

---

## 8. Cryptographic Details Not Public in Preview

This repository does not expose:

- Key exchange algorithms
- Exact cryptographic primitives
- Reattachment proof structures

Security-critical implementation details are staged
for hardened release and review.

---

## 9. No Promise of Perpetual Continuity

Session continuity is bounded by:

- Policy constraints
- Session lifetime limits
- Inactivity timeouts
- Security violation triggers

If limits are exceeded, termination is explicit.

---

## 10. Early-Stage Architectural Preview

This repository represents:

- Behavioral modeling
- Architectural direction
- Early PoC demonstration

It does not represent a production-hardened release.

Security reviews, stress testing, and formal validation
remain future phases.

---

## Final Note

Jumping VPN does not attempt to solve every networking problem.

It addresses one core challenge:

Preserving session integrity under transport volatility —
within explicit, bounded rules.