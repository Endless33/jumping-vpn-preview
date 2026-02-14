from engine import DemoEngine

class LongSessionSimulator:
    """
    Runs the engine for extended durations by looping run() multiple times.
    """

    def __init__(self, session_id="long", output="long_output.jsonl", cycles=5):
        self.session_id = session_id
        self.output = output
        self.cycles = cycles

    def run(self):
        engine = DemoEngine(self.session_id, self.output)
        for _ in range(self.cycles):
            engine.run()
        return self.output