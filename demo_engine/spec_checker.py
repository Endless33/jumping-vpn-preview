import json

class DemoSpecChecker:
    """
    Validates compliance with DEMO_SPEC.md.
    """

    REQUIRED_PHASES = [
        "SESSION_CREATED",
        "VOLATILITY_SIGNAL",
        "DEGRADED_ENTERED",
        "CANDIDATE_SCORES_RAW",
        "CANDIDATE_SCORES_WEIGHTED",
        "BEST_CANDIDATE_SELECTED",
        "AUDIT_EVENT",
        "REATTACH_REQUEST",
        "REATTACH_PROOF",
        "TRANSPORT_SWITCH",
        "RECOVERY_SIGNAL",
        "RECOVERY_PROGRESS",
        "ATTACHED_RESTORED",
        "SESSION_EXPIRED"
    ]

    def __init__(self, path: str):
        self.path = path
        self.events = []
        self.errors = []

    def load(self):
        with open(self.path, "r") as f:
            for line in f:
                self.events.append(json.loads(line))

    def check_required_phases(self):
        seen = {e["event"] for e in self.events}
        for phase in self.REQUIRED_PHASES:
            if phase not in seen:
                self.errors.append(f"Missing required phase: {phase}")

    def check_recovery_window(self):
        progress = [e for e in self.events if e["event"] == "RECOVERY_PROGRESS"]
        if not progress:
            self.errors.append("Missing RECOVERY_PROGRESS events")
            return

        elapsed = [p["elapsed_ms"] for p in progress]
        if elapsed != sorted(elapsed):
            self.errors.append("Recovery window timestamps not increasing")

        if elapsed[-1] < 2000:
            self.errors.append("Recovery window shorter than required 2000ms")

    def check_switching_logic(self):
        switches = [e for e in self.events if e["event"] == "TRANSPORT_SWITCH"]
        if not switches:
            self.errors.append("Missing TRANSPORT_SWITCH event")

    def validate(self):
        self.load()
        self.check_required_phases()
        self.check_recovery_window()
        self.check_switching_logic()
        return self.errors