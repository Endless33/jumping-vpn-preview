"""
Jumping VPN — Demo Trace Validator (contract-first)

Validates a JSONL demo trace for deterministic session continuity.

Usage:
    python demo_engine/replay.py DEMO_TRACE.jsonl

Expected output style:
    SESSION_CREATED OK
    VOLATILITY_SIGNAL OK
    TRANSPORT_SWITCH OK
    STATE_CHANGE OK
    RECOVERY_COMPLETE OK
    Trace validated successfully. Session continuity preserved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


REQUIRED_EVENTS_IN_ORDER = [
    "SESSION_CREATED",
    "VOLATILITY_SIGNAL",
    "TRANSPORT_SWITCH",
    "STATE_CHANGE",        # must include ATTACHED -> VOLATILE
    "RECOVERY_COMPLETE",   # represented by STATE_CHANGE to ATTACHED with reason RECOVERY_COMPLETE
]

# Minimal required fields for the contract:
BASE_REQUIRED_FIELDS = ["event", "session_id", "ts_ms"]


class ValidationError(Exception):
    pass


def _load_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise ValidationError(f"File not found: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValidationError("Trace file is empty.")

    events: List[Dict[str, Any]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as ex:
            raise ValidationError(f"Invalid JSON at line {i}: {ex}") from ex
        if not isinstance(obj, dict):
            raise ValidationError(f"JSONL line {i} must be an object/dict.")
        events.append(obj)

    if not events:
        raise ValidationError("No JSON events found (only comments/blank lines?).")

    return events


def _get_event_name(e: Dict[str, Any]) -> str:
    # Accept both "event" and "event_type" (some docs use either)
    return str(e.get("event") or e.get("event_type") or "").strip()


def _require_fields(e: Dict[str, Any], fields: List[str]) -> None:
    missing = [f for f in fields if f not in e]
    if missing:
        raise ValidationError(f"Missing required fields {missing} in event: {e}")


def _is_state_change_to_attached_recovery_complete(e: Dict[str, Any]) -> bool:
    if _get_event_name(e) != "STATE_CHANGE":
        return False
    to_state = (e.get("to") or e.get("state") or "").strip()
    reason = (e.get("reason") or "").strip()
    return to_state == "ATTACHED" and reason == "RECOVERY_COMPLETE"


def _is_state_change_attached_to_volatile(e: Dict[str, Any]) -> bool:
    if _get_event_name(e) != "STATE_CHANGE":
        return False
    frm = (e.get("from") or "").strip()
    to = (e.get("to") or e.get("state") or "").strip()
    return frm == "ATTACHED" and to == "VOLATILE"


def _validate_monotonic_ts(events: List[Dict[str, Any]]) -> None:
    last: Optional[int] = None
    for e in events:
        ts = e.get("ts_ms")
        if not isinstance(ts, int):
            raise ValidationError(f"ts_ms must be int (ms). Bad event: {e}")
        if last is not None and ts < last:
            raise ValidationError("ts_ms must be non-decreasing (monotonic).")
        last = ts


def _validate_single_session(events: List[Dict[str, Any]]) -> str:
    sid = None
    for e in events:
        name = _get_event_name(e)
        if not name:
            raise ValidationError(f"Event missing 'event'/'event_type': {e}")
        _require_fields(e, ["session_id", "ts_ms"])
        if sid is None:
            sid = str(e["session_id"])
        elif str(e["session_id"]) != sid:
            raise ValidationError("Trace must contain a single session_id (single demo session).")
    assert sid is not None
    return sid


def _validate_no_termination(events: List[Dict[str, Any]]) -> None:
    for e in events:
        name = _get_event_name(e)
        if name == "STATE_CHANGE":
            to_state = (e.get("to") or e.get("state") or "").strip()
            if to_state == "TERMINATED":
                raise ValidationError("TERMINATED found: session continuity violated.")
        if name == "TERMINATED":
            raise ValidationError("TERMINATED event found: session continuity violated.")


def _validate_switch_fields(events: List[Dict[str, Any]]) -> None:
    for e in events:
        if _get_event_name(e) == "TRANSPORT_SWITCH":
            # Require from/to path identifiers
            if not (e.get("from_path") or e.get("from")):
                raise ValidationError("TRANSPORT_SWITCH must include from_path/from.")
            if not (e.get("to_path") or e.get("to")):
                raise ValidationError("TRANSPORT_SWITCH must include to_path/to.")


def _validate_audit_no_dual_active(events: List[Dict[str, Any]]) -> None:
    # Optional but strong: if present, must PASS
    for e in events:
        if _get_event_name(e) in ("AUDIT_EVENT", "SECURITY_EVENT"):
            if str(e.get("check", "")).strip() == "NO_DUAL_ACTIVE_BINDING":
                if str(e.get("result", "")).strip().upper() != "PASS":
                    raise ValidationError("NO_DUAL_ACTIVE_BINDING audit not PASS.")


def _validate_required_sequence(events: List[Dict[str, Any]]) -> List[str]:
    """
    Returns a list of status lines like 'SESSION_CREATED OK'
    """
    status: List[str] = []

    # 1) SESSION_CREATED exists
    if any(_get_event_name(e) == "SESSION_CREATED" for e in events):
        status.append("SESSION_CREATED OK")
    else:
        raise ValidationError("Missing SESSION_CREATED.")

    # 2) VOLATILITY_SIGNAL exists
    if any(_get_event_name(e) == "VOLATILITY_SIGNAL" for e in events):
        status.append("VOLATILITY_SIGNAL OK")
    else:
        raise ValidationError("Missing VOLATILITY_SIGNAL.")

    # 3) TRANSPORT_SWITCH exists
    if any(_get_event_name(e) == "TRANSPORT_SWITCH" for e in events):
        status.append("TRANSPORT_SWITCH OK")
    else:
        raise ValidationError("Missing TRANSPORT_SWITCH.")

    # 4) Must contain ATTACHED -> VOLATILE explicit change
    if any(_is_state_change_attached_to_volatile(e) for e in events):
        status.append("STATE_CHANGE OK")
    else:
        raise ValidationError("Missing STATE_CHANGE ATTACHED -> VOLATILE.")

    # 5) Must contain recovery completion (STATE_CHANGE ... to ATTACHED with reason RECOVERY_COMPLETE)
    if any(_is_state_change_to_attached_recovery_complete(e) for e in events):
        status.append("RECOVERY_COMPLETE OK")
    else:
        raise ValidationError("Missing recovery completion back to ATTACHED (reason=RECOVERY_COMPLETE).")

    return status


def validate(trace_path: Path) -> Tuple[bool, str]:
    events = _load_jsonl(trace_path)

    # Basic invariants
    _validate_single_session(events)
    _validate_monotonic_ts(events)
    _validate_no_termination(events)
    _validate_switch_fields(events)
    _validate_audit_no_dual_active(events)

    status_lines = _validate_required_sequence(events)

    out = []
    out.extend(status_lines)
    out.append("Trace validated successfully. Session continuity preserved.")
    return True, "\n".join(out)


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("Usage: python demo_engine/replay.py DEMO_TRACE.jsonl")
        return 2

    trace_path = Path(argv[1]).resolve()

    try:
        ok, msg = validate(trace_path)
        print(msg)
        return 0 if ok else 1
    except ValidationError as ex:
        print(f"VALIDATION FAILED: {ex}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))