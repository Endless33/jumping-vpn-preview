import json

class ScenarioDiff:
    """
    Compares two scenario outputs and produces a diff summary.
    """

    def __init__(self, path_a: str, path_b: str):
        self.path_a = path_a
        self.path_b = path_b

    def load(self, path):
        with open(path, "r") as f:
            return [json.loads(line) for line in f]

    def diff(self):
        a = self.load(self.path_a)
        b = self.load(self.path_b)

        def count(events, name):
            return len([e for e in events if e["event"] == name])

        return {
            "switch_diff": count(a, "TRANSPORT_SWITCH") - count(b, "TRANSPORT_SWITCH"),
            "loss_diff": count(a, "PACKET_LOST") - count(b, "PACKET_LOST"),
            "deliver_diff": count(a, "PACKET_DELIVERED") - count(b, "PACKET_DELIVERED"),
            "avg_rtt_diff": self._avg(a, "rtt_smoothed_ms") - self._avg(b, "rtt_smoothed_ms"),
            "avg_health_diff": self._avg(a, "health_score") - self._avg(b, "health_score"),
        }

    def _avg(self, events, field):
        values = [e[field] for e in events if field in e and isinstance(e[field], (int, float))]
        return sum(values) / len(values) if values else 0.0