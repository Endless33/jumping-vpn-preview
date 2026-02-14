class EvolutionHooks:
    """
    Allows injecting experimental protocol behaviors.
    """

    def __init__(self):
        self.hooks = []

    def add(self, fn):
        """
        Adds a hook function: fn(engine, event)
        """
        self.hooks.append(fn)

    def apply(self, engine, event):
        for fn in self.hooks:
            fn(engine, event)