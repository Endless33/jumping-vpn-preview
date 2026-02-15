# Jumping VPN Demo

This demo demonstrates deterministic session continuity independent of transport attachment.

## Files

DEMO_TRACE.jsonl — published demo trace  
DEMO_OUTPUT.jsonl — deterministic replay output  
DEMO_TRACE_EXPLANATION.md — explanation of each event  

## Key properties demonstrated

• Session identity anchored independently of transport  
• Transport switch without renegotiation  
• Deterministic recovery after volatility  
• No identity reset  
• Cryptographic continuity preserved  

## How to verify

Trace can be replayed deterministically by DemoEngine.

Session identity remains continuous across transport switches.