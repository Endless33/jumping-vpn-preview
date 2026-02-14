from output_format_checker import OutputFormatChecker

if __name__ == "__main__":
    checker = OutputFormatChecker("demo_output.jsonl")
    errors = checker.validate()

    if not errors:
        print("Output format is valid.")
    else:
        print("Output format errors:")
        for e in errors:
            print(" -", e)