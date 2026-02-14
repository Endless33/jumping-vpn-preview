from scenario_runner import ScenarioRunner
from scenario import DemoScenario

if __name__ == "__main__":
    runner = ScenarioRunner()

    scenarios = [
        DemoScenario("scenario_low_loss", 1.0, 3.0, 5.0, 15.0),
        DemoScenario("scenario_medium_loss", 3.0, 7.0, 10.0, 25.0),
        DemoScenario("scenario_high_loss", 7.0, 12.0, 20.0, 40.0)
    ]

    results = runner.run_all(scenarios)

    print("Scenarios completed:")
    for name, path in results:
        print(f" - {name}: {path}")