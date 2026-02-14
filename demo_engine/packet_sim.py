import random

class PacketSimulator:
    """
    Simulates packet-level behavior:
    - loss
    - delay
    - reordering
    """

    def __init__(self, loss_rate=0.05, reorder_rate=0.02, delay_min=5, delay_max=50):
        self.loss_rate = loss_rate
        self.reorder_rate = reorder_rate
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.buffer = []

    def send_packet(self, packet_id: int):
        # Loss
        if random.random() < self.loss_rate:
            return None  # packet lost

        # Delay
        delay = random.randint(self.delay_min, self.delay_max)

        # Reordering
        if random.random() < self.reorder_rate:
            self.buffer.insert(0, (packet_id, delay))
        else:
            self.buffer.append((packet_id, delay))

        return True

    def flush(self):
        """
        Returns packets in the order they are delivered.
        """
        delivered = sorted(self.buffer, key=lambda x: x[1])
        self.buffer = []
        return delivered