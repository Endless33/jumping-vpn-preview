import json

class PerfProfiler:
    """
    Simulates performance profiling by counting event types.
    """

    COST = {
        "PACKET_DELIVERED": 1,
        "PACKET_LOST": 1,
        "VOLATILITY_SIGNAL": 5,
        "DEGRADED_ENTERED": 3,
        "BEST_CANDIDATE_SELECTED": 4,
        "TRANSPORT_SWITCH": 6,
        "RECOVERY_PROGRESS": 2,
        "ATTACHED_RESTORED": 3
    }

    def __init__(self, input_path: str, output_path: str = "PERF_PROFILE.json"):
        self.input_path = input_path
        self.output_path = output_path

    def generate(self):
        total_cost = 0
        breakdown = {}

        with open(self.input_path, "r") as f:
            for line in f:
                e = json.loads(line)
                cost = self.COST.get(e["event"], 0)
                total_cost += cost
                breakdown[e["event"]] = breakdown.get(e["event"], 0) + cost

        profile = {
            "total_cost": total_cost,
            "breakdown": breakdown
        }

        with open(self.output_path, "w") as f:
            json.dump(profile, f, indent=2)

        return self.output_path