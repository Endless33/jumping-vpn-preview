from .events import Event
from .state_machine import StateMachine, State
from .emitter import Emitter
from .volatility import VolatilitySimulator
from .policy import Policy
from .scoring import Scoring
from .candidates import CandidateGenerator
from .audit import Audit
from .recovery import RecoveryWindow
from .flow_control import FlowControl


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
        self.audit = Audit()
        self.recovery = RecoveryWindow(window_ms=2000)
        self.flow = FlowControl()

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
        self.emit("SESSION_CREATED", state="ATTACHED", **self.flow.snapshot())

        # PHASE 2 — VOLATILITY
        self.tick(5000)
        loss = self.vol.loss_spike()
        jitter = self.vol.jitter_spike()
        rtt = self.vol.rtt_spike()

        self.flow.degrade(loss)

        self.sm.transition(State.VOLATILE, "loss_threshold_exceeded")
        self.emit("VOLATILITY_SIGNAL",
                  loss_pct=loss,
                  jitter_ms=jitter,
                  rtt_ms=rtt,
                  **self.flow.snapshot())

        # PHASE 3 — DEGRADED
        if self.policy.allow_switch(loss):
            self.tick(1000)
            self.sm.transition(State.DEGRADED, "quality_below_threshold")
            self.emit("DEGRADED_ENTERED", **self.flow.snapshot())

        # PHASE 4 — MULTIPATH SCORING
        cand_list = self.candidates.list_candidates()
        cand_scores = {c: self.scoring.score(loss, jitter, rtt) for c in cand_list}
        best = self.scoring.pick_best(cand_scores)

        self.emit("CANDIDATE_SCORES", scores=cand_scores)
        self.emit("BEST_CANDIDATE_SELECTED", candidate=best)

        # PHASE 5 — AUDIT BEFORE SWITCH
        identity_ok = self.audit.check_identity_reset(self.session_id, self.session_id)
        dual_ok = self.audit.check_dual_binding(["udp:A"])

        self.emit("AUDIT_EVENT", identity_ok=identity_ok, dual_binding_ok=dual_ok)

        # PHASE 6 — REATTACHING
        self.tick(1000)
        self.emit("REATTACH_REQUEST", candidate=best)
        self.emit("REATTACH_PROOF", proof="ok")
        self.sm.transition(State.REATTACHING, "preferred_path_changed")
        self.emit("TRANSPORT_SWITCH", from_="udp:A", to=best)

        # PHASE 7 — RECOVERING
        self.tick(500)
        self.sm.transition(State.RECOVERING, "new_transport_validated")
        self.emit("RECOVERY_SIGNAL", **self.flow.snapshot())

        # PHASE 8 — RECOVERY WINDOW
        while not self.recovery.is_stable():
            self.tick(500)
            self.recovery.tick(500)
            self.flow.recover()
            self.emit("RECOVERY_PROGRESS",
                      elapsed_ms=self.recovery.elapsed,
                      **self.flow.snapshot())

        # PHASE 9 — BACK TO ATTACHED
        self.sm.transition(State.ATTACHED, "metrics_stabilized")
        self.emit("ATTACHED_RESTORED", **self.flow.snapshot())

        self.emitter.close()