from chaos_recovery import ChaosRecoveryAnalyzer

if __name__ == "__main__":
    analyzer = ChaosRecoveryAnalyzer("chaos_output.jsonl")
    path = analyzer.analyze()
    print(f"Chaos recovery analysis saved to {path}")