class State:
    BIRTH = "BIRTH"
    ATTACHED = "ATTACHED"
    VOLATILE = "VOLATILE"
    DEGRADED = "DEGRADED"
    REATTACHING = "REATTACHING"
    RECOVERING = "RECOVERING"
    TERMINATED = "TERMINATED"


ALLOWED_TRANSITIONS = {
    State.BIRTH: [State.ATTACHED],
    State.ATTACHED: [State.VOLATILE, State.TERMINATED],
    State.VOLATILE: [State.DEGRADED, State.ATTACHED, State.TERMINATED],
    State.DEGRADED: [State.REATTACHING, State.TERMINATED],
    State.REATTACHING: [State.RECOVERING, State.TERMINATED],
    State.RECOVERING: [State.ATTACHED, State.TERMINATED],
}


class StateMachine:
    def __init__(self):
        self.state = State.BIRTH
        self.state_version = 0

    def transition(self, new_state: str, reason: str):
        if new_state not in ALLOWED_TRANSITIONS.get(self.state, []):
            raise ValueError(f"Illegal transition {self.state} -> {new_state}")

        old_state = self.state
        self.state = new_state
        self.state_version += 1

        return {
            "from": old_state,
            "to": new_state,
            "reason": reason,
            "state_version": self.state_version
        }