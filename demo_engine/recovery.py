class RecoveryWindow:
    """
    Models the recovery stabilization window after a transport switch.
    """

    def __init__(self, window_ms: int = 2000):
        self.window_ms = window_ms
        self.elapsed = 0

    def tick(self, ms: int):
        self.elapsed += ms

    def is_stable(self) -> bool:
        return self.elapsed >= self.window_ms