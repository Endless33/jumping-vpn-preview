import json

class ReportGenerator:
    """
    Generates a Markdown report from SCENARIO_SUMMARY.json.
    """

    def __init__(self, summary_path: str, output_path: str = "DEMO_REPORT.md"):
        self.summary_path = summary_path
        self.output_path = output_path

    def generate(self):
        with open(self.summary_path, "r") as f:
            data = json.load(f)

        lines = []
        lines.append("# Demo Scenario Report\n")
        lines.append("This report summarizes all executed demo scenarios.\n")
        lines.append("## Summary Table\n")
        lines.append("| Scenario | Events | Switches | Lost Packets | Delivered | Avg RTT | Avg Health |")
        lines.append("|----------|--------|----------|--------------|-----------|---------|------------|")

        for name, stats in data.items():
            lines.append(
                f"| {name} | {stats['total_events']} | {stats['switches']} | "
                f"{stats['loss_events']} | {stats['delivered_packets']} | "
                f"{stats['avg_smoothed_rtt']} | {stats['avg_health_score']} |"
            )

        with open(self.output_path, "w") as f:
            f.write("\n".join(lines))

        return self.output_path