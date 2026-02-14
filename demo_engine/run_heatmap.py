from heatmap import EventHeatmap

if __name__ == "__main__":
    hm = EventHeatmap("demo_output.jsonl")
    path = hm.generate()
    print(f"Heatmap generated: {path}")