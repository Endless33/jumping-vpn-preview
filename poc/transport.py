import asyncio
import random
from dataclasses import dataclass


@dataclass
class Transport:
    """
    Simulated transport path.
    This PoC models latency, packet loss and alive/dead state.
    No real networking is implemented.
    """
    name: str
    base_latency_ms: int
    loss_prob: float  # 0.0 – 1.0
    alive: bool = True

    async def send(self, payload: bytes) -> bool:
        """
        Returns True if delivered.
        Returns False if dropped or transport is dead.
        """
        if not self.alive:
            await asyncio.sleep(0)
            return False

        jitter = random.randint(0, 40)
        await asyncio.sleep((self.base_latency_ms + jitter) / 1000)

        if random.random() < self.loss_prob:
            return False

        return True