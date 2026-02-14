from timeline_generator import TimelineGenerator

if __name__ == "__main__":
    gen = TimelineGenerator("demo_output.jsonl", "DEMO_TIMELINE.jsonl")
    gen.generate()
    print("DEMO_TIMELINE.jsonl generated.")