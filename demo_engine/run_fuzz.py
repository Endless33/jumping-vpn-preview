from engine import DemoEngine
from fuzz import FuzzMode

if __name__ == "__main__":
    engine = DemoEngine("fuzz", "fuzz_output.jsonl")
    fuzz = FuzzMode(engine)
    fuzz.apply()
    engine.run()
    print("Fuzz run completed: fuzz_output.jsonl")