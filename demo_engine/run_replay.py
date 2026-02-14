from replay import DeterministicReplay

if __name__ == "__main__":
    rep = DeterministicReplay("demo_output.jsonl")
    rep.load()
    events = rep.replay()

    for e in events:
        print(json.dumps(e))