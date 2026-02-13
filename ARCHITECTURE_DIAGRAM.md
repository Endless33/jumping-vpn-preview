# Jumping VPN — Architecture Diagrams (ASCII)

These diagrams describe the architectural model of Jumping VPN
in a reviewer-friendly format.

Session is the anchor. Transport is volatile.

---

## 1) High-Level System View

+-------------------+                         +----------------------+ |     Client Agent  |                         |    Server Gateway    | |-------------------|                         |----------------------| | Session Context   |                         | Session Table        | |  - session_id     |  Control Plane          |  - ownership         | |  - keys (abstract)|<----------------------->|  - TTLs              | |  - policy         |                         |  - state_version     | |                   |                         |                      | | Transport Adapters|  Data Plane (abstract)  | Transport Listeners  | |  - UDP/TCP/QUIC   |========================>|  - UDP/TCP/QUIC      | +-------------------+                         +----------------------+

+----------------------------------------------+
             |        Observability (Non-Blocking)          |
             |  Events: STATE_CHANGE, SWITCH, SECURITY, ... |
             |  Export: SIEM / NOC / Logs / Dashboard       |
             +----------------------------------------------+

---

## 2) Session vs Transport Model

SESSION (Identity Anchor)             TRANSPORT (Replaceable Attachment)
session_id (stable)                   ip:port / proto / interface keys (session-bound)                  NAT mapping / route / path policy snapshot                        quality fluctuates state machine                           may die anytime
Transport death != Session death (within TTL + policy bounds)

---

## 3) State Machine (Conceptual)

+-------+
       | BIRTH |
       +-------+
           |
           | handshake ok
           v
      +-----------+
      | ATTACHED  |<-----------------------------+
      +-----------+                              |
           |                                     |

instability  |                                     | recovered detected    v                                     | +-----------+                               | | VOLATILE  |                               | +-----------+                               | |                                     | bounds hit |                                     | v                                     | +-----------+                               | | DEGRADED  |                               | +-----------+                               | |                                     | transport dead|                                     | v                                     | +-----------+     reattach ok               | | RECOVERING|-------------------------------+ +-----------+ | | TTL expired / policy exceeded v +-----------+ | TERMINATED| +-----------+

Rules:
- Transitions are explicit and reason-coded
- state_version increments on mutation
- ambiguity fails closed

---

## 4) Control Plane Flow — Reattach

(1) Transport dies Client/Server emits: TRANSPORT_DEAD ATTACHED -> RECOVERING
(2) Client finds candidate path Candidate transport appears (udp/tcp/quic)
(3) Client sends REATTACH_REQUEST
session_id
nonce (freshness)
proof-of-possession (abstract)
candidate transport metadata
expected state_version
(4) Server validates
session exists + TTL valid
nonce freshness (anti-replay)
proof valid
ownership authoritative
CAS(state_version) succeeds
no dual-active binding
(5) Server binds new transport Server emits: TRANSPORT_SWITCH + STATE_CHANGE
(6) Session returns RECOVERING -> ATTACHED No identity reset

---

## 5) Safety Gates (Fail Closed)

REATTACH_REQUEST -> VALIDATION GATES:
[Gate A] session exists + TTL valid [Gate B] state_version matches expected (CAS) [Gate C] nonce fresh (anti-replay) [Gate D] proof valid (crypto module) [Gate E] ownership authoritative (cluster safety) [Gate F] dual-active forbidden
If any gate fails: -> deterministic REJECT (reason-coded) or -> deterministic TERMINATE (reason-coded)

---

## 6) Cluster Ownership (Conceptual)

### Option A: Sticky Routing

SessionID --hash--> Gateway Node (authoritative) Only that node may accept reattach.

### Option B: Shared Atomic Store

All gateways share:
session table
CAS version field Only one winner can bind a transport. Others reject deterministically.

Rule:
- Consistency is preferred over ambiguous continuation.

---

## 7) Observability Timeline (Example)

t0   STATE_CHANGE: ATTACHED t1   VOLATILITY_SIGNAL: LOSS_SPIKE t2   STATE_CHANGE: VOLATILE t3   TRANSPORT_DEAD: NO_DELIVERY_WINDOW t4   STATE_CHANGE: RECOVERING t5   REATTACH_REQUEST_SENT t6   TRANSPORT_SWITCH: CANDIDATE_SELECTED t7   REATTACH_ACK_RECEIVED t8   STATE_CHANGE: ATTACHED

Observability must be:
- structured
- reason-coded
- non-blocking

---

## Final Principle

Jumping VPN is not defined by features.
It is defined by behavior over time.

Session is the anchor.  
Transport is volatile.