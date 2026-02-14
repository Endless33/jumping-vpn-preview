import json

class InvariantsChecker:
    """
    Validates protocol invariants.
    """

    def __init__(self, path: str):
        self.path = path
        self.events = []
        self.errors = []

    def load(self):
        with open(self.path, "r") as f:
            for line in f:
                self.events.append(json.loads(line))

    def check_monotonic_timestamps(self):
        ts = [e["ts_ms"] for e in self.events]
        if ts != sorted(ts):
            self.errors.append("Invariant violated: timestamps not monotonic")

    def check_single_expiry(self):
        expiry = [e for e in self.events if e["event"] == "SESSION_EXPIRED"]
        if len(expiry) != 1:
            self.errors.append("Invariant violated: SESSION_EXPIRED must occur exactly once")

    def check_switch_after_degraded(self):
        degraded_seen = False
        for e in self.events:
            if e["event"] == "DEGRADED_ENTERED":
                degraded_seen = True
            if e["event"] == "TRANSPORT_SWITCH" and not degraded_seen:
                self.errors.append("Invariant violated: switch before degraded")

    def validate(self):
        self.load()
        self.check_monotonic_timestamps()
        self.check_single_expiry()
        self.check_switch_after_degraded()
        return self.errors