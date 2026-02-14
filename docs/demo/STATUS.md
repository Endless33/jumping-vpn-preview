# Demo Status

## What exists today (public preview)

- Architecture model + state machine + invariants
- Threat model, non-goals, limitations
- Behavioral PoCs (conceptual / minimal)
- Telemetry event model
- Multipath scoring model
- Flow-control model (cwnd/pacing/in-flight)

## What is not public / not finalized

- Production-grade cryptography
- Full TUN integration
- Fully formalized reconnect semantics for all edge cases
- Public, reproducible benchmark numbers
- Deterministic transport-switch policy implementation

## What this demo package provides

- A measurable demo contract (steps + pass/fail)
- A stable output format (JSONL event stream)
- A reviewer-friendly validation checklist
- A clear boundary between implemented and non-implemented parts

This repository is a window into the model.
The demo contract defines what will be proven on real runtime output.

Session is the anchor. Transport is volatile.