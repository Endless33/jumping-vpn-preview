import json

class DashboardGenerator:
    """
    Combines all demo artifacts into a single dashboard JSON.
    """

    def __init__(self,
                 metrics_path="DEMO_METRICS.json",
                 summary_path="SCENARIO_SUMMARY.json",
                 spec_path="SPEC_MAP.md",
                 timeline_path="DEMO_TIMELINE.jsonl",
                 output_path="DEMO_DASHBOARD.json"):
        self.metrics_path = metrics_path
        self.summary_path = summary_path
        self.spec_path = spec_path
        self.timeline_path = timeline_path
        self.output_path = output_path

    def load_json(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def load_timeline(self):
        with open(self.timeline_path, "r") as f:
            return [json.loads(line) for line in f]

    def load_spec_map(self):
        with open(self.spec_path, "r") as f:
            return f.read()

    def generate(self):
        dashboard = {
            "metrics": self.load_json(self.metrics_path),
            "scenario_summary": self.load_json(self.summary_path),
            "timeline": self.load_timeline(),
            "spec_map": self.load_spec_map()
        }

        with open(self.output_path, "w") as f:
            json.dump(dashboard, f, indent=2)

        return self.output_path