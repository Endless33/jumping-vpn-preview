from dashboard_generator import DashboardGenerator

if __name__ == "__main__":
    gen = DashboardGenerator()
    path = gen.generate()
    print(f"Dashboard generated: {path}")