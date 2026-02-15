import json
import sys


class ReplayEngine:
    def __init__(self, trace_path: str):
        self.trace_path = trace_path
        self.events = []
        self.session_state = None
        self.transport = None

    def load(self):
        with open(self.trace_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.events.append(json.loads(line))

    def replay(self):
        print("=== Jumping VPN Replay ===")

        for event in self.events:
            name = event.get("event")

            if name == "SESSION_CREATED":
                self.session_state = event.get("state")
                print(f"[SESSION CREATED] state={self.session_state}")

            elif name == "PATH_SELECTED":
                self.transport = event.get("active_path")
                print(f"[PATH SELECTED] transport={self.transport}")

            elif name == "VOLATILITY_SIGNAL":
                reason = event.get("reason")
                print(f"[VOLATILITY] reason={reason}")

            elif name == "STATE_CHANGE":
                old = event.get("from")
                new = event.get("to")
                self.session_state = new
                print(f"[STATE] {old} → {new}")

            elif name == "TRANSPORT_SWITCH":
                old = event.get("from_path")
                new = event.get("to_path")
                self.transport = new
                print(f"[TRANSPORT SWITCH] {old} → {new}")

            elif name == "AUDIT_EVENT":
                check = event.get("check")
                result = event.get("result")
                print(f"[AUDIT] {check} = {result}")

        print("\nReplay complete.")
        print(f"Final state: {self.session_state}")
        print(f"Final transport: {self.transport}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python replay.py DEMO_TRACE.jsonl")
        return

    path = sys.argv[1]

    engine = ReplayEngine(path)
    engine.load()
    engine.replay()


if __name__ == "__main__":
    main()