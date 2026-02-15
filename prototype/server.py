# prototype/server.py
from __future__ import annotations
import argparse
import json
from typing import Dict, Tuple

from prototype.protocol import Packet, derive_session_key, sign_packet, verify_packet, now_ms
from prototype.session_manager import SessionManager

class JumpingVpnServer:
    def __init__(self, host: str, port_a: int, port_b: int, psk: str) -> None:
        import socket
        self.host = host
        self.port_a = port_a
        self.port_b = port_b
        self.psk = psk
        self.sm = SessionManager()

        self.sock_a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_b = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_a.bind((host, port_a))
        self.sock_b.bind((host, port_b))
        self.sock_a.settimeout(0.2)
        self.sock_b.settimeout(0.2)

        # Remember last address per session per path
        self.last_addr: Dict[Tuple[str, str], Tuple[str, int]] = {}

    def _handle(self, raw: bytes, addr: Tuple[str, int], path_name: str) -> None:
        try:
            pkt = Packet.from_json(raw.decode("utf-8"))
        except Exception:
            return

        key = derive_session_key(self.psk, pkt.session_id)
        if not verify_packet(key, pkt):
            # drop invalid MAC
            return

        # Anti-replay
        if not self.sm.accept_rx(pkt.session_id, pkt.counter):
            return

        self.last_addr[(pkt.session_id, path_name)] = addr

        if pkt.type == "HELLO":
            # Reply on same path
            ack = sign_packet(
                key=key,
                v=1,
                typ="HELLO_ACK",
                session_id=pkt.session_id,
                counter=self.sm.next_tx(pkt.session_id),
                ts_ms=now_ms(),
                payload={"path": path_name, "msg": "ok"},
            )
            self._send_on(path_name, ack.to_json().encode("utf-8"), addr)

        elif pkt.type == "DATA":
            # Echo ACK
            ack = sign_packet(
                key=key,
                v=1,
                typ="ACK",
                session_id=pkt.session_id,
                counter=self.sm.next_tx(pkt.session_id),
                ts_ms=now_ms(),
                payload={"path": path_name, "rx": pkt.payload},
            )
            self._send_on(path_name, ack.to_json().encode("utf-8"), addr)

    def _send_on(self, path_name: str, data: bytes, addr: Tuple[str, int]) -> None:
        if path_name == "udp:A":
            self.sock_a.sendto(data, addr)
        else:
            self.sock_b.sendto(data, addr)

    def loop_forever(self) -> None:
        print(f"[server] listening on {self.host}:{self.port_a} (udp:A) and {self.host}:{self.port_b} (udp:B)")
        while True:
            for sock, path_name in [(self.sock_a, "udp:A"), (self.sock_b, "udp:B")]:
                try:
                    raw, addr = sock.recvfrom(65535)
                except Exception:
                    continue
                self._handle(raw, addr, path_name)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port-a", type=int, default=40000)
    ap.add_argument("--port-b", type=int, default=40001)
    ap.add_argument("--psk", default="DEMO_PSK_CHANGE_ME")
    args = ap.parse_args()

    s = JumpingVpnServer(args.host, args.port_a, args.port_b, args.psk)
    s.loop_forever()

if __name__ == "__main__":
    main()