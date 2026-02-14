from .randomness import DeterministicRandom

class VolatilitySimulator:
    def __init__(self, loss_min=1.0, loss_max=12.0):
        self.rng = DeterministicRandom(seed=1337)
        self.loss_min = loss_min
        self.loss_max = loss_max

    def loss_spike(self):
        return round(self.rng.rand(self.loss_min, self.loss_max), 2)

    def jitter_spike(self):
        return round(self.rng.rand(5.0, 40.0), 2)

    def rtt_spike(self):
        return round(self.rng.rand(80.0, 350.0), 2)