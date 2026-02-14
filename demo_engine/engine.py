from .events import Event
from .state_machine import StateMachine, State
from .emitter import Emitter
from .volatility import VolatilitySimulator
from .policy import Policy
from .scoring import Scoring
from .adaptive_score import AdaptiveScore
from .candidates import CandidateGenerator
from .audit import Audit
from .recovery import RecoveryWindow
from .flow_control import FlowControl
from .transport_health import TransportHealth
from .weights import CandidateWeights
from .session_lifetime import SessionLifetime
from .packet_sim import PacketSimulator
from .hysteresis import Hysteresis
from .hysteresis_decay import HysteresisDecay
from .delay_switch import DelaySwitchLogic
from .loss_switch import LossSwitchLogic


class DemoEngine:
    def __init__(self, session_id: str, output_path: str):
        self.session_id = session_id
        self.ts = 0
        self.sm = StateMachine()
        self.emitter = Emitter(output_path)
        self.vol = VolatilitySimulator()
        self.policy = Policy()
        self.scoring = Scoring()
        self.adaptive = AdaptiveScore()
        self.candidates = CandidateGenerator()
        self.audit = Audit()
        self.recovery = RecoveryWindow(window_ms=2000)
        self.flow = FlowControl()
        self.health = TransportHealth()
        self.weights = CandidateWeights()
        self.lifetime = SessionLifetime()
        self.packets = PacketSimulator()
        self.hysteresis = Hysteresis(margin=5.0)
        self.hysteresis_decay = HysteresisDecay(initial_margin=5.0, decay_rate=0.2, min_margin=1.0)
        self.delay_switch = DelaySwitchLogic(rtt_threshold_ms=180.0)
        self.loss_switch = LossSwitchLogic(loss_threshold_pct=5.0)

    def tick(self, ms: int):
        self.ts += ms
        self.lifetime.tick(ms)

        # decay hysteresis margin
        self.hysteresis_decay.tick()
        self.hysteresis.update_margin(self.hysteresis_decay.get_margin())

        if self.lifetime.should_heartbeat():
            self.emit("HEARTBEAT", lifetime_ms=self.lifetime.elapsed)
            self.lifetime.consume_heartbeat()

    def emit(self, event: str, **data):
        ev = Event(
            ts_ms=self.ts,
            event=event,
            session_id=self.session_id,
            data=data
        )
        self.emitter.emit(ev)

    def simulate_packets(self, count: int):
        for i in range(count):
            result = self.packets.send_packet(i)
            if result is None:
                self.emit("PACKET_LOST", packet_id=i)
        delivered = self.packets.flush()
        for packet_id, delay in delivered:
            self.emit("PACKET_DELIVERED", packet_id=packet_id, delay_ms=delay)

    def run(self):
        # PHASE 1 — BIRTH → ATTACHED
        self.sm.transition(State.ATTACHED, "initial_attach")
        self.emit("SESSION_CREATED", state="ATTACHED", **self.flow.snapshot())

        self.simulate_packets(5)

        # PHASE 2 — VOLATILITY
        self.tick(5000)
        loss = self.vol.loss_spike()
        jitter = self.vol.jitter_spike()
        rtt = self.vol.rtt_spike()

        self.flow.degrade(loss)
        self.health.update(loss, jitter, rtt)

        # update adaptive model
        self.adaptive.update_history(loss, jitter, rtt)
        self.adaptive.adapt()

        self.sm.transition(State.VOLATILE, "loss_threshold_exceeded")
        self.emit("VOLATILITY_SIGNAL",
                  **self.health.snapshot(),
                  **self.flow.snapshot(),
                  adaptive_weights={
                      "loss": self.adaptive.loss_weight,
                      "jitter": self.adaptive.jitter_weight,
                      "rtt": self.adaptive.rtt_weight
                  },
                  hysteresis_margin=self.hysteresis_decay.get_margin())

        self.simulate_packets(5)

        # PHASE 3 — DEGRADED
        if self.policy.allow_switch(loss):
            self.tick(1000)
            self.sm.transition(State.DEGRADED, "quality_below_threshold")
            self.emit("DEGRADED_ENTERED",
                      **self.health.snapshot(),
                      **self.flow.snapshot(),
                      adaptive_weights={
                          "loss": self.adaptive.loss_weight,
                          "jitter": self.adaptive.jitter_weight,
                          "rtt": self.adaptive.rtt_weight
                      },
                      hysteresis_margin=self.hysteresis_decay.get_margin())

        # PHASE 4 — MULTIPATH DECISION
        cand_list = self.candidates.list_candidates()

        # adaptive scoring
        adaptive_scores = {
            c: self.adaptive.score(loss, jitter, self.health.rtt_smoothed.get())
            for c in cand_list
        }

        weighted_scores = self.weights.apply(adaptive_scores)
        best = max(weighted_scores, key=weighted_scores.get)

        delay_ok = self.delay_switch.should_switch(self.health.rtt_smoothed.get())
        loss_ok = self.loss_switch.should_switch(loss)
        hysteresis_ok = self.hysteresis.allow_switch(self.health.score, weighted_scores[best])

        if not (delay_ok or loss_ok) or not hysteresis_ok:
            self.emit("SWITCH_BLOCKED",
                      candidate=best,
                      delay_ok=delay_ok,
                      loss_ok=loss_ok,
                      hysteresis_ok=hysteresis_ok,
                      hysteresis_margin=self.hysteresis_decay.get_margin())
            best = "udp:A"

        self.emit("CANDIDATE_SCORES_ADAPTIVE", scores=adaptive_scores)
        self.emit("CANDIDATE_SCORES_WEIGHTED", scores=weighted_scores)
        self.emit("BEST_CANDIDATE_SELECTED", candidate=best)

        # PHASE 5 — AUDIT
        identity_ok = self.audit.check_identity_reset(self.session_id, self.session_id)
        dual_ok = self.audit.check_dual_binding(["udp:A"])
        self.emit("AUDIT_EVENT", identity_ok=identity_ok, dual_binding_ok=dual_ok)

        # PHASE 6 — REATTACHING
        self.tick(1000)
        self.emit("REATTACH_REQUEST", candidate=best)
        self.emit("REATTACH_PROOF", proof="ok")
        self.sm.transition(State.REATTACHING, "preferred_path_changed")
        self.emit("TRANSPORT_SWITCH", from_="udp:A", to=best)

        self.simulate_packets(5)

        # PHASE 7 — RECOVERING
        self.tick(500)
        self.sm.transition(State.RECOVERING, "new_transport_validated")
        self.emit("RECOVERY_SIGNAL",
                  **self.health.snapshot(),
                  **self.flow.snapshot(),
                  adaptive_weights={
                      "loss": self.adaptive.loss_weight,
                      "jitter": self.adaptive.jitter_weight,
                      "rtt": self.adaptive.rtt_weight
                  },
                  hysteresis_margin=self.hysteresis_decay.get_margin())

        # PHASE 8 — RECOVERY WINDOW
        while not self.recovery.is_stable():
            self.tick(500)
            self.recovery.tick(500)
            self.flow.recover()
            self.emit("RECOVERY_PROGRESS",
                      elapsed_ms=self.recovery.elapsed,
                      **self.health.snapshot(),
                      **self.flow.snapshot(),
                      adaptive_weights={
                          "loss": self.adaptive.loss_weight,
                          "jitter": self.adaptive.jitter_weight,
                          "rtt": self.adaptive.rtt_weight
                      },
                      hysteresis_margin=self.hysteresis_decay.get_margin())

        # PHASE 9 — BACK TO ATTACHED
        self.sm.transition(State.ATTACHED, "metrics_stabilized")
        self.emit("ATTACHED_RESTORED",
                  **self.health.snapshot(),
                  **self.flow.snapshot(),
                  adaptive_weights={
                      "loss": self.adaptive.loss_weight,
                      "jitter": self.adaptive.jitter_weight,
                      "rtt": self.adaptive.rtt_weight
                  },
                  hysteresis_margin=self.hysteresis_decay.get_margin())

        # PHASE 10 — SESSION EXPIRY
        while not self.lifetime.expired():
            self.tick(1000)

        self.sm.transition(State.TERMINATED, "session_expired")
        self.emit("SESSION_EXPIRED", lifetime_ms=self.lifetime.elapsed)

        self.emitter.close()