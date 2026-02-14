from engine import DemoEngine

if __name__ == "__main__":
    engine = DemoEngine(session_id="demo_s", output_path="demo_output.jsonl")
    engine.run()
    print("Demo completed.")