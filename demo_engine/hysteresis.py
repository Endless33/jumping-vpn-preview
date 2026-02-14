class Hysteresis:
    """
    Prevents rapid switching between transports.
    A candidate must exceed the current path score by a margin.
    """

    def __init__(self, margin: float = 5.0):
        self.margin = margin
        self.last_score = None

    def allow_switch(self, current_score: float, new_score: float) -> bool:
        """
        Returns True only if new_score is sufficiently better.
        """
        if self.last_score is None:
            self.last_score = current_score
            return True

        if new_score >= self.last_score + self.margin:
            self.last_score = new_score
            return True

        return False