from latency_profile import LatencyProfile

if __name__ == "__main__":
    lp = LatencyProfile("demo_output.jsonl")
    path = lp.generate()
    print(f"Latency profile generated: {path}")