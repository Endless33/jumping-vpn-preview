import random

class ChaosMode:
    """
    Extreme volatility + packet chaos.
    Used for stress testing and failure discovery.
    """

    def __init__(self, engine):
        self.engine = engine

    def apply(self):
        # Extreme volatility
        self.engine.vol.loss_min = random.uniform(5, 20)
        self.engine.vol.loss_max = random.uniform(20, 50)
        self.engine.vol.jitter_min = random.uniform(20, 60)
        self.engine.vol.jitter_max = random.uniform(60, 150)

        # Extreme packet chaos
        self.engine.packets.loss_rate = random.uniform(0.1, 0.4)
        self.engine.packets.reorder_rate = random.uniform(0.1, 0.3)
        self.engine.packets.delay_min = random.randint(10, 50)
        self.engine.packets.delay_max = random.randint(100, 300)