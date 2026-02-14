class LossSwitchLogic:
    """
    Loss-based switching logic.
    Switch only if loss exceeds threshold.
    """

    def __init__(self, loss_threshold_pct: float = 5.0):
        self.loss_threshold = loss_threshold_pct

    def should_switch(self, loss_pct: float) -> bool:
        return loss_pct >= self.loss_threshold