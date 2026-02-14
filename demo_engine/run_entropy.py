from entropy_analyzer import EntropyAnalyzer

if __name__ == "__main__":
    ea = EntropyAnalyzer("demo_output.jsonl")
    path = ea.analyze()
    print(f"Entropy analysis saved to {path}")