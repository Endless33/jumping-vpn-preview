class DemoScenario:
    """
    Defines a scenario configuration for the demo engine.
    """

    def __init__(self, name: str, loss_min: float, loss_max: float, jitter_min: float, jitter_max: float):
        self.name = name
        self.loss_min = loss_min
        self.loss_max = loss_max
        self.jitter_min = jitter_min
        self.jitter_max = jitter_max

    def apply(self, engine):
        """
        Applies scenario parameters to the engine's volatility simulator.
        """
        engine.vol.loss_min = self.loss_min
        engine.vol.loss_max = self.loss_max
        engine.vol.jitter_min = self.jitter_min
        engine.vol.jitter_max = self.jitter_max