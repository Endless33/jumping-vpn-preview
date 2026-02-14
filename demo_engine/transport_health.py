from .ewma import EWMA

class TransportHealth:
    """
    Models health of a transport path with RTT smoothing.
    """

    def __init__(self):
        self.loss = 0.0
        self.jitter = 0.0
        self.rtt_raw = 0.0
        self.rtt_smoothed = EWMA(alpha=0.25)
        self.score = 100.0

    def update(self, loss: float, jitter: float, rtt: float):
        self.loss = loss
        self.jitter = jitter
        self.rtt_raw = rtt

        # Update smoothed RTT
        self.rtt_smoothed.update(rtt)

        # Scoring model uses smoothed RTT
        score = 100.0
        score -= loss * 2.0
        score -= jitter * 0.3
        score -= self.rtt_smoothed.get() * 0.1

        self.score = round(score, 2)

    def snapshot(self):
        return {
            "loss_pct": self.loss,
            "jitter_ms": self.jitter,
            "rtt_raw_ms": self.rtt_raw,
            "rtt_smoothed_ms": self.rtt_smoothed.get(),
            "health_score": self.score
        }