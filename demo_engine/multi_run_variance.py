import json
import glob

class MultiRunVariance:
    """
    Computes variance across multiple demo runs.
    """

    def __init__(self, runs_dir="scenarios", output_path="MULTI_RUN_VARIANCE.json"):
        self.runs_dir = runs_dir
        self.output_path = output_path

    def load_runs(self):
        files = glob.glob(f"{self.runs_dir}/*.jsonl")
        runs = []
        for f in files:
            with open(f, "r") as fd:
                events = [json.loads(line) for line in fd]
                runs.append(events)
        return runs

    def compute(self):
        runs = self.load_runs()
        if not runs:
            return None

        def avg(values):
            return sum(values) / len(values) if values else 0

        switch_counts = [len([e for e in r if e["event"] == "TRANSPORT_SWITCH"]) for r in runs]
        loss_counts = [len([e for e in r if e["event"] == "PACKET_LOST"]) for r in runs]

        def variance(values):
            if len(values) < 2:
                return 0.0
            m = avg(values)
            return sum((v - m) ** 2 for v in values) / len(values)

        result = {
            "switch_variance": variance(switch_counts),
            "loss_variance": variance(loss_counts),
            "runs_analyzed": len(runs)
        }

        with open(self.output_path, "w") as f:
            json.dump(result, f, indent=2)

        return self.output_path