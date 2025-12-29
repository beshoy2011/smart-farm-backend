# تشغيل Backend Server
# Start Backend Server

Write-Host "🚀 Starting Backend Server..." -ForegroundColor Green
Write-Host ""

cd backend

# تفعيل البيئة الافتراضية / Activate virtual environment
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    .\venv\Scripts\Activate.ps1
}

# تثبيت المتطلبات بدون psycopg2-binary (لأننا نستخدم SQLite) / Install requirements without psycopg2-binary (using SQLite)
Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
python -m pip install --upgrade pip
# Install from requirements.txt (includes new dependencies)
python -m pip install -r requirements.txt

# Update database
Write-Host "📊 Updating database..." -ForegroundColor Cyan
python migrate_add_achievements.py

Write-Host ""
Write-Host "🚀 Starting server..." -ForegroundColor Green
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

