import json

class MutationLog:
    """
    Generates a mutation log based on behavioral changes in the demo output.
    Detects:
    - phase transitions
    - score jumps
    - RTT spikes
    - loss spikes
    - switching decisions
    """

    def __init__(self, input_path: str, output_path: str = "MUTATION_LOG.md"):
        self.input_path = input_path
        self.output_path = output_path
        self.events = []

    def load(self):
        with open(self.input_path, "r") as f:
            for line in f:
                self.events.append(json.loads(line))

    def generate(self):
        lines = []
        lines.append("# Mutation Log\n")
        lines.append("Behavioral mutations detected during session execution.\n")

        last_health = None
        last_rtt = None

        for e in self.events:
            ev = e["event"]

            # Phase transitions
            if ev in [
                "SESSION_CREATED",
                "VOLATILITY_SIGNAL",
                "DEGRADED_ENTERED",
                "BEST_CANDIDATE_SELECTED",
                "TRANSPORT_SWITCH",
                "RECOVERY_SIGNAL",
                "ATTACHED_RESTORED",
                "SESSION_EXPIRED"
            ]:
                lines.append(f"- **{ev}** @ {e['ts_ms']}ms")

            # Health mutation
            if "health_score" in e:
                if last_health is not None:
                    if abs(e["health_score"] - last_health) > 10:
                        lines.append(
                            f"- Health mutation: {last_health} → {e['health_score']} @ {e['ts_ms']}ms"
                        )
                last_health = e["health_score"]

            # RTT mutation
            if "rtt_smoothed_ms" in e:
                if last_rtt is not None:
                    if abs(e["rtt_smoothed_ms"] - last_rtt) > 50:
                        lines.append(
                            f"- RTT mutation: {last_rtt}ms → {e['rtt_smoothed_ms']}ms @ {e['ts_ms']}ms"
                        )
                last_rtt = e["rtt_smoothed_ms"]

            # Loss spike
            if "loss_pct" in e and e["loss_pct"] > 10:
                lines.append(f"- Loss spike: {e['loss_pct']}% @ {e['ts_ms']}ms")

            # Switch mutation
            if ev == "TRANSPORT_SWITCH":
                lines.append(
                    f"- Transport mutation: {e['data']['from_']} → {e['data']['to']} @ {e['ts_ms']}ms"
                )

        with open(self.output_path, "w") as f:
            f.write("\n".join(lines))

        return self.output_path