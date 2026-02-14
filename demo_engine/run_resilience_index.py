from resilience_index import ResilienceIndex

if __name__ == "__main__":
    ri = ResilienceIndex("demo_output.jsonl")
    ri.load()
    path = ri.compute()
    print(f"Resilience index generated: {path}")