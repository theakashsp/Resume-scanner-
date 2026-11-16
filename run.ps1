Set-Location $PSScriptRoot

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Starting Resume Analyzer (Backend + Frontend)" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

Write-Host "[1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ..." -ForegroundColor Yellow
Start-Process cmd.exe -ArgumentList '/k', "cd /d `"$PSScriptRoot\backend`" && .\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000"

Write-Host "[2/2] Starting React Frontend on http://localhost:3000 ..." -ForegroundColor Yellow
Start-Process cmd.exe -ArgumentList '/k', "cd /d `"$PSScriptRoot\frontend`" && npx serve -s build -l 3000"

Start-Sleep -Seconds 2
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "===================================================" -ForegroundColor Green
Write-Host "Resume Analyzer is now running!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host "Backend:  http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "API Docs: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
