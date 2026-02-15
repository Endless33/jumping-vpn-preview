# prototype/protocol.py
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import hmac
import json
import time
from typing import Any, Dict, Optional

# --- Minimal "session anchor" crypto (demo-level, not production) ---
# The goal: show session continuity + anti-replay via monotonic counters.
# Replace with real AEAD + key schedule later.

def now_ms() -> int:
    return int(time.time() * 1000)

def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def hmac_sha256(key: bytes, msg: bytes) -> bytes:
    return hmac.new(key, msg, hashlib.sha256).digest()

def bhex(b: bytes) -> str:
    return b.hex()

def uhex(s: str) -> bytes:
    return bytes.fromhex(s)

@dataclass
class Packet:
    v: int
    type: str               # "HELLO", "HELLO_ACK", "DATA", "ACK"
    session_id: str
    counter: int            # monotonic per-direction
    ts_ms: int
    payload: Dict[str, Any]
    mac: str                # hex HMAC

    def to_json(self) -> str:
        return json.dumps({
            "v": self.v,
            "type": self.type,
            "session_id": self.session_id,
            "counter": self.counter,
            "ts_ms": self.ts_ms,
            "payload": self.payload,
            "mac": self.mac,
        }, separators=(",", ":"))

    @staticmethod
    def from_json(s: str) -> "Packet":
        o = json.loads(s)
        return Packet(
            v=o["v"],
            type=o["type"],
            session_id=o["session_id"],
            counter=o["counter"],
            ts_ms=o["ts_ms"],
            payload=o.get("payload", {}),
            mac=o["mac"],
        )

def canonical_bytes(v: int, typ: str, session_id: str, counter: int, ts_ms: int, payload: Dict[str, Any]) -> bytes:
    # Canonical encoding for MAC
    body = json.dumps({
        "v": v,
        "type": typ,
        "session_id": session_id,
        "counter": counter,
        "ts_ms": ts_ms,
        "payload": payload,
    }, separators=(",", ":"), sort_keys=True)
    return body.encode("utf-8")

def sign_packet(key: bytes, v: int, typ: str, session_id: str, counter: int, ts_ms: int, payload: Dict[str, Any]) -> Packet:
    body = canonical_bytes(v, typ, session_id, counter, ts_ms, payload)
    mac = bhex(hmac_sha256(key, body))
    return Packet(v=v, type=typ, session_id=session_id, counter=counter, ts_ms=ts_ms, payload=payload, mac=mac)

def verify_packet(key: bytes, pkt: Packet) -> bool:
    body = canonical_bytes(pkt.v, pkt.type, pkt.session_id, pkt.counter, pkt.ts_ms, pkt.payload)
    expected = hmac_sha256(key, body)
    return hmac.compare_digest(expected, uhex(pkt.mac))

def derive_session_key(pre_shared_secret: str, session_id: str) -> bytes:
    # Demo derivation: key = SHA256(psk || session_id)
    return sha256((pre_shared_secret + "::" + session_id).encode("utf-8"))