import json

class ScenarioSummary:
    """
    Aggregates results from multiple scenarios and produces a summary.
    """

    def __init__(self):
        self.results = {}

    def add_result(self, scenario_name: str, path: str):
        with open(path, "r") as f:
            events = [json.loads(line) for line in f]

        summary = {
            "total_events": len(events),
            "switches": len([e for e in events if e["event"] == "TRANSPORT_SWITCH"]),
            "loss_events": len([e for e in events if e["event"] == "PACKET_LOST"]),
            "delivered_packets": len([e for e in events if e["event"] == "PACKET_DELIVERED"]),
            "avg_smoothed_rtt": self._avg(events, "rtt_smoothed_ms"),
            "avg_health_score": self._avg(events, "health_score"),
        }

        self.results[scenario_name] = summary

    def _avg(self, events, field):
        values = []
        for e in events:
            if field in e:
                v = e[field]
                if isinstance(v, (int, float)):
                    values.append(v)
        return round(sum(values) / len(values), 2) if values else None

    def export(self, output_path: str):
        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=2)