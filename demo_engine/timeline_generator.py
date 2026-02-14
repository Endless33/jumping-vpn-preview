import json

class TimelineGenerator:
    """
    Generates a normalized timeline from demo_output.jsonl.
    Produces a minimal, canonical DEMO_TIMELINE.jsonl.
    """

    KEY_EVENTS = [
        "SESSION_CREATED",
        "VOLATILITY_SIGNAL",
        "DEGRADED_ENTERED",
        "BEST_CANDIDATE_SELECTED",
        "TRANSPORT_SWITCH",
        "RECOVERY_SIGNAL",
        "ATTACHED_RESTORED",
        "SESSION_EXPIRED"
    ]

    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.events = []

    def load(self):
        with open(self.input_path, "r") as f:
            for line in f:
                self.events.append(json.loads(line))

    def filter_key_events(self):
        return [e for e in self.events if e["event"] in self.KEY_EVENTS]

    def normalize(self, ev):
        """
        Produce a minimal canonical event representation.
        """
        return {
            "ts_ms": ev["ts_ms"],
            "event": ev["event"],
            "session_id": ev["session_id"]
        }

    def generate(self):
        self.load()
        key_events = self.filter_key_events()
        key_events = sorted(key_events, key=lambda e: e["ts_ms"])

        with open(self.output_path, "w") as f:
            for ev in key_events:
                f.write(json.dumps(self.normalize(ev)) + "\n")