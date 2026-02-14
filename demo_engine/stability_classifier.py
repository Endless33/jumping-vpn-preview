import json

class StabilityClassifier:
    """
    Classifies session stability based on:
    - RTT variance
    - health score variance
    - number of switches
    """

    def __init__(self, input_path: str, output_path: str = "STABILITY.json"):
        self.input_path = input_path
        self.output_path = output_path

    def classify(self):
        events = []
        with open(self.input_path, "r") as f:
            for line in f:
                events.append(json.loads(line))

        rtts = [e["rtt_smoothed_ms"] for e in events if "rtt_smoothed_ms" in e]
        health = [e["health_score"] for e in events if "health_score" in e]
        switches = len([e for e in events if e["event"] == "TRANSPORT_SWITCH"])

        def variance(values):
            if len(values) < 2:
                return 0.0
            avg = sum(values) / len(values)
            return sum((v - avg) ** 2 for v in values) / len(values)

        rtt_var = variance(rtts)
        health_var = variance(health)

        if switches <= 1 and rtt_var < 50 and health_var < 20:
            status = "STABLE"
        elif switches <= 3 and rtt_var < 150:
            status = "UNSTABLE"
        else:
            status = "CRITICAL"

        result = {
            "status": status,
            "rtt_variance": round(rtt_var, 2),
            "health_variance": round(health_var, 2),
            "switches": switches
        }

        with open(self.output_path, "w") as f:
            json.dump(result, f, indent=2)

        return self.output_path