from .events import Event
from .state_machine import StateMachine, State
from .emitter import Emitter
from .volatility import VolatilitySimulator
from .policy import Policy
from .scoring import Scoring
from .candidates import CandidateGenerator


class DemoEngine:
    def __init__(self, session_id: str, output_path: str):
        self.session_id = session_id
        self.ts = 0
        self.sm = StateMachine()
        self.emitter = Emitter(output_path)
        self.vol = VolatilitySimulator()
        self.policy = Policy()
        self.scoring = Scoring()
        self.candidates = CandidateGenerator()

    def tick(self, ms: int):
        self.ts += ms

    def emit(self, event: str, **data):
        ev = Event(
            ts_ms=self.ts,
            event=event,
            session_id=self.session_id,
            data=data
        )
        self.emitter.emit(ev)

    def run(self):
        # PHASE 1 — BIRTH → ATTACHED
        self.sm.transition(State.ATTACHED, "initial_attach")
        self.emit("SESSION_CREATED", state="ATTACHED")

        # PHASE 2 — VOLATILITY
        self.tick(5000)
        loss = self.vol.loss_spike()
        jitter = self.vol.jitter_spike()
        rtt = self.vol.rtt_spike()

        self.sm.transition(State.VOLATILE, "loss_threshold_exceeded")
        self.emit("VOLATILITY_SIGNAL", loss_pct=loss, jitter_ms=jitter, rtt_ms=rtt)

        # PHASE 3 — DEGRADED
        if self.policy.allow_switch(loss):
            self.tick(1000)
            self.sm.transition(State.DEGRADED, "quality_below_threshold")
            self.emit("DEGRADED_ENTERED")

        # PHASE 4 — MULTIPATH SCORING
        cand_list = self.candidates.list_candidates()
        cand_scores = {}

        for c in cand_list:
            cand_scores[c] = self.scoring.score(loss, jitter, rtt)

        best = self.scoring.pick_best(cand_scores)

        self.emit("CANDIDATE_SCORES", scores=cand_scores)
        self.emit("BEST_CANDIDATE_SELECTED", candidate=best)

        # PHASE 5 — REATTACHING
        self.tick(1000)
        self.emit("REATTACH_REQUEST", candidate=best)
        self.emit("REATTACH_PROOF", proof="ok")
        self.sm.transition(State.REATTACHING, "preferred_path_changed")
        self.emit("TRANSPORT_SWITCH", from_="udp:A", to=best)

        # PHASE 6 — RECOVERING
        self.tick(2000)
        self.sm.transition(State.RECOVERING, "new_transport_validated")
        self.emit("RECOVERY_SIGNAL")

        # PHASE 7 — BACK TO ATTACHED
        if self.policy.allow_recovery(rtt):
            self.tick(2000)
            self.sm.transition(State.ATTACHED, "metrics_stabilized")
            self.emit("ATTACHED_RESTORED")

        self.emitter.close()