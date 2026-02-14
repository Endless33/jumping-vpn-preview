import os
from engine import DemoEngine
from validator import DemoValidator

class SelfTest:
    """
    Minimal self-test suite for DemoEngine.
    """

    def __init__(self, output="selftest_output.jsonl"):
        self.output = output

    def run(self):
        engine = DemoEngine("selftest", self.output)
        engine.run()

        validator = DemoValidator(self.output)
        errors = validator.validate()

        return errors

    def print_result(self, errors):
        if not errors:
            print("SELF-TEST PASSED")
        else:
            print("SELF-TEST FAILED:")
            for e in errors:
                print(" -", e)