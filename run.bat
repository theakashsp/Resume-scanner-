@echo off
setlocal
cd /d "%~dp0"

echo ===================================================
echo Starting Resume Analyzer (Backend + Frontend)
echo ===================================================

echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "Resume Analyzer - Backend" cmd /k "cd /d %~dp0backend && .\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000"

echo [2/2] Starting React Frontend on http://localhost:3000 ...
start "Resume Analyzer - Frontend" cmd /k "cd /d %~dp0frontend && npx serve -s build -l 3000"

ping 127.0.0.1 -n 3 >nul
start http://localhost:3000

echo.
echo ===================================================
echo Resume Analyzer is now running!
echo Frontend: http://localhost:3000
echo Backend:  http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo ===================================================
echo Keep the two opened command prompt windows open.
echo.
