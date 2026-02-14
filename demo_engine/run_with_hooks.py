from engine import DemoEngine
from engine_hooks_patch import EngineHooksPatch

if __name__ == "__main__":
    engine = DemoEngine("hooks", "hooks_output.jsonl")
    EngineHooksPatch().attach(engine)

    # Example hook
    engine.hooks.add(lambda eng, ev: print(f"[HOOK] Event: {ev}"))

    engine.run()
    print("Run with evolution hooks complete.")