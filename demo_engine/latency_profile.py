import json

class LatencyProfile:
    """
    Builds a latency profile from demo_output.jsonl.
    """

    def __init__(self, input_path: str, output_path: str = "LATENCY_PROFILE.json"):
        self.input_path = input_path
        self.output_path = output_path

    def generate(self):
        rtts = []
        with open(self.input_path, "r") as f:
            for line in f:
                e = json.loads(line)
                if "rtt_smoothed_ms" in e:
                    rtts.append(e["rtt_smoothed_ms"])

        profile = {
            "min_rtt": min(rtts) if rtts else None,
            "max_rtt": max(rtts) if rtts else None,
            "avg_rtt": round(sum(rtts) / len(rtts), 2) if rtts else None,
            "samples": len(rtts)
        }

        with open(self.output_path, "w") as f:
            json.dump(profile, f, indent=2)

        return self.output_path