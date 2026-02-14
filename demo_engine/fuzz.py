import random

class FuzzMode:
    """
    Randomizes volatility and packet behavior for stress testing.
    """

    def __init__(self, engine):
        self.engine = engine

    def apply(self):
        # Randomize volatility ranges
        self.engine.vol.loss_min = random.uniform(0, 5)
        self.engine.vol.loss_max = random.uniform(5, 20)
        self.engine.vol.jitter_min = random.uniform(5, 20)
        self.engine.vol.jitter_max = random.uniform(20, 80)

        # Randomize packet simulator
        self.engine.packets.loss_rate = random.uniform(0.01, 0.2)
        self.engine.packets.reorder_rate = random.uniform(0.01, 0.1)
        self.engine.packets.delay_min = random.randint(1, 20)
        self.engine.packets.delay_max = random.randint(20, 120)