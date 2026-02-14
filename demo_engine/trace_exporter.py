import json

class TraceExporter:
    """
    Exports a compact trace for visualization tools.
    """

    def __init__(self, input_path: str, output_path: str = "DEMO_TRACE.json"):
        self.input_path = input_path
        self.output_path = output_path

    def export(self):
        trace = []
        with open(self.input_path, "r") as f:
            for line in f:
                e = json.loads(line)
                trace.append({
                    "t": e["ts_ms"],
                    "e": e["event"],
                    "h": e.get("health_score"),
                    "rtt": e.get("rtt_smoothed_ms"),
                    "loss": e.get("loss_pct")
                })

        with open(self.output_path, "w") as f:
            json.dump(trace, f, indent=2)

        return self.output_path