# prototype/transport_layer.py
from __future__ import annotations
import socket
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class UdpPath:
    name: str
    remote_host: str
    remote_port: int

class TransportLayer:
    """
    A minimal "transport attachment" abstraction.
    We can switch paths without recreating session identity.
    """
    def __init__(self, bind_host: str = "0.0.0.0", bind_port: int = 0) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((bind_host, bind_port))
        self.sock.settimeout(0.3)
        self.active: Optional[UdpPath] = None

    def set_active(self, path: UdpPath) -> None:
        self.active = path

    def send(self, data: bytes) -> None:
        if not self.active:
            raise RuntimeError("No active path set")
        self.sock.sendto(data, (self.active.remote_host, self.active.remote_port))

    def recv(self) -> Optional[Tuple[bytes, Tuple[str, int]]]:
        try:
            b, addr = self.sock.recvfrom(65535)
            return b, addr
        except socket.timeout:
            return None

    def close(self) -> None:
        try:
            self.sock.close()
        except Exception:
            pass