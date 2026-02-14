import json

class PhaseTimeline:
    """
    Extracts phase transitions and produces a timeline JSON.
    """

    PHASE_EVENTS = [
        "SESSION_CREATED",
        "VOLATILITY_SIGNAL",
        "DEGRADED_ENTERED",
        "BEST_CANDIDATE_SELECTED",
        "TRANSPORT_SWITCH",
        "RECOVERY_SIGNAL",
        "ATTACHED_RESTORED",
        "SESSION_EXPIRED"
    ]

    def __init__(self, input_path: str, output_path: str = "PHASE_TIMELINE.json"):
        self.input_path = input_path
        self.output_path = output_path

    def generate(self):
        timeline = []
        with open(self.input_path, "r") as f:
            for line in f:
                e = json.loads(line)
                if e["event"] in self.PHASE_EVENTS:
                    timeline.append({
                        "t": e["ts_ms"],
                        "phase": e["event"]
                    })

        with open(self.output_path, "w") as f:
            json.dump(timeline, f, indent=2)

        return self.output_path