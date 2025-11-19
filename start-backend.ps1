# تشغيل Backend Server
# Start Backend Server

Write-Host "🚀 Starting Backend Server..." -ForegroundColor Green
Write-Host ""

cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 0.0.0.0 --port 8000

