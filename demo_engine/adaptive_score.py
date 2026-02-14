class AdaptiveScore:
    """
    Adaptive scoring model.
    Adjusts scoring weights based on historical performance.
    """

    def __init__(self):
        self.history = []
        self.alpha = 0.1  # learning rate
        self.loss_weight = 2.0
        self.jitter_weight = 0.3
        self.rtt_weight = 0.1

    def update_history(self, loss: float, jitter: float, rtt: float):
        self.history.append((loss, jitter, rtt))
        if len(self.history) > 50:
            self.history.pop(0)

    def adapt(self):
        """
        Adjust weights based on historical averages.
        """
        if not self.history:
            return

        avg_loss = sum(h[0] for h in self.history) / len(self.history)
        avg_jitter = sum(h[1] for h in self.history) / len(self.history)
        avg_rtt = sum(h[2] for h in self.history) / len(self.history)

        # Increase weight for metrics that are consistently bad
        self.loss_weight += self.alpha * (avg_loss / 10)
        self.jitter_weight += self.alpha * (avg_jitter / 50)
        self.rtt_weight += self.alpha * (avg_rtt / 200)

    def score(self, loss: float, jitter: float, rtt: float) -> float:
        """
        Adaptive scoring formula.
        """
        base = 100.0
        base -= loss * self.loss_weight
        base -= jitter * self.jitter_weight
        base -= rtt * self.rtt_weight
        return round(base, 2)