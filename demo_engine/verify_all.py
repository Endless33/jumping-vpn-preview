import os
import sys
import subprocess
from pathlib import Path


def run(cmd, cwd: Path) -> int:
    print(f"\n$ {' '.join(cmd)}\n")
    p = subprocess.run(cmd, cwd=str(cwd))
    return int(p.returncode)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    trace = repo_root / "DEMO_TRACE.jsonl"

    if not trace.exists():
        print("ERROR: DEMO_TRACE.jsonl not found in repo root.")
        print(f"Expected: {trace}")
        return 2

    checks = [
        # 1) continuity invariants
        [sys.executable, str(repo_root / "demo_engine" / "continuity_verifier.py"), str(trace)],
        # 2) optional replay verifier (if you create it later)
        # [sys.executable, str(repo_root / "demo_engine" / "replay.py"), str(trace)],
    ]

    print("Jumping VPN — Demo Verification Suite")
    print(f"Repo root: {repo_root}")
    print(f"Trace:     {trace}")

    failed = 0
    for cmd in checks:
        code = run(cmd, repo_root)
        if code != 0:
            failed += 1

    if failed:
        print(f"\nRESULT: FAIL ({failed} check(s) failed)")
        return 1

    print("\nRESULT: PASS (all checks passed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())