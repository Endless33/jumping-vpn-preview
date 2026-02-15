# Quickstart (60 seconds)

This repo is an architectural preview + deterministic demo package.

What you will validate:
- Session continuity survives transport volatility
- Explicit transport switch (auditable)
- No silent identity reset / renegotiation in the demo contract

## Run (Windows / PowerShell)

From repo root:

```powershell
python --version
python run_demo.py
python demo_engine/replay.py DEMO_OUTPUT.jsonl

Run (Linux/macOS)
From repo root:

python3 --version
python3 run_demo.py
python3 demo_engine/replay.py DEMO_OUTPUT.jsonl

Expected result

The validator should print an ordered set of required events and finish with:

Trace validated successfully

Session continuity preserved
Outputs

Generated files (repo root or /out depending on your version):

DEMO_OUTPUT.jsonl — produced trace

DEMO_PACKAGE.zip — packaged demo artifacts
Troubleshooting

If python is not found: install Python 3.10+ and restart terminal.

If imports fail: ensure you run commands from the repository root (where README.md is).

