from anomaly_detector import AnomalyDetector

if __name__ == "__main__":
    det = AnomalyDetector("demo_output.jsonl")
    path = det.detect()
    print(f"Anomaly report saved to {path}")