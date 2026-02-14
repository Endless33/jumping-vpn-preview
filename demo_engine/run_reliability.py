from reliability import ReliabilityScore

if __name__ == "__main__":
    r = ReliabilityScore("demo_output.jsonl")
    path = r.compute()
    print(f"Reliability score saved to {path}")