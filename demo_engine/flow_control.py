class FlowControl:
    """
    Minimal flow-control model for demo purposes.
    Models cwnd (congestion window) and pacing rate.
    """

    def __init__(self):
        self.cwnd = 10.0          # packets
        self.pacing_rate = 1.0    # packets/ms

    def degrade(self, loss_pct: float):
        """
        Loss increases → reduce cwnd and pacing.
        """
        self.cwnd = max(1.0, self.cwnd * (1.0 - loss_pct / 100.0))
        self.pacing_rate = max(0.1, self.pacing_rate * (1.0 - loss_pct / 120.0))

    def recover(self):
        """
        Recovery window → slowly restore cwnd and pacing.
        """
        self.cwnd = min(10.0, self.cwnd + 0.5)
        self.pacing_rate = min(1.0, self.pacing_rate + 0.05)

    def snapshot(self):
        return {
            "cwnd": round(self.cwnd, 2),
            "pacing_rate": round(self.pacing_rate, 3)
        }