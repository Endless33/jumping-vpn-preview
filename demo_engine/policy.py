class Policy:
    def allow_switch(self, loss_pct: float) -> bool:
        return loss_pct > 5.0

    def allow_recovery(self, rtt_ms: float) -> bool:
        return rtt_ms < 200.0