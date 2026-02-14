from behavior_signature import BehavioralSignature

if __name__ == "__main__":
    bs = BehavioralSignature("demo_output.jsonl")
    bs.load()
    path = bs.extract()
    print(f"Behavioral signature generated: {path}")