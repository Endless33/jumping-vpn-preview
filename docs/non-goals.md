# Jumping VPN — Non-Goals (Public Preview)

This document lists explicit non-goals of Jumping VPN.

Stating non-goals is intentional:
it prevents over-claiming and keeps scope credible.

---

## 1) Not an Anonymity Network

Jumping VPN does not claim to provide:

- Tor-level anonymity
- protection against a global passive adversary
- guaranteed unlinkability across independent networks

Privacy properties depend on deployment context and additional layers.

---

## 2) Not a Censorship Bypass System

Jumping VPN does not inherently guarantee:

- bypass of national firewalls
- DPI evasion
- traffic obfuscation against state-level filtering

Those capabilities require separate obfuscation and routing systems.

---

## 3) Not Endpoint Compromise Protection

Jumping VPN does not protect against:

- malware on the client
- compromised OS / kernel
- malicious local administrators
- physical access attacks

If the endpoint is compromised, session continuity guarantees are irrelevant.

---

## 4) Not Anti-Forensics or Anti-Attribution

Jumping VPN is not designed to:

- erase local traces
- provide anti-forensics guarantees
- defeat endpoint telemetry

Operational security requires additional practices and tooling.

---

## 5) Not a Replacement for All VPNs

Jumping VPN is a behavioral model focused on:

- session continuity under transport volatility
- bounded adaptation and deterministic recovery

It is not positioned as a universal replacement for every VPN use case.

---

## 6) Not "Magic Routing"

Jumping VPN does not claim:

- zero-latency switching
- perfect path selection
- immunity to network-wide outages
- infinite continuity without bounds

If no viable transport exists within policy constraints,
the session terminates deterministically.

---

## 7) Not a Finished, Audited Product (This Repo)

This repository is an architectural preview.
It is not:

- production hardened
- independently audited
- a commercial distribution package

Security review, hardened cryptography, and pilots are staged goals.

---

## Summary

Jumping VPN focuses on one core problem:

**session integrity and continuity under transport volatility**

Everything outside that scope is intentionally treated as a non-goal.