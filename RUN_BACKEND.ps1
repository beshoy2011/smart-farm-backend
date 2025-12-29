# تشغيل Backend - Run Backend
Write-Host "🚀 Starting Backend..." -ForegroundColor Green

# الانتقال لمجلد Backend
Set-Location -Path "backend"

# تفعيل البيئة الافتراضية
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    .\venv\Scripts\Activate.ps1
}

# تثبيت المتطلبات
Write-Host "📦 Installing/updating dependencies..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# تحديث قاعدة البيانات
Write-Host "📊 Updating database..." -ForegroundColor Cyan
python migrate_add_achievements.py

# تشغيل السيرفر
Write-Host ""
Write-Host "🚀 Starting server on http://localhost:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000


