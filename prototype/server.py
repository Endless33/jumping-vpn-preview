# prototype/server.py
from __future__ import annotations

import argparse
import hmac
import hashlib
import json
import socket
import threading
import time
from dataclasses import dataclass
from typing import Dict, Optional, Tuple


def now_ms() -> int:
    return int(time.time() * 1000)


def b64_hmac(psk: str, payload: bytes) -> str:
    mac = hmac.new(psk.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return mac


@dataclass
class SessionState:
    session_id: str
    last_counter: int = -1
    active_path: str = "unknown"  # "udp:A" / "udp:B"
    active_addr: Optional[Tuple[str, int]] = None
    last_seen_ms: int = 0


class SessionManager:
    """
    Minimal session table:
    - single session anchor (session_id)
    - monotonic counter enforcement
    - single active binding (path + addr)
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sessions: Dict[str, SessionState] = {}

    def get_or_create(self, session_id: str) -> SessionState:
        with self._lock:
            s = self._sessions.get(session_id)
            if s is None:
                s = SessionState(session_id=session_id, last_seen_ms=now_ms())
                self._sessions[session_id] = s
            return s

    def validate_counter(self, s: SessionState, counter: int) -> bool:
        # Strictly monotonic (simple model).
        # If you want a sliding window later — expand here.
        return counter > s.last_counter

    def bind_active(self, s: SessionState, path: str, addr: Tuple[str, int], counter: int) -> None:
        with self._lock:
            s.active_path = path
            s.active_addr = addr
            s.last_counter = counter
            s.last_seen_ms = now_ms()


class UDPServer:
    def __init__(self, host: str, port_a: int, port_b: int, psk: str) -> None:
        self.host = host
        self.port_a = port_a
        self.port_b = port_b
        self.psk = psk

        self.sessions = SessionManager()
        self._stop = threading.Event()

        self.sock_a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_b = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sock_a.bind((self.host, self.port_a))
        self.sock_b.bind((self.host, self.port_b))

    def stop(self) -> None:
        self._stop.set()
        try:
            self.sock_a.close()
        except Exception:
            pass
        try:
            self.sock_b.close()
        except Exception:
            pass

    def serve_forever(self) -> None:
        t1 = threading.Thread(target=self._loop, args=(self.sock_a, "udp:A"), daemon=True)
        t2 = threading.Thread(target=self._loop, args=(self.sock_b, "udp:B"), daemon=True)
        t1.start()
        t2.start()

        print(f"[server] listening on {self.host}:{self.port_a} (udp:A) and {self.host}:{self.port_b} (udp:B)")
        try:
            while not self._stop.is_set():
                time.sleep(0.2)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def _loop(self, sock: socket.socket, path: str) -> None:
        while not self._stop.is_set():
            try:
                data, addr = sock.recvfrom(64 * 1024)
            except OSError:
                return
            except Exception:
                continue

            msg = self._decode_and_auth(data)
            if msg is None:
                # silently drop (fail-closed)
                continue

            session_id = msg["session_id"]
            counter = int(msg["counter"])
            mtype = msg["type"]

            s = self.sessions.get_or_create(session_id)

            if not self.sessions.validate_counter(s, counter):
                # replay / out-of-order -> reject
                self._send(sock, addr, self._make_reply(session_id, counter, "REJECT", {"reason": "REPLAY_OR_STALE"}))
                print(f"[server] REJECT session={session_id} counter={counter} path={path} addr={addr} reason=REPLAY_OR_STALE")
                continue

            # single active binding update (auditable "switch" if path changes)
            switched = (s.active_path != "unknown" and s.active_path != path)

            self.sessions.bind_active(s, path, addr, counter)

            if mtype == "HELLO":
                reply = self._make_reply(session_id, counter, "ACK", {"hello": True, "active_path": path})
                self._send(sock, addr, reply)
                print(f"[server] HELLO  session={session_id} counter={counter} active={path} addr={addr}")

            elif mtype == "DATA":
                reply = self._make_reply(session_id, counter, "ACK", {"ok": True, "active_path": path})
                self._send(sock, addr, reply)
                if switched:
                    print(f"[server] SWITCH session={session_id} -> {path} (single-active binding) addr={addr}")
                else:
                    print(f"[server] DATA   session={session_id} counter={counter} active={path} addr={addr}")

            elif mtype == "REATTACH":
                reply = self._make_reply(session_id, counter, "ACK", {"reattach": True, "active_path": path})
                self._send(sock, addr, reply)
                print(f"[server] REATTACH session={session_id} counter={counter} active={path} addr={addr}")

            else:
                self._send(sock, addr, self._make_reply(session_id, counter, "REJECT", {"reason": "UNKNOWN_TYPE"}))
                print(f"[server] REJECT session={session_id} counter={counter} path={path} addr={addr} reason=UNKNOWN_TYPE")

    def _decode_and_auth(self, raw: bytes) -> Optional[dict]:
        """
        Wire format:
        {
          "payload": {...},
          "mac": "hex"
        }
        Where MAC = HMAC_SHA256(psk, json(payload_bytes_sorted))
        """
        try:
            outer = json.loads(raw.decode("utf-8"))
            payload = outer["payload"]
            mac = outer["mac"]

            payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
            expected = b64_hmac(self.psk, payload_bytes)

            if not hmac.compare_digest(mac, expected):
                return None
            return payload
        except Exception:
            return None

    def _make_reply(self, session_id: str, counter: int, rtype: str, extra: dict) -> bytes:
        payload = {
            "ts_ms": now_ms(),
            "type": rtype,
            "session_id": session_id,
            "counter": counter,
            "extra": extra,
        }
        payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        outer = {"payload": payload, "mac": b64_hmac(self.psk, payload_bytes)}
        return json.dumps(outer, separators=(",", ":"), sort_keys=True).encode("utf-8")

    def _send(self, sock: socket.socket, addr: Tuple[str, int], data: bytes) -> None:
        try:
            sock.sendto(data, addr)
        except Exception:
            pass


def main() -> None:
    ap = argparse.ArgumentParser(description="Jumping VPN prototype server (UDP A/B)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port-a", type=int, default=40000)
    ap.add_argument("--port-b", type=int, default=40001)
    ap.add_argument("--psk", required=True, help="Pre-shared key for HMAC auth (demo only)")
    args = ap.parse_args()

    srv = UDPServer(args.host, args.port_a, args.port_b, args.psk)
    srv.serve_forever()


if __name__ == "__main__":
    main()