from metrics_collector import MetricsCollector

if __name__ == "__main__":
    collector = MetricsCollector("demo_output.jsonl")
    collector.load()
    metrics = collector.collect()
    path = collector.export("DEMO_METRICS.json")
    print(f"Metrics collected: {path}")