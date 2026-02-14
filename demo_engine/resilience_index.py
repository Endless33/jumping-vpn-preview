import json
import math

class ResilienceIndex:
    """
    Computes a single resilience score (0–100) based on:
    - RTT stability
    - health stability
    - recovery speed
    - anomaly density
    - switching efficiency
    """

    def __init__(self, input_path: str, output_path: str = "RESILIENCE_INDEX.json"):
        self.input_path = input_path
        self.output_path = output_path
        self.events = []

    def load(self):
        with open(self.input_path, "r") as f:
            for line in f:
                self.events.append(json.loads(line))

    def compute(self):
        rtts = [e["rtt_smoothed_ms"] for e in self.events if "rtt_smoothed_ms" in e]
        health = [e["health_score"] for e in self.events if "health_score" in e]

        switches = len([e for e in self.events if e["event"] == "TRANSPORT_SWITCH"])
        failed_switches = len([e for e in self.events if e["event"] == "SWITCH_BLOCKED"])
        anomalies = len([e for e in self.events if "loss_pct" in e and e["loss_pct"] > 10])

        # Variance helpers
        def variance(values):
            if len(values) < 2:
                return 0.0
            avg = sum(values) / len(values)
            return sum((v - avg) ** 2 for v in values) / len(values)

        rtt_var = variance(rtts)
        health_var = variance(health)

        # Recovery time
        degraded_ts = None
        restored_ts = None
        for e in self.events:
            if e["event"] == "DEGRADED_ENTERED":
                degraded_ts = e["ts_ms"]
            if e["event"] == "ATTACHED_RESTORED":
                restored_ts = e["ts_ms"]

        recovery_time = (restored_ts - degraded_ts) if degraded_ts and restored_ts else 0

        # Score components
        score = 100

        # RTT stability
        score -= min(40, rtt_var / 10)

        # Health stability
        score -= min(30, health_var / 5)

        # Recovery penalty
        if recovery_time > 2000:
            score -= min(20, (recovery_time - 2000) / 100)

        # Switching penalty
        score -= failed_switches * 5
        score -= max(0, switches - 3) * 2

        # Anomaly penalty
        score -= anomalies * 1.5

        score = max(0, min(100, round(score, 2)))

        result = {
            "resilience_index": score,
            "rtt_variance": round(rtt_var, 2),
            "health_variance": round(health_var, 2),
            "switches": switches,
            "failed_switches": failed_switches,
            "anomalies": anomalies,
            "recovery_time_ms": recovery_time
        }

        with open(self.output_path, "w") as f:
            json.dump(result, f, indent=2)

        return self.output_path