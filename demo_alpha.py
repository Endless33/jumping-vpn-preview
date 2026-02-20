# demo_alpha.py
from jumping_vpn.session_manager import SessionManager
from jumping_vpn.transport_tcp import TCPTransport
from jumping_vpn.transport_udp import UDPTransport


def main() -> None:
    sm = SessionManager()

    # Create identity first (above transport)
    session = sm.create_session()
    expected_key = session.continuity_key

    # Attach TCP first
    tcp = TCPTransport("127.0.0.1", 9999)  # port doesn't need to be open for the demo logic
    try:
        # If no server is listening, connect will fail, but we can still show attach conceptually
        tcp.attach(sm, session)
    except Exception:
        # Still demonstrate state machine behaviour even if endpoint isn't available
        sm.mark_degraded(session, reason="tcp_connect_failed")
        sm.detach_transport(session, reason="tcp_unreachable")

    # Switch to UDP
    udp = UDPTransport("127.0.0.1", 9998)
    udp.attach(sm, session)

    # Verify continuity didn't change
    sm.continuity_verified(session, expected_key)

    print("\n=== EARLY ALPHA TRACE ===")
    for e in session.trace:
        print(e)

    print("\nSession identity (continuity_key) stayed the same.")
    print("Current transport:", session.transport_label)


if __name__ == "__main__":
    main()