from stability_classifier import StabilityClassifier

if __name__ == "__main__":
    sc = StabilityClassifier("demo_output.jsonl")
    path = sc.classify()
    print(f"Stability classification saved to {path}")