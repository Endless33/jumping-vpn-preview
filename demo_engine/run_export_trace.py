from trace_exporter import TraceExporter

if __name__ == "__main__":
    exp = TraceExporter("demo_output.jsonl")
    path = exp.export()
    print(f"Trace exported: {path}")