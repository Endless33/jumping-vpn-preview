# RUN_DEMO.ps1
# One-click demo runner for Windows PowerShell
# Usage:
#   Right click -> Run with PowerShell
#   or: powershell -ExecutionPolicy Bypass -File .\RUN_DEMO.ps1

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "[Jumping VPN] Demo runner" -ForegroundColor Cyan
Write-Host "Repo root:" (Get-Location)
Write-Host ""

# Ensure we run from the repo root (where README.md exists)
if (-not (Test-Path ".\README.md")) {
  Write-Host "ERROR: Run this script from the repository root (README.md not found)." -ForegroundColor Red
  exit 1
}

# Pick python executable
$py = $null
if (Get-Command python -ErrorAction SilentlyContinue) { $py = "python" }
elseif (Get-Command py -ErrorAction SilentlyContinue) { $py = "py" }
else {
  Write-Host "ERROR: Python not found. Install Python 3.10+ and reopen PowerShell." -ForegroundColor Red
  exit 1
}

Write-Host "[1/4] Python:" -NoNewline
& $py --version
Write-Host ""

# Create venv if missing
if (-not (Test-Path ".\.venv")) {
  Write-Host "[2/4] Creating virtual environment (.venv)..." -ForegroundColor Yellow
  & $py -m venv .venv
} else {
  Write-Host "[2/4] Virtual environment exists (.venv)." -ForegroundColor Green
}

# Activate venv
Write-Host "[3/4] Activating venv..." -ForegroundColor Yellow
. .\.venv\Scripts\Activate.ps1

# Install deps if requirements.txt exists (optional)
if (Test-Path ".\requirements.txt") {
  Write-Host "[3/4] Installing requirements..." -ForegroundColor Yellow
  python -m pip install --upgrade pip | Out-Null
  python -m pip install -r requirements.txt
} else {
  Write-Host "[3/4] requirements.txt not found — skipping dependency install." -ForegroundColor DarkYellow
}

Write-Host ""
Write-Host "[4/4] Running demo..." -ForegroundColor Yellow
python run_demo.py

Write-Host ""
Write-Host "[validate] Running replay validator..." -ForegroundColor Yellow

# Prefer DEMO_OUTPUT.jsonl; fall back to DEMO_TRACE.jsonl if user uses that name
if (Test-Path ".\DEMO_OUTPUT.jsonl") {
  python demo_engine\replay.py DEMO_OUTPUT.jsonl
} elseif (Test-Path ".\DEMO_TRACE.jsonl") {
  python demo_engine\replay.py DEMO_TRACE.jsonl
} else {
  Write-Host "WARNING: No DEMO_OUTPUT.jsonl / DEMO_TRACE.jsonl found in repo root." -ForegroundColor DarkYellow
  Write-Host "If your demo writes output elsewhere, update this script accordingly."
}

Write-Host ""
Write-Host "[done] If you see 'Trace validated successfully', the demo passed." -ForegroundColor Green
Write-Host ""