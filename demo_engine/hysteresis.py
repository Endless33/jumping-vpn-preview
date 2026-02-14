class Hysteresis:
    """
    Prevents rapid switching between transports.
    Now supports dynamic decay of the margin.
    """

    def __init__(self, margin: float = 5.0):
        self.margin = margin
        self.last_score = None

    def update_margin(self, new_margin: float):
        self.margin = new_margin

    def allow_switch(self, current_score: float, new_score: float) -> bool:
        if self.last_score is None:
            self.last_score = current_score
            return True

        if new_score >= self.last_score + self.margin:
            self.last_score = new_score
            return True

        return False