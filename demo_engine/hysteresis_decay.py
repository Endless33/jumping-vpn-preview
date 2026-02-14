class HysteresisDecay:
    """
    Gradually reduces hysteresis margin over time.
    Prevents the system from being stuck on a bad path forever.
    """

    def __init__(self, initial_margin: float = 5.0, decay_rate: float = 0.1, min_margin: float = 1.0):
        self.margin = initial_margin
        self.decay_rate = decay_rate
        self.min_margin = min_margin

    def tick(self):
        """
        Decays the margin slightly each cycle.
        """
        self.margin = max(self.min_margin, self.margin - self.decay_rate)

    def get_margin(self) -> float:
        return round(self.margin, 2)