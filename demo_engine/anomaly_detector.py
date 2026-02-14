import json

class AnomalyDetector:
    """
    Detects anomalies in RTT, health, and packet behavior.
    """

    def __init__(self, input_path: str, output_path: str = "ANOMALIES.json"):
        self.input_path = input_path
        self.output_path = output_path

    def detect(self):
        events = []
        with open(self.input_path, "r") as f:
            for line in f:
                events.append(json.loads(line))

        anomalies = []

        for e in events:
            if "rtt_smoothed_ms" in e and e["rtt_smoothed_ms"] > 500:
                anomalies.append({"event": "HIGH_RTT", "ts": e["ts_ms"], "value": e["rtt_smoothed_ms"]})

            if "health_score" in e and e["health_score"] < 20:
                anomalies.append({"event": "LOW_HEALTH", "ts": e["ts_ms"], "value": e["health_score"]})

            if e["event"] == "SWITCH_BLOCKED":
                anomalies.append({"event": "FAILED_SWITCH", "ts": e["ts_ms"]})

        with open(self.output_path, "w") as f:
            json.dump(anomalies, f, indent=2)

        return self.output_path