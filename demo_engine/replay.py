import json

class DeterministicReplay:
    """
    Replays a demo_output.jsonl file deterministically.
    Emits events in the exact same order with the same timestamps.
    """

    def __init__(self, input_path: str):
        self.input_path = input_path
        self.events = []

    def load(self):
        with open(self.input_path, "r") as f:
            for line in f:
                self.events.append(json.loads(line))

    def replay(self):
        """
        Returns events in deterministic order.
        """
        return sorted(self.events, key=lambda e: e["ts_ms"])