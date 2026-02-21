@echo off
title DataVex - Start frontend + backend
cd /d "%~dp0"

echo Installing dependencies...
pip install -q -r requirements.txt
echo.
echo Starting at http://127.0.0.1:8001 (frontend with input form)
echo.
start "" "http://127.0.0.1:8001"
python start_server.py
pause
