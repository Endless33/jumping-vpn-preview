from report_generator import ReportGenerator

if __name__ == "__main__":
    gen = ReportGenerator("SCENARIO_SUMMARY.json")
    path = gen.generate()
    print(f"Report generated: {path}")