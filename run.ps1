# DataVex Lead Intelligence - Run script (PowerShell)
Set-Location $PSScriptRoot

Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install dependencies. Check Python and pip." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Project folder: $PSScriptRoot" -ForegroundColor Gray
Write-Host "Starting FRONTEND + BACKEND at http://127.0.0.1:8001" -ForegroundColor Green
Write-Host "Open this URL in your browser for the input page." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server." -ForegroundColor Yellow
Write-Host ""

Start-Process "http://127.0.0.1:8001"
python start_server.py
