# تشغيل Backend و Frontend معاً
# Start Backend and Frontend Together

Write-Host "🚀 Starting SmartFarm AI..." -ForegroundColor Cyan
Write-Host ""

# Start Backend in new window
Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\start-backend.ps1"

# Wait a bit
Start-Sleep -Seconds 3

# Start Frontend in new window
Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\start-frontend.ps1"

Write-Host "✅ Backend and Frontend are starting in separate windows" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access the application:" -ForegroundColor Yellow
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""

