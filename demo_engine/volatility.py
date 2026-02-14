import random

class VolatilitySimulator:
    def __init__(self, loss_min=1.0, loss_max=12.0):
        self.loss_min = loss_min
        self.loss_max = loss_max

    def loss_spike(self):
        return round(random.uniform(self.loss_min, self.loss_max), 2)

    def jitter_spike(self):
        return round(random.uniform(5.0, 40.0), 2)

    def rtt_spike(self):
        return round(random.uniform(80.0, 350.0), 2)