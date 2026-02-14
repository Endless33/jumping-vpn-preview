import random

class DeterministicSeed:
    """
    Injects a deterministic seed into all random components.
    Ensures reproducible runs.
    """

    def __init__(self, seed: int = 12345):
        self.seed = seed

    def apply(self):
        random.seed(self.seed)