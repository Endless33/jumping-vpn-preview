from validator import DemoValidator

if __name__ == "__main__":
    v = DemoValidator("demo_output.jsonl")
    errors = v.validate()

    if not errors:
        print("Demo validation PASSED.")
    else:
        print("Demo validation FAILED:")
        for e in errors:
            print(" -", e)