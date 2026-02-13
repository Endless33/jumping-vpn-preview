# Orchestrator Layer — Jumping VPN (Preview)

This folder contains the behavioral orchestration skeleton.

It connects:

- session state machine
- deterministic policy evaluation
- transport candidate management
- replay / abuse protection
- measurable recovery metrics

It does **not** implement a full VPN stack.
It models the behavioral core: how sessions survive transport volatility.

---

## Modules

### `runtime_controller.py`
The session-level coordinator.

Responsibilities:
- reacts to transport death / restoration signals
- enforces bounded recovery window
- gates reattach attempts via:
  - anti-replay window
  - switch rate limiting
- exposes state + metrics snapshots

Key idea:
**Correctness first.**
If recovery exceeds bounds → deterministic termination.

---

### `transport_manager.py`
Candidate transport set management + deterministic selection.

Responsibilities:
- maintains a bounded set of transport candidates
- evicts stale candidates (TTL)
- resolves competition deterministically
- guarantees **single active transport**

Deterministic ranking:
Sort by `(priority, loss, rtt, transport_id)`.

---

## How They Work Together

A typical volatility event loop:

1) Candidates discovered / updated  
   `TransportManager.upsert_candidate(...)`

2) Active transport quality violates policy  
   `PolicyEngine.evaluate(...)`

3) If transport declared dead  
   `RuntimeController.on_transport_dead(...)`  
   and `TransportManager.clear_active()`

4) Reattach attempt (bounded + gated)
   `RuntimeController.attempt_reattach(...)`

5) Active selection after reattach  
   `TransportManager.select_active(...)`

6) Recovery success  
   `RuntimeController.on_transport_restored(...)`

All transitions are:
- explicit
- reason-coded
- auditable
- bounded by policy

---

## Non-Goals

This orchestrator does NOT provide:
- real socket handling
- data-plane encryption
- production authentication stack
- kernel integration

It is an architecture-level behavioral core.

---

## Invariants

The orchestrator must preserve:

- no dual-active binding
- monotonic state progression
- bounded recovery
- deterministic rejection on ambiguity
- replay resistance for control-plane actions

---

Session is the anchor.  
Transport is volatile.