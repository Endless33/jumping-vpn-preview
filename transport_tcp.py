# jumping_vpn/transport_tcp.py
from __future__ import annotations

import socket
import time
import secrets
from dataclasses import dataclass
from typing import Optional

from .session_manager import SessionManager, Session


@dataclass
class TCPTransport:
    """
    Early Alpha TCP transport:
    - Connects to an endpoint
    - Can be 'failed' to simulate transport disappearance
    - Does not own identity; it only attaches to a Session
    """
    host: str
    port: int
    sock: Optional[socket.socket] = None
    attachment_id: str = ""

    @property
    def label(self) -> str:
        return f"tcp://{self.host}:{self.port}"

    def connect(self, timeout: float = 1.0) -> None:
        self.attachment_id = f"tcp-attach-{secrets.token_hex(6)}"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((self.host, self.port))
        self.sock = s

    def attach(self, sm: SessionManager, session: Session) -> None:
        if self.sock is None:
            self.connect()
        sm.attach_transport(session, self.label, self.attachment_id)

    def send_ping(self) -> None:
        if not self.sock:
            raise RuntimeError("TCP socket not connected")
        self.sock.sendall(b"ping\n")

    def close(self) -> None:
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                self.sock.close()
            finally:
                self.sock = None

    def simulate_failure(self, sm: SessionManager, session: Session, reason: str = "tcp_failure") -> None:
        # Transport disappears -> session persists but detaches
        self.close()
        sm.detach_transport(session, reason=reason)
        time.sleep(0.05)