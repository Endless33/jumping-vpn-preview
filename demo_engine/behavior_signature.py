import json
import hashlib

class BehavioralSignature:
    """
    Extracts a behavioral signature from demo_output.jsonl.
    Signature is based on:
    - event sequence
    - switching pattern
    - RTT trend
    - health trend
    """

    def __init__(self, input_path: str, output_path: str = "BEHAVIOR_SIGNATURE.json"):
        self.input_path = input_path
        self.output_path = output_path
        self.events = []

    def load(self):
        with open(self.input_path, "r") as f:
            for line in f:
                self.events.append(json.loads(line))

    def extract(self):
        seq = []
        rtt_trend = []
        health_trend = []

        for e in self.events:
            seq.append(e["event"])

            if "rtt_smoothed_ms" in e:
                rtt_trend.append(e["rtt_smoothed_ms"])

            if "health_score" in e:
                health_trend.append(e["health_score"])

        # Normalize trends
        def normalize(values):
            if not values:
                return []
            base = values[0]
            return [round(v - base, 2) for v in values]

        rtt_norm = normalize(rtt_trend)
        health_norm = normalize(health_trend)

        # Build raw signature string
        raw = json.dumps({
            "seq": seq,
            "rtt": rtt_norm,
            "health": health_norm
        })

        # Hash signature
        signature = hashlib.sha256(raw.encode()).hexdigest()

        result = {
            "signature": signature,
            "events": len(seq),
            "rtt_points": len(rtt_norm),
            "health_points": len(health_norm)
        }

        with open(self.output_path, "w") as f:
            json.dump(result, f, indent=2)

        return self.output_path