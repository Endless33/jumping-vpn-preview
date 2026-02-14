import os
from engine import DemoEngine
from scenario import DemoScenario

class ScenarioRunner:
    """
    Runs multiple demo scenarios and produces separate outputs.
    """

    def __init__(self, output_dir: str = "scenarios"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def run_scenario(self, scenario: DemoScenario):
        output_path = os.path.join(self.output_dir, f"{scenario.name}.jsonl")
        engine = DemoEngine(session_id=scenario.name, output_path=output_path)
        scenario.apply(engine)
        engine.run()
        return output_path

    def run_all(self, scenarios):
        results = []
        for s in scenarios:
            path = self.run_scenario(s)
            results.append((s.name, path))
        return results