class DelaySwitchLogic:
    """
    Delay-based switching logic.
    Switch only if smoothed RTT is above threshold.
    """

    def __init__(self, rtt_threshold_ms: float = 180.0):
        self.rtt_threshold = rtt_threshold_ms

    def should_switch(self, smoothed_rtt: float) -> bool:
        return smoothed_rtt >= self.rtt_threshold