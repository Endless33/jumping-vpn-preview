class Scoring:
    """
    Simple multipath scoring model.
    Higher score = better candidate.
    """

    def score(self, loss_pct: float, jitter_ms: float, rtt_ms: float) -> float:
        # Normalize metrics into a single score
        score = 100.0
        score -= loss_pct * 2.0
        score -= jitter_ms * 0.3
        score -= rtt_ms * 0.1
        return round(score, 2)

    def pick_best(self, candidates: dict) -> str:
        """
        candidates = {
            "udp:A": score,
            "udp:B": score,
            ...
        }
        """
        return max(candidates, key=candidates.get)