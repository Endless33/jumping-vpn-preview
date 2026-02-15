import time
import random
from datetime import datetime


class Session:
    def __init__(self, session_id):
        self.session_id = session_id
        self.state = "ATTACHED"
        self.transport = "udp:A"
        self.cwnd = 64
        self.rtt = 24
        self.loss = 0.0


def now():
    return datetime.now().strftime("%H:%M:%S")


def log(event, details=""):
    print(f"[{now()}] {event:<20} {details}")


def simulate():
    session = Session("DEMO-SESSION")

    log("SESSION_CREATED", f"id={session.session_id}")
    time.sleep(1)

    log("PATH_SELECTED", f"path={session.transport} rtt={session.rtt}ms cwnd={session.cwnd}")
    time.sleep(1)

    # Normal telemetry
    for i in range(3):
        session.rtt += random.randint(-1, 2)
        log("TELEMETRY", f"path={session.transport} rtt={session.rtt}ms loss={session.loss}% cwnd={session.cwnd}")
        time.sleep(1)

    # Loss spike
    session.loss = 8.2
    session.rtt = 42
    session.state = "VOLATILE"

    log("VOLATILITY_SIGNAL", f"loss spike detected loss={session.loss}% rtt={session.rtt}ms")
    time.sleep(1)

    # Flow control reacts
    session.cwnd = int(session.cwnd / 2)
    log("FLOW_CONTROL_UPDATE", f"cwnd reduced to {session.cwnd}")
    time.sleep(1)

    # Transport switch
    old = session.transport
    session.transport = "udp:B"

    log("TRANSPORT_SWITCH", f"{old} → {session.transport}")
    time.sleep(1)

    # Recovery
    session.state = "RECOVERING"
    session.loss = 0.4
    session.rtt = 26

    log("STATE_CHANGE", "RECOVERING")
    time.sleep(1)

    session.state = "ATTACHED"
    session.cwnd = 52

    log("STATE_CHANGE", "ATTACHED (session continuity preserved)")
    time.sleep(1)

    log("SESSION_ALIVE", f"id={session.session_id} transport={session.transport}")


if __name__ == "__main__":
    print("\nJumping VPN Live Demo\n")
    simulate()
    print("\nDemo complete.\n")