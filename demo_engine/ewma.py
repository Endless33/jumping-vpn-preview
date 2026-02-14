class EWMA:
    """
    Exponential Weighted Moving Average for RTT smoothing.
    """

    def __init__(self, alpha: float = 0.2):
        self.alpha = alpha
        self.value = None

    def update(self, sample: float):
        if self.value is None:
            self.value = sample
        else:
            self.value = self.alpha * sample + (1 - self.alpha) * self.value

    def get(self):
        return round(self.value, 2) if self.value is not None else None