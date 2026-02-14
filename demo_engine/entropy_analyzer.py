import json
import math
from collections import Counter

class EntropyAnalyzer:
    """
    Computes Shannon entropy of event distribution.
    Measures unpredictability of protocol behavior.
    """

    def __init__(self, input_path: str, output_path: str = "ENTROPY.json"):
        self.input_path = input_path
        self.output_path = output_path

    def compute_entropy(self, counts):
        total = sum(counts.values())
        if total == 0:
            return 0.0
        entropy = 0.0
        for c in counts.values():
            p = c / total
            entropy -= p * math.log2(p)
        return round(entropy, 4)

    def analyze(self):
        counter = Counter()
        with open(self.input_path, "r") as f:
            for line in f:
                e = json.loads(line)
                counter[e["event"]] += 1

        entropy = self.compute_entropy(counter)

        result = {
            "entropy": entropy,
            "event_distribution": dict(counter)
        }

        with open(self.output_path, "w") as f:
            json.dump(result, f, indent=2)

        return self.output_path