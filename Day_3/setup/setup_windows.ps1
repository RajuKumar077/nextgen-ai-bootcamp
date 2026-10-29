# ─────────────────────────────────────────────────────────────────────────────
#  Day 3 · RAG + Agents · one-time setup for Windows (PowerShell)
#  Run from the Day_3 folder:   powershell -ExecutionPolicy Bypass -File setup\setup_windows.ps1
# ─────────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "`n=== 1/5  Checking Ollama ===" -ForegroundColor Cyan
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "Ollama is not installed. Trying winget..." -ForegroundColor Yellow
    winget install --id Ollama.Ollama -e --accept-source-agreements --accept-package-agreements
    Write-Host "Close and reopen PowerShell, then run this script again." -ForegroundColor Yellow
    exit 1
}
ollama --version

Write-Host "`n=== 2/5  Reading model names from bootcamp_config.json ===" -ForegroundColor Cyan
$cfg = Get-Content (Join-Path $Root "bootcamp_config.json") -Raw | ConvertFrom-Json
Write-Host "Main model : $($cfg.model)"
Write-Host "Small model: $($cfg.small_model)"
Write-Host "Embed model: $($cfg.embed_model)"

Write-Host "`n=== 3/5  Downloading models (first time only, may take a few minutes) ===" -ForegroundColor Cyan
$models = @($cfg.model, $cfg.small_model, $cfg.embed_model) | Select-Object -Unique
foreach ($m in $models) { ollama pull $m }

Write-Host "`n=== 4/5  Creating Python virtual environment (.venv) ===" -ForegroundColor Cyan
$py = (Get-Command py -ErrorAction SilentlyContinue)
if ($py) { py -3 -m venv .venv } else { python -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install --upgrade pip -q
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt -q

Write-Host "`n=== 5/5  Connection test ===" -ForegroundColor Cyan
& .\.venv\Scripts\python.exe setup\check_setup.py

Write-Host "`nDone. Open the Day_3 folder in VS Code or Antigravity, open Class_5_RAG\notebooks\Class_5_*.ipynb," -ForegroundColor Green
Write-Host "and choose the kernel '.venv' (top right). Then press Shift+Enter on each cell." -ForegroundColor Green
