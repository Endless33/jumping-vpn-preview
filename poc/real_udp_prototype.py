#!/usr/bin/env python3
"""
Jumping VPN - Real UDP Prototype (Minimal)

Goal:
- Demonstrate a *real* UDP client/server with:
  - SESSION (persistent identity)
  - TRANSPORT (ephemeral: socket can be recreated / port can change)
  - REATTACH without full "new session" (uses session-bound proof)

This is NOT production crypto.
It uses an HMAC as "proof of possession" for demonstration.

Run server:
  python poc/real_udp_prototype.py server --bind 0.0.0.0:9999

Run client:
  python poc/real_udp_prototype.py client --server 127.0.0.1:9999

Simulate transport death (client):
  - client will deliberately close its socket (transport dies)
  - then reopen a new UDP socket (new transport) and REATTACH using the same session_id
"""

import argparse
import json
import os
import secrets
import socket
import time
import hmac
import hashlib
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

# Demo shared secret (for PoC only). In real life: derived from handshake keys.
DEMO_SHARED_SECRET = b"jumpingvpn-demo-secret"

SESSION_TTL_SEC = 30  # server keeps session state for this long without traffic


def now_ms() -> int:
    return int(time.time() * 1000)


def bhex(b: bytes) -> str:
    return b.hex()


def hmac_proof(session_id: str, nonce: str) -> str:
    """
    Proof of possession: HMAC(secret, session_id || nonce)
    """
    msg = (session_id + "|" + nonce).encode("utf-8")
    mac = hmac.new(DEMO_SHARED_SECRET, msg, hashlib.sha256).digest()
    return bhex(mac)


def send_json(sock: socket.socket, addr: Tuple[str, int], obj: dict) -> None:
    data = json.dumps(obj).encode("utf-8")
    sock.sendto(data, addr)


def recv_json(sock: socket.socket, bufsize: int = 4096) -> Tuple[dict, Tuple[str, int]]:
    data, addr = sock.recvfrom(bufsize)
    return json.loads(data.decode("utf-8")), addr


@dataclass
class SessionRecord:
    session_id: str
    last_seen_ms: int
    bound_addr: Tuple[str, int]  # current transport endpoint (IP:port)


class Server:
    def __init__(self, bind_ip: str, bind_port: int):
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((bind_ip, bind_port))
        self.sessions: Dict[str, SessionRecord] = {}

    def gc(self) -> None:
        cutoff = now_ms() - (SESSION_TTL_SEC * 1000)
        dead = [sid for sid, rec in self.sessions.items() if rec.last_seen_ms < cutoff]
        for sid in dead:
            del self.sessions[sid]

    def log(self, event: str, **data) -> None:
        print(json.dumps({"ts_ms": now_ms(), "event": event, **data}, ensure_ascii=False))

    def handle(self) -> None:
        self.log("ServerStart", bind=f"{self.bind_ip}:{self.bind_port}", ttl_sec=SESSION_TTL_SEC)

        while True:
            self.gc()

            msg, addr = recv_json(self.sock)
            mtype = msg.get("type")

            if mtype == "HANDSHAKE_INIT":
                # Create new session
                session_id = "S-" + secrets.token_hex(8)
                self.sessions[session_id] = SessionRecord(
                    session_id=session_id,
                    last_seen_ms=now_ms(),
                    bound_addr=addr,
                )
                self.log("SessionCreated", session_id=session_id, transport=f"{addr[0]}:{addr[1]}")

                send_json(self.sock, addr, {
                    "type": "HANDSHAKE_ACK",
                    "session_id": session_id,
                    "note": "session established",
                })

            elif mtype == "DATA":
                session_id = msg.get("session_id")
                payload = msg.get("payload")

                rec = self.sessions.get(session_id)
                if not rec:
                    self.log("DataRejected", reason="unknown_session", from_addr=f"{addr[0]}:{addr[1]}")
                    send_json(self.sock, addr, {"type": "ERROR", "code": "UNKNOWN_SESSION"})
                    continue

                # Require transport to match current binding (for demo).
                # In real design, you might accept data only from active transport.
                if addr != rec.bound_addr:
                    self.log("DataRejected", reason="wrong_transport", session_id=session_id,
                             expected=f"{rec.bound_addr[0]}:{rec.bound_addr[1]}",
                             got=f"{addr[0]}:{addr[1]}")
                    send_json(self.sock, addr, {"type": "ERROR", "code": "WRONG_TRANSPORT"})
                    continue

                rec.last_seen_ms = now_ms()
                self.log("DataAccepted", session_id=session_id, transport=f"{addr[0]}:{addr[1]}", payload=payload)
                send_json(self.sock, addr, {"type": "DATA_ACK", "session_id": session_id})

            elif mtype == "REATTACH_REQUEST":
                session_id = msg.get("session_id")
                nonce = msg.get("nonce")
                proof = msg.get("proof")

                rec = self.sessions.get(session_id)
                if not rec:
                    self.log("ReattachRejected", reason="unknown_session", from_addr=f"{addr[0]}:{addr[1]}")
                    send_json(self.sock, addr, {"type": "ERROR", "code": "UNKNOWN_SESSION"})
                    continue

                expected = hmac_proof(session_id, nonce)
                if not hmac.compare_digest(expected, proof or ""):
                    self.log("ReattachRejected", reason="bad_proof", session_id=session_id,
                             from_addr=f"{addr[0]}:{addr[1]}")
                    send_json(self.sock, addr, {"type": "ERROR", "code": "BAD_PROOF"})
                    continue

                old = rec.bound_addr
                rec.bound_addr = addr
                rec.last_seen_ms = now_ms()

                self.log("TransportSwitch", session_id=session_id,
                         from_transport=f"{old[0]}:{old[1]}",
                         to_transport=f"{addr[0]}:{addr[1]}",
                         reason="transport_volatility",
                         explicit=True,
                         auditable=True)

                send_json(self.sock, addr, {
                    "type": "REATTACH_ACK",
                    "session_id": session_id,
                    "note": "transport reattached",
                })

            else:
                self.log("UnknownMessage", from_addr=f"{addr[0]}:{addr[1]}", msg=msg)
                send_json(self.sock, addr, {"type": "ERROR", "code": "UNKNOWN_TYPE"})


