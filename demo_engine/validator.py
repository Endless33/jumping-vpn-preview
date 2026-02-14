import json

class DemoValidator:
    """
    Validates the generated demo_output.jsonl file.
    Ensures ordering, state transitions, invariants, and required events.
    """

    REQUIRED_EVENTS = [
        "SESSION_CREATED",
        "VOLATILITY_SIGNAL",
        "DEGRADED_ENTERED",
        "CANDIDATE_SCORES",
        "BEST_CANDIDATE_SELECTED",
        "AUDIT_EVENT",
        "REATTACH_REQUEST",
        "REATTACH_PROOF",
        "TRANSPORT_SWITCH",
        "RECOVERY_SIGNAL",
        "RECOVERY_PROGRESS",
        "ATTACHED_RESTORED"
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

    def check_state_progression(self):
        """
        Ensures the state progression follows the expected path:
        ATTACHED → VOLATILE → DEGRADED → REATTACHING → RECOVERING → ATTACHED
        """
        expected = [
            "SESSION_CREATED",
            "VOLATILITY_SIGNAL",
            "DEGRADED_ENTERED",
            "REATTACH_REQUEST",
            "RECOVERY_SIGNAL",
            "ATTACHED_RESTORED"
        ]

        idx = 0
        for ev in self.events:
            if ev["event"] == expected[idx]:
                idx += 1
                if idx == len(expected):
                    break

        if idx != len(expected):
            self.errors.append("State progression does not match expected sequence")

    def check_audit(self):
        audits = [e for e in self.events if e["event"] == "AUDIT_EVENT"]
        if not audits:
            self.errors.append("Missing AUDIT_EVENT")
            return

        audit = audits[0]
        if not audit.get("identity_ok", False):
            self.errors.append("Audit failed: identity reset detected")

        if not audit.get("dual_binding_ok", False):
            self.errors.append("Audit failed: dual binding detected")

    def validate(self):
        self.load()
        self.check_required_events()
        self.check_timestamp_order()
        self.check_state_progression()
        self.check_audit()

        return self.errors