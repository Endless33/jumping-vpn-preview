import os
from scenario_runner import ScenarioRunner
from scenario_summary import ScenarioSummary
from scenario import DemoScenario

class Orchestrator:
    """
    Runs multiple scenarios and produces a summary report.
    """

    def __init__(self, output_dir="scenarios", summary_path="SCENARIO_SUMMARY.json"):
        self.output_dir = output_dir
        self.summary_path = summary_path
        self.runner = ScenarioRunner(output_dir=output_dir)
        self.summary = ScenarioSummary()

    def run(self):
        scenarios = [
            DemoScenario("scenario_low_loss", 1.0, 3.0, 5.0, 15.0),
            DemoScenario("scenario_medium_loss", 3.0, 7.0, 10.0, 25.0),
            DemoScenario("scenario_high_loss", 7.0, 12.0, 20.0, 40.0),
            DemoScenario("scenario_extreme_loss", 10.0, 20.0, 30.0, 60.0),
        ]

        results = self.runner.run_all(scenarios)

        for name, path in results:
            self.summary.add_result(name, path)

        self.summary.export(self.summary_path)

        return self.summary_path