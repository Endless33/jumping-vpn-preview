from long_session import LongSessionSimulator

if __name__ == "__main__":
    sim = LongSessionSimulator(cycles=3)
    path = sim.run()
    print(f"Long session simulation saved to {path}")