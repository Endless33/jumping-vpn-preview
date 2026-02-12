import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from .logger import JsonlLogger
from .policy import Policy
from .transport import Transport


class SessionState(str, Enum):
    BIRTH = "BIRTH"
    ATTACHED = "ATTACHED"
    VOLATILE = "VOLATILE"
    DEGRADED = "DEGRADED"
    RECOVERING = "RECOVERING"
    TERMINATED = "TERMINATED"


class SwitchReason(str, Enum):
    LOSS = "LOSS"
    LATENCY = "LATENCY"
    POLICY = "POLICY"


def now_ms() -> int:
    return int(time.time() * 1000)


@dataclass
class Session:
    session_id: str
    transports: List[Transport]
    policy: Policy
    log: JsonlLogger

    state: SessionState = SessionState.BIRTH
    active: Optional[Transport] = None

    _drops: int = 0
    _last_good_ms: int = field(default_factory=now_ms)
    _switch_times: List[int] = field(default_factory=list)

    def set_state(self, new_state: SessionState, reason: str) -> None:
        if self.state != new_state:
            prev = self.state
            self.state = new_state
            self.log.emit(
                "SessionStateChange",
                session_id=self.session_id,
                prev=str(prev),
                new=str(new_state),
                reason=reason,
            )

    def _switch_rate_ok(self) -> bool:
        cutoff = now_ms() - 60_000
        self._switch_times = [t for t in self._switch_times if t >= cutoff]
        return len(self._switch_times) < self.policy.max_switches_per_min

    def _record_switch(self) -> None:
        self._switch_times.append(now_ms())

    def choose_next_transport(self) -> Optional[Transport]:
        candidates = [t for t in self.transports if t.alive and t is not self.active]
        return candidates[0] if candidates else None

    async def attach_initial(self) -> None:
        first = next((t for t in self.transports if t.alive), None)
        if not first:
            self.set_state(SessionState.TERMINATED, "no_transports_available")
            return

        self.active = first
        self._drops = 0
        self._last_good_ms = now_ms()
        self.set_state(SessionState.ATTACHED, f"attached_to_{first.name}")
        self.log.emit("TransportAttached", session_id=self.session_id, transport=first.name)

    async def switch_transport(self, reason: SwitchReason) -> None:
        if not self._switch_rate_ok():
            self.set_state(SessionState.DEGRADED, "switch_rate_limited")
            self.log.emit(
                "TransportSwitchDenied",
                session_id=self.session_id,
                reason="rate_limit",
            )
            return

        self.set_state(SessionState.RECOVERING, reason.value)
        nxt = self.choose_next_transport()
        if not nxt:
            self.set_state(SessionState.TERMINATED, "no_candidate_transports")
            self.log.emit(
                "TransportSwitchFailed",
                session_id=self.session_id,
                reason="no_candidates",
            )
            return

        prev_name = self.active.name if self.active else None
        self.active = nxt
        self._drops = 0
        self._last_good_ms = now_ms()
        self._record_switch()

        self.log.emit(
            "TransportSwitch",
            session_id=self.session_id,
            from_transport=prev_name,
            to_transport=nxt.name,
            reason=reason.value,
            explicit=True,
            auditable=True,
        )
        self.set_state(SessionState.ATTACHED, f"reattached_to_{nxt.name}")

    async def tick_send(self, seq: int) -> None:
        if not self.active:
            return

        ok = await self.active.send(f"ping#{seq}".encode())
        if ok:
            self._drops = 0
            self._last_good_ms = now_ms()
            self.log.emit(
                "PacketDelivered",
                session_id=self.session_id,
                transport=self.active.name,
                seq=seq,
                state=str(self.state),
            )
            if self.state in (SessionState.VOLATILE, SessionState.DEGRADED):
                self.set_state(SessionState.ATTACHED, "stabilized")
        else:
            self._drops += 1
            self.log.emit(
                "PacketDropped",
                session_id=self.session_id,
                transport=self.active.name if self.active else None,
                seq=seq,
                drops=self._drops,
                state=str(self.state),
            )

            if self.active and not self.active.alive:
                self.set_state(SessionState.VOLATILE, "transport_dead")
                await self.switch_transport(SwitchReason.LOSS)
                return

            if self._drops >= self.policy.max_consecutive_drops:
                self.set_state(SessionState.VOLATILE, "loss_threshold_exceeded")
                await self.switch_transport(SwitchReason.LOSS)
                return

        if now_ms() - self._last_good_ms > self.policy.degrade_after_ms:
            if self.state == SessionState.ATTACHED:
                self.set_state(SessionState.DEGRADED, "no_good_packets_timeout")

    def summary(self) -> str:
        return f"session_id={self.session_id} state={self.state} active={self.active.name if self.active else None}"