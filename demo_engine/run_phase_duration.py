from phase_duration import PhaseDurationCalculator

if __name__ == "__main__":
    calc = PhaseDurationCalculator("demo_output.jsonl")
    path = calc.generate()
    print(f"Phase duration report saved to {path}")