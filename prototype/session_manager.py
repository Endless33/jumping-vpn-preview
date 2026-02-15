# prototype/session_manager.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class SessionState:
    session_id: str
    # Monotonic counters per direction
    tx_counter: int = 0
    rx_counter_max: int = -1  # highest accepted counter (anti-replay)

    state: str = "ATTACHED"
    active_path: str = "udp:A"

class SessionManager:
    def __init__(self) -> None:
        self._sessions: Dict[str, SessionState] = {}

    def get_or_create(self, session_id: str) -> SessionState:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionState(session_id=session_id)
        return self._sessions[session_id]

    def next_tx(self, session_id: str) -> int:
        s = self.get_or_create(session_id)
        s.tx_counter += 1
        return s.tx_counter

    def accept_rx(self, session_id: str, counter: int) -> bool:
        """
        Anti-replay gate: accept only strictly increasing counters.
        """
        s = self.get_or_create(session_id)
        if counter <= s.rx_counter_max:
            return False
        s.rx_counter_max = counter
        return True

    def set_state(self, session_id: str, new_state: str) -> None:
        s = self.get_or_create(session_id)
        s.state = new_state

    def set_active_path(self, session_id: str, path: str) -> None:
        s = self.get_or_create(session_id)
        s.active_path = path