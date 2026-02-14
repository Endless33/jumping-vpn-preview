# Jumping VPN — Demo Package

This directory contains the complete contract‑first demo package for Jumping VPN.
It defines **what the demo must prove**, **how it behaves**, and **how reviewers validate it**.

The demo is not an executed trace.  
It is a deterministic, auditable behavioral contract.

---

## Components

### 1. Demo Specification
Defines the purpose, phases, and pass/fail criteria.

→ [`DEMO_SPEC.md`](DEMO_SPEC.md)

### 2. Output Format
Defines the JSONL event envelope and field structure.

→ [`DEMO_OUTPUT_FORMAT.md`](DEMO_OUTPUT_FORMAT.md)

### 3. Demo Scenario
Defines the timeline (baseline → volatility → switch → recovery).

→ [`DEMO_SCENARIO.md`](DEMO_SCENARIO.md)

### 4. Expected Timeline (Skeleton)
A structured example of what a real demo run will look like.

→ `DEMO_TIMELINE.jsonl`

### 5. Status
What exists today, what is not public, and what is planned.

→ [`STATUS.md`](STATUS.md)

### 6. Review Checklist
A deterministic validation list for engineers.

→ [`REVIEW_CHECKLIST.md`](REVIEW_CHECKLIST.md)

---

## Philosophy

Jumping VPN follows a contract‑first model:

1. Define behavior  
2. Define invariants  
3. Define output  
4. Only then implement  

This demo package is the behavioral contract that the runtime must satisfy.

---

## Summary

This directory provides:

- a reproducible scenario  
- a deterministic output format  
- a validation checklist  
- a clear boundary between implemented and non‑implemented parts  

Session is the anchor.  
Transport is volatile.