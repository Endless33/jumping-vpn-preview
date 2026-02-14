import json

class PhaseDurationCalculator:
    """
    Calculates duration of each protocol phase.
    """

    PHASE_ORDER = [
        "SESSION_CREATED",
        "VOLATILITY_SIGNAL",
        "DEGRADED_ENTERED",
        "BEST_CANDIDATE_SELECTED",
        "TRANSPORT_SWITCH",
        "RECOVERY_SIGNAL",
        "ATTACHED_RESTORED",
        "SESSION_EXPIRED"
    ]

    def __init__(self, input_path: str, output_path: str = "PHASE_DURATION.json"):
        self.input_path = input_path
        self.output_path = output_path

    def generate(self):
        events = []
        with open(self.input_path, "r") as f:
            for line in f:
                events.append(json.loads(line))

        timestamps = {}
        for e in events:
            if e["event"] in self.PHASE_ORDER:
                timestamps[e["event"]] = e["ts_ms"]

        durations = {}
        for i in range(len(self.PHASE_ORDER) - 1):
            a = self.PHASE_ORDER[i]
            b = self.PHASE_ORDER[i + 1]
            if a in timestamps and b in timestamps:
                durations[a + " → " + b] = timestamps[b] - timestamps[a]

        with open(self.output_path, "w") as f:
            json.dump(durations, f, indent=2)

        return self.output_path