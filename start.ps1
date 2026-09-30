# IntelTransform AI - SIH26154 Startup Script
# Run this from the root "GenAI Platform" directory in PowerShell

Write-Host ""
Write-Host "  ==========================================" -ForegroundColor Cyan
Write-Host "   IntelTransform AI  |  SIH26154" -ForegroundColor White
Write-Host "   Trusted Multi-Format Content Transform" -ForegroundColor Gray
Write-Host "  ==========================================" -ForegroundColor Cyan
Write-Host ""

# Start Backend (FastAPI)
Write-Host "[1/2] Starting Backend (FastAPI + uvicorn on :8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; .\venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload" -WindowStyle Normal

Start-Sleep -Seconds 3

# Start Frontend (Vite React)
Write-Host "[2/2] Starting Frontend (Vite React on :5173)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev" -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "  App is starting up!" -ForegroundColor Green
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Press Ctrl+C in each terminal to stop." -ForegroundColor Gray
