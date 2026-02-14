import json

class DemoValidator:
    REQUIRED_EVENTS = [
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

    def check_required_events(self):
        seen = {e["event"] for e in self.events}
        for req in self.REQUIRED_EVENTS:
            if req not in seen:
                self.errors.append(f"Missing required event: {req}")

    def check_timestamp_order(self):
        timestamps = [e["ts_ms"] for e in self.events]
        if timestamps != sorted(timestamps):
            self.errors.append("Timestamps are not strictly increasing")

    def check_heartbeat(self):
        heartbeats = [e for e in self.events if e["event"] == "HEARTBEAT"]
        if not heartbeats:
            self.errors.append("Missing HEARTBEAT events")

    def check_session_expiry(self):
        expiry = [e for e in self.events if e["event"] == "SESSION_EXPIRED"]
        if not expiry:
            self.errors.append("Missing SESSION_EXPIRED event")

    def validate(self):
        self.load()
        self.check_required_events()
        self.check_timestamp_order()
        self.check_heartbeat()
        self.check_session_expiry()
        return self.errors