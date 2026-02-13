"""
Policy Engine — Deterministic Recovery Control

Defines bounded adaptation rules for transport switching,
degradation handling, and termination decisions.

This module does NOT perform networking.
It enforces policy constraints on session state transitions.
"""

from dataclasses import dataclass
from typing import Optional
import time


@dataclass
class PolicyConfig:
    max_switches_per_minute: int = 5
    recovery_window_ms: int = 5000
    transport_loss_ttl_ms: int = 8000
    max_consecutive_failures: int = 3


class PolicyViolation(Exception):
    pass


class PolicyEngine:
    """
    Enforces bounded adaptation rules.
    """

    def __init__(self, config: Optional[PolicyConfig] = None):
        self.config = config or PolicyConfig()
        self._switch_timestamps = []
        self._consecutive_failures = 0

    def record_switch(self):
        now = time.time()
        self._switch_timestamps.append(now)
        self._cleanup_old_switches(now)

        if len(self._switch_timestamps) > self.config.max_switches_per_minute:
            raise PolicyViolation("Switch rate exceeded (anti-flap triggered)")

    def record_failure(self):
        self._consecutive_failures += 1
        if self._consecutive_failures >= self.config.max_consecutive_failures:
            raise PolicyViolation("Too many consecutive transport failures")

    def reset_failures(self):
        self._consecutive_failures = 0

    def check_recovery_window(self, recovery_start_ts_ms: int):
        now_ms = int(time.time() * 1000)
        if now_ms - recovery_start_ts_ms > self.config.recovery_window_ms:
            raise PolicyViolation("Recovery window exceeded")

    def check_transport_loss_ttl(self, last_transport_alive_ms: int):
        now_ms = int(time.time() * 1000)
        if now_ms - last_transport_alive_ms > self.config.transport_loss_ttl_ms:
            raise PolicyViolation("Transport-loss TTL expired")

    def _cleanup_old_switches(self, now: float):
        self._switch_timestamps = [
            ts for ts in self._switch_timestamps
            if now - ts < 60
        ]