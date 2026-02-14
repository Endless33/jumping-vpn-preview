import json
from collections import Counter

class EventHeatmap:
    """
    Produces a frequency map of events for heatmap visualization.
    """

    def __init__(self, input_path: str, output_path: str = "EVENT_HEATMAP.json"):
        self.input_path = input_path
        self.output_path = output_path

    def generate(self):
        counter = Counter()
        with open(self.input_path, "r") as f:
            for line in f:
                e = json.loads(line)
                counter[e["event"]] += 1

        with open(self.output_path, "w") as f:
            json.dump(counter, f, indent=2)

        return self.output_path