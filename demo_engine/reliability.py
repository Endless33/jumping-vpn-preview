import json

class ReliabilityScore:
    """
    Computes a reliability score based on:
    - packet loss
    - recovery time
    - health stability
    - number of failed switches
    """

    def __init__(self, input_path: str, output_path: str = "RELIABILITY.json"):
        self.input_path = input_path
        self.output_path = output_path

    def compute(self):
        events = []
        with open(self.input_path, "r") as f:
            for line in f:
                events.append(json.loads(line))

        loss = len([e for e in events if e["event"] == "PACKET_LOST"])
        failed_switches = len([e for e in events if e["event"] == "SWITCH_BLOCKED"])

        health_values = [e["health_score"] for e in events if "health_score" in e]
        avg_health = sum(health_values) / len(health_values) if health_values else 100

        degraded_ts = None
        restored_ts = None
        for e in events:
            if e["event"] == "DEGRADED_ENTERED":
                degraded_ts = e["ts_ms"]
            if e["event"] == "ATTACHED_RESTORED":
                restored_ts = e["ts_ms"]

        recovery_time = (restored_ts - degraded_ts) if degraded_ts and restored_ts else 0

        score = 100
        score -= loss * 0.1
        score -= failed_switches * 2
        score -= max(0, (recovery_time - 2000) / 100)
        score -= max(0, (50 - avg_health))

        score = max(0, min(100, round(score, 2)))

        result = {
            "reliability_score": score,
            "loss_events": loss,
            "failed_switches": failed_switches,
            "avg_health": avg_health,
            "recovery_time_ms": recovery_time
        }

        with open(self.output_path, "w") as f:
            json.dump(result, f, indent=2)

        return self.output_path