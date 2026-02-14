from spec_checker import DemoSpecChecker

if __name__ == "__main__":
    checker = DemoSpecChecker("demo_output.jsonl")
    errors = checker.validate()

    if not errors:
        print("DEMO_SPEC compliance PASSED.")
    else:
        print("DEMO_SPEC compliance FAILED:")
        for e in errors:
            print(" -", e)