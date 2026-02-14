from engine import DemoEngine
from chaos import ChaosMode

if __name__ == "__main__":
    engine = DemoEngine("chaos", "chaos_output.jsonl")
    ChaosMode(engine).apply()
    engine.run()
    print("Chaos-mode run complete: chaos_output.jsonl")