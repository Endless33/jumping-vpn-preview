# Demo Engine

This directory contains the contract-first demo engine for Jumping VPN.

## Components

- `engine.py` — deterministic behavioral engine
- `events.py` — JSONL event envelope
- `state_machine.py` — protocol state machine
- `volatility.py` — deterministic volatility simulator
- `scoring.py` — multipath scoring model
- `candidates.py` — candidate transport generator
- `policy.py` — switch/recovery policy
- `audit.py` — invariant checks
- `recovery.py` — recovery window model
- `validator.py` — demo output validator
- `run_demo.py` — generates demo_output.jsonl
- `run_validate.py` — validates demo_output.jsonl

## Usage

python3 run_demo.py python3 run_validate.py

The validator ensures:

- correct event ordering  
- correct state progression  
- invariants respected  
- audit checks passed  
- recovery window completed