class Client:
    def __init__(self, server_ip: str, server_port: int):
        self.server = (server_ip, server_port)
        self.session_id: Optional[str] = None

    def log(self, event: str, **data) -> None:
        print(json.dumps({"ts_ms": now_ms(), "event": event, **data}, ensure_ascii=False))

    def new_socket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Let OS pick a new ephemeral port (this simulates transport change)
        sock.bind(("0.0.0.0", 0))
        sock.settimeout(2.0)
        return sock

    def run(self) -> None:
        # 1) Create initial transport and handshake
        sock = self.new_socket()
        local = sock.getsockname()
        self.log("ClientStart", local=f"{local[0]}:{local[1]}", server=f"{self.server[0]}:{self.server[1]}")

        send_json(sock, self.server, {"type": "HANDSHAKE_INIT"})
        resp, _ = recv_json(sock)
        if resp.get("type") != "HANDSHAKE_ACK":
            raise RuntimeError(f"Unexpected handshake response: {resp}")

        self.session_id = resp["session_id"]
        self.log("SessionEstablished", session_id=self.session_id)

        # 2) Send some data
        for i in range(3):
            send_json(sock, self.server, {"type": "DATA", "session_id": self.session_id, "payload": f"hello#{i+1}"})
            ack, _ = recv_json(sock)
            self.log("DataRoundtrip", seq=i+1, ack=ack.get("type"))

        # 3) Simulate transport death (close socket)
        self.log("SimulateTransportDeath", note="closing UDP socket (transport)")
        sock.close()

        # 4) Create new transport (new UDP socket => new port)
        sock2 = self.new_socket()
        local2 = sock2.getsockname()
        self.log("NewTransportCreated", local=f"{local2[0]}:{local2[1]}")

        # 5) Reattach using session_id + proof
        nonce = secrets.token_hex(8)
        proof = hmac_proof(self.session_id, nonce)
        send_json(sock2, self.server, {
            "type": "REATTACH_REQUEST",
            "session_id": self.session_id,
            "nonce": nonce,
            "proof": proof,
        })

        resp2, _ = recv_json(sock2)
        self.log("ReattachResult", response=resp2)

        # 6) Continue sending data (should succeed over new transport)
        for i in range(3, 6):
            send_json(sock2, self.server, {"type": "DATA", "session_id": self.session_id, "payload": f"hello#{i+1}"})
            ack, _ = recv_json(sock2)
            self.log("DataRoundtrip", seq=i+1, ack=ack.get("type"))

        self.log("ClientDone", session_id=self.session_id)
        sock2.close()


def parse_hostport(s: str) -> Tuple[str, int]:
    host, port = s.rsplit(":", 1)
    return host, int(port)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)

    aps = sub.add_parser("server")
    aps.add_argument("--bind", default="0.0.0.0:9999", help="bind address, e.g. 0.0.0.0:9999")

    apc = sub.add_parser("client")
    apc.add_argument("--server", default="127.0.0.1:9999", help="server address, e.g. 127.0.0.1:9999")

    args = ap.parse_args()

    if args.mode == "server":
        ip, port = parse_hostport(args.bind)
        Server(ip, port).handle()

    if args.mode == "client":
        ip, port = parse_hostport(args.server)
        Client(ip, port).run()


if __name__ == "__main__":
    main()