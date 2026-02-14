import os
import shutil

class EcosystemPackager:
    """
    Collects all demo artifacts into a single folder.
    """

    def __init__(self, output_dir="DEMO_ECOSYSTEM"):
        self.output_dir = output_dir

    def package(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)

        artifacts = [
            "demo_output.jsonl",
            "DEMO_TIMELINE.jsonl",
            "DEMO_METRICS.json",
            "SCENARIO_SUMMARY.json",
            "DEMO_REPORT.md",
            "SPEC_MAP.md",
            "EVENT_HEATMAP.json",
            "LATENCY_PROFILE.json",
            "PERF_PROFILE.json",
            "PHASE_TIMELINE.json",
            "PHASE_DURATION.json",
            "ANOMALIES.json",
            "RELIABILITY.json",
            "CHAOS_RECOVERY.json"
        ]

        for a in artifacts:
            if os.path.exists(a):
                shutil.copy(a, os.path.join(self.output_dir, a))

        return self.output_dir