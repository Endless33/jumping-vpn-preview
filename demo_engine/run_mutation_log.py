from mutation_log import MutationLog

if __name__ == "__main__":
    ml = MutationLog("demo_output.jsonl")
    ml.load()
    path = ml.generate()
    print(f"Mutation log generated: {path}")