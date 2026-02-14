import json
from collections import defaultdict

class AnomalyHeatmap:
    """
    Builds a time-bucketed anomaly heatmap.
    Buckets are 500ms windows.
    """

    def __init__(self, input_path: str, output_path: str = "ANOMALY_HEATMAP.json"):
        self.input_path = input_path
        self.output_path = output_path
        self.events = []

    def load(self):
        with open(self.input_path, "r") as f:
            for line in f:
                self.events.append(json.loads(line))

    def generate(self):
        buckets = defaultdict(lambda: {
            "high_rtt": 0,
            "low_health": 0,
            "loss_spike": 0,
            "failed_switch": 0
        })

        for e in self.events:
            ts = e["ts_ms"]
            bucket = ts // 500  # 500ms window

            # High RTT
            if "rtt_smoothed_ms" in e and e["rtt_smoothed_ms"] > 300:
                buckets[bucket]["high_rtt"] += 1

            # Low health
            if "health_score" in e and e["health_score"] < 40:
                buckets[bucket]["low_health"] += 1

            # Loss spike
            if "loss_pct" in e and e["loss_pct"] > 10:
                buckets[bucket]["loss_spike"] += 1

            # Failed switch
            if e["event"] == "SWITCH_BLOCKED":
                buckets[bucket]["failed_switch"] += 1

        # Convert keys to strings for JSON
        heatmap = {str(k): v for k, v in buckets.items()}

        with open(self.output_path, "w") as f:
            json.dump(heatmap, f, indent=2)

        return self.output_path