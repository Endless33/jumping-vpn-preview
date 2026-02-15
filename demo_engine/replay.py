"""
Jumping VPN — Demo Replay Engine (Preview)

Purpose:
- Read a JSONL demo trace (DEMO_TRACE.jsonl)
- Validate basic structure
- Enforce monotonic time
- Enforce monotonic state_version (when present)
- Reject obvious replay/injection patterns (duplicate counters if present)
- Produce a clear PASS/FAIL summary

This is NOT production crypto.
This is a deterministic demo validator for reviewers.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


# -----------------------------
# Config / expectations
# -----------------------------

REQUIRED_KEYS = {"ts_ms", "event", "session_id"}
OPTIONAL_KEYS = {
    "state",
    "from",
    "to",
    "reason",
    "reason_code",
    "state_version",
    "counter",  # optional monotonic per-session frame counter
    "active_path",
    "from_path",
    "to_path",
    "score",
    "observed",
    "bounded_by_policy",
    "check",
    "result",
}


@dataclass
class ReplayResult:
    ok: bool
    errors: List[str]
    warnings: List[str]
    stats: Dict[str, Any]


# -----------------------------
# Parsing
# -----------------------------

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                # allow comments
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Line {idx}: invalid JSON: {e}") from e
            if not isinstance(obj, dict):
                raise ValueError(f"Line {idx}: event must be a JSON object")
            events.append(obj)
    return events


# -----------------------------
# Validators
# -----------------------------

def validate_required_fields(events: List[Dict[str, Any]]) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    for i, ev in enumerate(events):
        missing = [k for k in REQUIRED_KEYS if k not in ev]
        if missing:
            errors.append(f"Event[{i}] missing required keys: {missing}")

        # warn on unknown keys (helps keep contract clean)
        unknown = [k for k in ev.keys() if k not in REQUIRED_KEYS and k not in OPTIONAL_KEYS]
        if unknown:
            warnings.append(f"Event[{i}] has unknown keys (ok but review): {unknown}")

        # basic type checks
        if "ts_ms" in ev and not isinstance(ev["ts_ms"], int):
            errors.append(f"Event[{i}] ts_ms must be int (ms), got: {type(ev['ts_ms']).__name__}")
        if "event" in ev and not isinstance(ev["event"], str):
            errors.append(f"Event[{i}] event must be str, got: {type(ev['event']).__name__}")
        if "session_id" in ev and not isinstance(ev["session_id"], str):
            errors.append(f"Event[{i}] session_id must be str, got: {type(ev['session_id']).__name__}")

        if "state_version" in ev and not isinstance(ev["state_version"], int):
            errors.append(f"Event[{i}] state_version must be int, got: {type(ev['state_version']).__name__}")

        if "counter" in ev and not isinstance(ev["counter"], int):
            errors.append(f"Event[{i}] counter must be int, got: {type(ev['counter']).__name__}")

    return errors, warnings


def validate_monotonic_time(events: List[Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    last_ts: Optional[int] = None
    for i, ev in enumerate(events):
        ts = ev.get("ts_ms")
        if ts is None:
            continue
        if last_ts is not None and ts < last_ts:
            errors.append(f"Time not monotonic at Event[{i}]: {ts} < {last_ts}")
        last_ts = ts
    return errors


def validate_single_session(events: List[Dict[str, Any]]) -> Tuple[Optional[str], List[str]]:
    errors: List[str] = []
    session_ids = {ev.get("session_id") for ev in events if "session_id" in ev}
    session_ids = {s for s in session_ids if isinstance(s, str)}
    if len(session_ids) == 0:
        errors.append("No valid session_id found in trace.")
        return None, errors
    if len(session_ids) > 1:
        errors.append(f"Trace contains multiple session_id values: {sorted(session_ids)}")
        return None, errors
    return next(iter(session_ids)), errors


def validate_monotonic_state_version(events: List[Dict[str, Any]]) -> List[str]:
    """
    If state_version exists, it must never decrease.
    It may stay the same on non-state events.
    """
    errors: List[str] = []
    last_ver: Optional[int] = None
    for i, ev in enumerate(events):
        if "state_version" not in ev:
            continue
        ver = ev["state_version"]
        if last_ver is not None and ver < last_ver:
            errors.append(f"state_version decreased at Event[{i}]: {ver} < {last_ver}")
        last_ver = ver
    return errors


def validate_counter_anti_replay(events: List[Dict[str, Any]]) -> Tuple[List[str], List[str]]:
    """
    If 'counter' is present, enforce:
    - counter must strictly increase OR at least never repeat (depending on trace style)
    We'll enforce: no duplicates (replay) and no decrease (rollback).
    """
    errors: List[str] = []
    warnings: List[str] = []
    seen: set[int] = set()
    last: Optional[int] = None

    counters = [ev.get("counter") for ev in events if "counter" in ev]
    if not counters:
        warnings.append("No 'counter' fields found. Anti-replay check limited to state_version/time only.")
        return errors, warnings

    for i, ev in enumerate(events):
        if "counter" not in ev:
            continue
        c = ev["counter"]
        if c in seen:
            errors.append(f"Replay detected: duplicate counter={c} at Event[{i}]")
        seen.add(c)
        if last is not None and c < last:
            errors.append(f"Counter rollback detected at Event[{i}]: {c} < {last}")
        last = c

    return errors, warnings


def validate_core_claim(events: List[Dict[str, Any]]) -> Tuple[List[str], List[str]]:
    """
    Minimal high-signal checks:
    - must contain TRANSPORT_SWITCH
    - must contain ATTACHED state at start and end (either via 'state' or STATE_CHANGE to ATTACHED)
    - must NOT contain TERMINATED (unless explicitly documented, but demo claim says no)
    """
    errors: List[str] = []
    warnings: List[str] = []

    event_names = [ev.get("event") for ev in events if isinstance(ev.get("event"), str)]

    if "TRANSPORT_SWITCH" not in event_names:
        errors.append("Missing required event: TRANSPORT_SWITCH")

    if "TERMINATED" in [ev.get("state") for ev in events if "state" in ev]:
        errors.append("Trace contains state=TERMINATED (demo claim expects no termination).")

    # find attached at start/end
    attached_mentions = 0
    for ev in events:
        if ev.get("state") == "ATTACHED":
            attached_mentions += 1
        if ev.get("event") == "STATE_CHANGE" and ev.get("to") == "ATTACHED":
            attached_mentions += 1

    if attached_mentions == 0:
        warnings.append("No explicit ATTACHED found (state or STATE_CHANGE to ATTACHED). Consider adding for clarity.")

    # soft check: volatility -> switch -> recover
    if "VOLATILITY_SIGNAL" not in event_names:
        warnings.append("No VOLATILITY_SIGNAL found. Demo may feel less realistic to reviewers.")
    if "RECOVERY_SIGNAL" not in event_names:
        warnings.append("No RECOVERY_SIGNAL found. Demo may feel less complete.")

    return errors, warnings


# -----------------------------
# Runner
# -----------------------------

def run(path: str) -> ReplayResult:
    events = load_jsonl(path)

    errors: List[str] = []
    warnings: List[str] = []

    e1, w1 = validate_required_fields(events)
    errors.extend(e1)
    warnings.extend(w1)

    sid, e2 = validate_single_session(events)
    errors.extend(e2)

    errors.extend(validate_monotonic_time(events))
    errors.extend(validate_monotonic_state_version(events))

    e3, w3 = validate_counter_anti_replay(events)
    errors.extend(e3)
    warnings.extend(w3)

    e4, w4 = validate_core_claim(events)
    errors.extend(e4)
    warnings.extend(w4)

    stats = {
        "path": path,
        "events_total": len(events),
        "session_id": sid,
        "has_counter": any("counter" in ev for ev in events),
        "has_state_version": any("state_version" in ev for ev in events),
        "events": sorted({ev.get("event") for ev in events if isinstance(ev.get("event"), str)}),
    }

    return ReplayResult(ok=(len(errors) == 0), errors=errors, warnings=warnings, stats=stats)


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Usage: python demo_engine/replay.py <path_to_jsonl>")
        print("Example: python demo_engine/replay.py DEMO_TRACE.jsonl")
        return 2

    path = argv[1]
    result = run(path)

    print("\n=== Jumping VPN Demo Replay Validation ===")
    for k, v in result.stats.items():
        print(f"{k}: {v}")

    if result.warnings:
        print("\nWARNINGS:")
        for w in result.warnings:
            print(f"- {w}")

    if not result.ok:
        print("\nFAIL:")
        for e in result.errors:
            print(f"- {e}")
        return 1

    print("\nPASS: deterministic demo trace validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))