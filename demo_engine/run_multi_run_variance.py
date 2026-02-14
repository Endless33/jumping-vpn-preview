from multi_run_variance import MultiRunVariance

if __name__ == "__main__":
    mv = MultiRunVariance()
    path = mv.compute()
    print(f"Multi-run variance saved to {path}")