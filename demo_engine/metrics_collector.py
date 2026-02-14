import json

class MetricsCollector:
    """
    Collects metrics from a demo_output.jsonl file.
    Produces a structured metrics JSON.
    """

    def __init__(self, path: str):
        self.path = path
        self.events = []
        self.metrics = {}

    def load(self):
        with open(self.path, "r") as f:
            for line in f:
                self.events.append(json.loads(line))

    def collect(self):
        self.metrics["total_events"] = len(self.events)
        self.metrics["packet_lost"] = len([e for e in self.events if e["event"] == "PACKET_LOST"])
        self.metrics["packet_delivered"] = len([e for e in self.events if e["event"] == "PACKET_DELIVERED"])
        self.metrics["switches"] = len([e for e in self.events if e["event"] == "TRANSPORT_SWITCH"])
        self.metrics["avg_rtt"] = self._avg("rtt_smoothed_ms")
        self.metrics["avg_health"] = self._avg("health_score")
        self.metrics["max_rtt"] = self._max("rtt_smoothed_ms")
        self.metrics["min_rtt"] = self._min("rtt_smoothed_ms")
        self.metrics["max_loss"] = self._max("loss_pct")
        self.metrics["max_jitter"] = self._max("jitter_ms")
        return self.metrics

    def _avg(self, field):
        values = [e[field] for e in self.events if field in e and isinstance(e[field], (int, float))]
        return round(sum(values) / len(values), 2) if values else None

    def _max(self, field):
        values = [e[field] for e in self.events if field in e and isinstance(e[field], (int, float))]
        return max(values) if values else None

    def _min(self, field):
        values = [e[field] for e in self.events if field in e and isinstance(e[field], (int, float))]
        return min(values) if values else None

    def export(self, output_path: str):
        with open(output_path, "w") as f:
            json.dump(self.metrics, f, indent=2)
        return output_path