class TransportHealth:
    """
    Models health of a transport path.
    """

    def __init__(self):
        self.loss = 0.0
        self.jitter = 0.0
        self.rtt = 0.0
        self.score = 100.0

    def update(self, loss: float, jitter: float, rtt: float):
        self.loss = loss
        self.jitter = jitter
        self.rtt = rtt

        # Simple scoring model
        score = 100.0
        score -= loss * 2.0
        score -= jitter * 0.3
        score -= rtt * 0.1

        self.score = round(score, 2)

    def snapshot(self):
        return {
            "loss_pct": self.loss,
            "jitter_ms": self.jitter,
            "rtt_ms": self.rtt,
            "health_score": self.score
        }