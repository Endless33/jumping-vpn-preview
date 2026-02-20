# jumping_vpn/transport_udp.py
from __future__ import annotations

import socket
import time
import secrets
from dataclasses import dataclass
from typing import Optional

from .session_manager import SessionManager, Session


@dataclass
class UDPTransport:
    """
    Early Alpha UDP transport:
    - Creates a UDP socket and can 'attach' to the same Session identity
    - Used to demonstrate transport switching without identity reset
    """
    host: str
    port: int
    sock: Optional[socket.socket] = None
    attachment_id: str = ""

    @property
    def label(self) -> str:
        return f"udp://{self.host}:{self.port}"

    def open(self) -> None:
        self.attachment_id = f"udp-attach-{secrets.token_hex(6)}"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock = s

    def attach(self, sm: SessionManager, session: Session) -> None:
        if self.sock is None:
            self.open()
        sm.attach_transport(session, self.label, self.attachment_id)

    def send_ping(self) -> None:
        if not self.sock:
            raise RuntimeError("UDP socket not opened")
        self.sock.sendto(b"ping\n", (self.host, self.port))

    def close(self) -> None:
        if self.sock:
            try:
                self.sock.close()
            finally:
                self.sock = None

    def simulate_failure(self, sm: SessionManager, session: Session, reason: str = "udp_failure") -> None:
        self.close()
        sm.detach_transport(session, reason=reason)
        time.sleep(0.05)