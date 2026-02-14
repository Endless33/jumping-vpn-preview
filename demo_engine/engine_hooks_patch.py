from evolution_hooks import EvolutionHooks

class EngineHooksPatch:
    """
    Monkey-patch for DemoEngine to support evolution hooks.
    """

    def attach(self, engine):
        engine.hooks = EvolutionHooks()

        original_emit = engine.emit

        def patched_emit(event, **data):
            original_emit(event, **data)
            engine.hooks.apply(engine, event)

        engine.emit = patched_emit