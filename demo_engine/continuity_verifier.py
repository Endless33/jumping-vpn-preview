import json
import sys
from typing import Any, Dict, List, Optional


class ContinuityError(Exception):
    pass


def load_jsonl(path: str) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ContinuityError(f"Invalid JSON on line {i}: {e}") from e
    if not events:
        raise ContinuityError("Trace is empty.")
    return events


def get_ts(ev: Dict[str, Any]) -> Optional[int]:
    # поддержим оба формата (ts_ms и ts)
    if "ts_ms" in ev:
        return int(ev["ts_ms"])
    if "ts" in ev:
        return int(ev["ts"])
    return None


def get_session_id(ev: Dict[str, Any]) -> Optional[str]:
    # поддержим оба ключа
    if "session_id" in ev:
        return str(ev["session_id"])
    if "session" in ev:
        return str(ev["session"])
    return None


def verify(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Базовые инварианты
    base_session: Optional[str] = None
    last_ts: Optional[int] = None
    last_state_version: Optional[int] = None

    session_created_count = 0
    transport_switch_count = 0
    audit_fail_count = 0

    identity_reset_markers = {
        "IDENTITY_RESET",
        "REKEY",
        "RENEGOTIATE",
        "SESSION_RESTART",
        "HANDSHAKE_RESTART",
    }

    for idx, ev in enumerate(events, start=1):
        name = str(ev.get("event", ""))

        # 1) session_id постоянен
        sid = get_session_id(ev)
        if sid is not None:
            if base_session is None:
                base_session = sid
            elif sid != base_session:
                raise ContinuityError(
                    f"Session ID changed at event #{idx}: {base_session} -> {sid}"
                )

        # 2) время монотонно
        ts = get_ts(ev)
        if ts is not None:
            if last_ts is None:
                last_ts = ts
            else:
                if ts < last_ts:
                    raise ContinuityError(
                        f"Timestamp went backwards at event #{idx}: {ts} < {last_ts}"
                    )
                last_ts = ts

        # 3) state_version монотонно (если присутствует)
        if "state_version" in ev:
            sv = int(ev["state_version"])
            if last_state_version is None:
                last_state_version = sv
            else:
                if sv < last_state_version:
                    raise ContinuityError(
                        f"state_version decreased at event #{idx}: {sv} < {last_state_version}"
                    )
                last_state_version = sv

        # 4) запрет на “identity reset” маркеры (если кто-то добавит такие события)
        if name in identity_reset_markers:
            raise ContinuityError(f"Identity reset marker found at event #{idx}: {name}")

        # 5) считаем ключевые события
        if name == "SESSION_CREATED":
            session_created_count += 1

        if name == "TRANSPORT_SWITCH":
            transport_switch_count += 1
            # после TRANSPORT_SWITCH НЕ должно быть повторного SESSION_CREATED дальше
            # (мы проверим это глобально ниже)

        if name == "AUDIT_EVENT":
            result = str(ev.get("result", "")).upper()
            if result and result != "PASS":
                audit_fail_count += 1

    # Глобальная проверка: SESSION_CREATED не повторяется после первого
    if session_created_count == 0:
        # не обязательно, но полезно
        raise ContinuityError("No SESSION_CREATED event found.")
    if session_created_count > 1:
        raise ContinuityError(f"Multiple SESSION_CREATED events found: {session_created_count}")

    # Проверка: после первого TRANSPORT_SWITCH не случилось SESSION_CREATED снова
    # (это уже покрыто проверкой множественных SESSION_CREATED, но оставим смысл)
    if transport_switch_count > 0 and session_created_count != 1:
        raise ContinuityError("Transport switch caused session re-creation (unexpected).")

    if audit_fail_count > 0:
        raise ContinuityError(f"AUDIT_EVENT failures: {audit_fail_count}")

    return {
        "session_id": base_session,
        "events": len(events),
        "transport_switches": transport_switch_count,
        "session_created_count": session_created_count,
        "last_ts": last_ts,
        "last_state_version": last_state_version,
        "audit_failures": audit_fail_count,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python demo_engine/continuity_verifier.py DEMO_TRACE.jsonl")
        return 2

    trace_path = sys.argv[1]

    try:
        events = load_jsonl(trace_path)
        report = verify(events)
    except ContinuityError as e:
        print("CONTINUITY: FAIL")
        print(str(e))
        return 1

    print("CONTINUITY: PASS")
    for k, v in report.items():
        print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())