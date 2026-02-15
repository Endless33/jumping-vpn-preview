# prototype/client.py
from __future__ import annotations
import argparse
import json
import time
from typing import Optional

from prototype.protocol import Packet, derive_session_key, sign_packet, verify_packet, now_ms
from prototype.session_manager import SessionManager
from prototype.transport_layer import TransportLayer, UdpPath

class JumpingVpnClient:
    def __init__(self, host: str, port_a: int, port_b: int, psk: str, session_id: str, trace_path: str) -> None:
        self.psk = psk
        self.session_id = session_id
        self.key = derive_session_key(psk, session_id)
        self.sm = SessionManager()
        self.tl = TransportLayer()
        self.path_a = UdpPath("udp:A", host, port_a)
        self.path_b = UdpPath("udp:B", host, port_b)
        self.tl.set_active(self.path_a)
        self.trace_path = trace_path

        self._trace({"ts_ms": now_ms(), "event": "SESSION_CREATED", "session_id": session_id, "state": "ATTACHED", "active_path": "udp:A"})

    def _trace(self, obj: dict) -> None:
        with open(self.trace_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj, separators=(",", ":")) + "\n")

    def _send(self, typ: str, payload: dict) -> None:
        c = self.sm.next_tx(self.session_id)
        pkt = sign_packet(self.key, 1, typ, self.session_id, c, now_ms(), payload)
        self.tl.send(pkt.to_json().encode("utf-8"))

    def _recv_one(self) -> Optional[Packet]:
        got = self.tl.recv()
        if not got:
            return None
        raw, _addr = got
        try:
            pkt = Packet.from_json(raw.decode("utf-8"))
        except Exception:
            return None
        if pkt.session_id != self.session_id:
            return None
        if not verify_packet(self.key, pkt):
            return None
        if not self.sm.accept_rx(self.session_id, pkt.counter):
            return None
        return pkt

    def hello(self) -> bool:
        self._trace({"ts_ms": now_ms(), "event": "PATH_SELECTED", "session_id": self.session_id, "active_path": self.sm.get_or_create(self.session_id).active_path})
        self._send("HELLO", {"active_path": self.sm.get_or_create(self.session_id).active_path})
        t0 = time.time()
        while time.time() - t0 < 2.0:
            pkt = self._recv_one()
            if pkt and pkt.type == "HELLO_ACK":
                return True
        return False

    def simulate_volatility(self) -> None:
        self.sm.set_state(self.session_id, "VOLATILE")
        self._trace({"ts_ms": now_ms(), "event": "VOLATILITY_SIGNAL", "session_id": self.session_id, "reason": "LOSS_SPIKE", "observed": {"loss_pct": 7.5, "rtt_ms": 41, "jitter_ms": 18}})
        self._trace({"ts_ms": now_ms(), "event": "STATE_CHANGE", "session_id": self.session_id, "from": "ATTACHED", "to": "VOLATILE", "reason": "LOSS_SPIKE"})

    def switch_transport(self) -> None:
        self.sm.set_state(self.session_id, "RECOVERING")
        self._trace({"ts_ms": now_ms(), "event": "STATE_CHANGE", "session_id": self.session_id, "from": "VOLATILE", "to": "RECOVERING", "reason": "PREFERRED_PATH_CHANGED"})

        # Switch attachment
        self.tl.set_active(self.path_b)
        self.sm.set_active_path(self.session_id, "udp:B")
        self._trace({"ts_ms": now_ms(), "event": "TRANSPORT_SWITCH", "session_id": self.session_id, "from_path": "udp:A", "to_path": "udp:B", "reason": "PREFERRED_PATH_CHANGED"})

    def recover(self) -> bool:
        # Prove continuity: same session_id, monotonic counters, same key.
        ok = self.hello()
        if ok:
            self.sm.set_state(self.session_id, "ATTACHED")
            self._trace({"ts_ms": now_ms(), "event": "STATE_CHANGE", "session_id": self.session_id, "from": "RECOVERING", "to": "ATTACHED", "reason": "RECOVERY_COMPLETE"})
        return ok

    def close(self) -> None:
        self.tl.close()

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port-a", type=int, default=40000)
    ap.add_argument("--port-b", type=int, default=40001)
    ap.add_argument("--psk", default="DEMO_PSK_CHANGE_ME")
    ap.add_argument("--session-id", default="DEMO-SESSION")
    ap.add_argument("--trace", default="DEMO_TRACE.jsonl")
    args = ap.parse_args()

    c = JumpingVpnClient(args.host, args.port_a, args.port_b, args.psk, args.session_id, args.trace)

    if not c.hello():
        print("[client] HELLO failed on udp:A")
        c.close()
        raise SystemExit(1)

    c.simulate_volatility()
    c.switch_transport()

    if not c.recover():
        print("[client] recovery failed on udp:B")
        c.close()
        raise SystemExit(2)

    print("[client] done. trace:", args.trace)
    c.close()

if __name__ == "__main__":
    main()