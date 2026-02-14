class SessionLifetime:
    """
    Models session lifetime, heartbeats, and expiry.
    """

    def __init__(self, max_lifetime_ms: int = 30000, heartbeat_interval_ms: int = 3000):
        self.max_lifetime_ms = max_lifetime_ms
        self.heartbeat_interval_ms = heartbeat_interval_ms
        self.elapsed = 0
        self.next_heartbeat = heartbeat_interval_ms

    def tick(self, ms: int):
        self.elapsed += ms

    def should_heartbeat(self) -> bool:
        return self.elapsed >= self.next_heartbeat

    def consume_heartbeat(self):
        self.next_heartbeat += self.heartbeat_interval_ms

    def expired(self) -> bool:
        return self.elapsed >= self.max_lifetime_ms