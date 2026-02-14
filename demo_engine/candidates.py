class CandidateGenerator:
    """
    Generates candidate transports for reattachment.
    """

    def list_candidates(self):
        return ["udp:A", "udp:B", "udp:C"]