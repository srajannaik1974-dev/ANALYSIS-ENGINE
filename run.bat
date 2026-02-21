@echo off
title DataVex Lead Intelligence
cd /d "%~dp0"

echo Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies. Check Python and pip.
    pause
    exit /b 1
)

echo.
echo Project folder: %cd%
echo.
echo Starting FRONTEND + BACKEND at http://127.0.0.1:8001
echo Open this URL in your browser for the input page.
echo Press Ctrl+C to stop.
echo.

start "" "http://127.0.0.1:8001"

python start_server.py
pause
