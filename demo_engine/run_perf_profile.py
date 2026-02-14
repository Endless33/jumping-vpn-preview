from perf_profiler import PerfProfiler

if __name__ == "__main__":
    pp = PerfProfiler("demo_output.jsonl")
    path = pp.generate()
    print(f"Performance profile generated: {path}")