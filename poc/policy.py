from dataclasses import dataclass


@dataclass
class Policy:
    # Maximum consecutive packet drops before marking transport unstable
    max_consecutive_drops: int = 3

    # If no successful delivery within this time (ms),
    # session enters DEGRADED state
    degrade_after_ms: int = 1500

    # Limit transport switches per minute (anti-flapping protection)
    max_switches_per_min: int = 10