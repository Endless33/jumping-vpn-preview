from engine import DemoEngine
from seed import DeterministicSeed

if __name__ == "__main__":
    DeterministicSeed(9999).apply()
    engine = DemoEngine("seeded", "seeded_output.jsonl")
    engine.run()
    print("Deterministic run complete: seeded_output.jsonl")