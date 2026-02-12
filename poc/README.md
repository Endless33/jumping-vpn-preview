# Jumping VPN PoC — Session survives transport death

This Proof of Concept demonstrates the core behavioral claim:

- The session is the source of truth  
- The transport is replaceable  
- Transport failure triggers an explicit, auditable switch  
- The session does NOT terminate if a backup transport exists  

---

## Run

From the repository root:

```bash
python -m poc.demo
```

---

## Output

The PoC writes JSONL logs to:

```
out/poc_run.jsonl
```

Look for these events:

- `TransportKilled`
- `TransportSwitch`
- `SessionStateChange`

---

## Expected Result

- A `TransportSwitch` occurs after the primary transport is killed  
- The session returns to `ATTACHED`  
- No `TERMINATED` state occurs while a backup transport is alive