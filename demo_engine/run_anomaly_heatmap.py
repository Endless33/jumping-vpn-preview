from anomaly_heatmap import AnomalyHeatmap

if __name__ == "__main__":
    ah = AnomalyHeatmap("demo_output.jsonl")
    ah.load()
    path = ah.generate()
    print(f"Anomaly heatmap generated: {path}")