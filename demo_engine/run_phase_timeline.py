from phase_timeline import PhaseTimeline

if __name__ == "__main__":
    pt = PhaseTimeline("demo_output.jsonl")
    path = pt.generate()
    print(f"Phase timeline generated: {path}")