import json

class ChaosRecoveryAnalyzer:
    """
    Analyzes how well the engine recovers under chaos-mode.
    Measures:
    - time to recovery
    - number of failed switches
    - health degradation depth
    """

    def __init__(self, input_path: str, output_path: str = "CHAOS_RECOVERY.json"):
        self.input_path = input_path
        self.output_path = output_path

    def analyze(self):
        events = []
        with open(self.input_path, "r") as f:
            for line in f:
                events.append(json.loads(line))

        degraded_ts = None
        restored_ts = None
        failed_switches = 0
        min_health = 100.0

        for e in events:
            if e["event"] == "DEGRADED_ENTERED":
                degraded_ts = e["ts_ms"]

            if e["event"] == "ATTACHED_RESTORED":
                restored_ts = e["ts_ms"]

            if e["event"] == "SWITCH_BLOCKED":
                failed_switches += 1

            if "health_score" in e:
                min_health = min(min_health, e["health_score"])

        recovery_time = None
        if degraded_ts is not None and restored_ts is not None:
            recovery_time = restored_ts - degraded_ts

        result = {
            "recovery_time_ms": recovery_time,
            "failed_switches": failed_switches,
            "min_health_score": min_health
        }

        with open(self.output_path, "w") as f:
            json.dump(result, f, indent=2)

        return self.output_path