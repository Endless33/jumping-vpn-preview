from invariants_checker import InvariantsChecker

if __name__ == "__main__":
    chk = InvariantsChecker("demo_output.jsonl")
    errors = chk.validate()

    if not errors:
        print("Invariants check PASSED.")
    else:
        print("Invariants check FAILED:")
        for e in errors:
            print(" -", e)