class CandidateWeights:
    """
    Assigns static or dynamic weights to candidate transports.
    Higher weight = more preferred.
    """

    def __init__(self):
        # Static weights for demo purposes
        self.weights = {
            "udp:A": 1.0,
            "udp:B": 1.2,
            "udp:C": 0.9
        }

    def get_weight(self, candidate: str) -> float:
        return self.weights.get(candidate, 1.0)

    def apply(self, scores: dict) -> dict:
        """
        Applies weights to raw scores.
        weighted_score = raw_score * weight
        """
        weighted = {}
        for cand, score in scores.items():
            w = self.get_weight(cand)
            weighted[cand] = round(score * w, 2)
        return weighted