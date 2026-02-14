import random

class DeterministicRandom:
    def __init__(self, seed: int = 1337):
        random.seed(seed)

    def rand(self, a: float, b: float) -> float:
        return random.uniform(a, b)