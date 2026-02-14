from orchestrator import Orchestrator

if __name__ == "__main__":
    orch = Orchestrator()
    summary_path = orch.run()
    print(f"Scenario orchestration complete. Summary saved to {summary_path}")