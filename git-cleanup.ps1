# Git Cleanup Script for HubSpot AI Agent
# This script helps organize the git repository

Write-Host "🧹 Git Cleanup Script" -ForegroundColor Green
Write-Host "====================" -ForegroundColor Green

# Check if git is available
try {
    git --version | Out-Null
    Write-Host "✅ Git is available" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not available. Please install Git first." -ForegroundColor Red
    exit 1
}

Write-Host "`n📋 Current git status:" -ForegroundColor Yellow
git status --short

Write-Host "`n🔄 Cleaning up cache files..." -ForegroundColor Yellow

# Unstage cache files
$cacheFiles = @(
    "app/__pycache__/",
    "app/api/__pycache__/", 
    "app/api/v1/__pycache__/",
    "app/api/v1/hubspot/__pycache__/",
    "app/core/__pycache__/",
    "app/db/__pycache__/",
    "app/models/__pycache__/",
    "app/services/__pycache__/"
)

foreach ($file in $cacheFiles) {
    if (git ls-files --cached $file 2>$null) {
        git reset HEAD $file
        Write-Host "  Unstaged: $file" -ForegroundColor Gray
    }
}

Write-Host "`n📁 Adding important new files..." -ForegroundColor Yellow

# Add important new files
$importantFiles = @(
    "Dockerfile",
    "docker-compose.yml", 
    "docker-entrypoint.sh",
    "docker-start.sh",
    ".dockerignore",
    ".gitignore",
    "requirements.txt",
    "env.docker.example",
    "DOCKER_DEPLOYMENT.md",
    "TWILIO_WHATSAPP_SETUP.md",
    "n8n_whatsapp_workflow.json",
    "test_whatsapp_controller.py",
    "test_docker_deployment.py",
    "test_complete_sales_flow.py"
)

foreach ($file in $importantFiles) {
    if (Test-Path $file) {
        git add $file
        Write-Host "  Added: $file" -ForegroundColor Green
    }
}

# Add app directory changes (excluding cache)
Write-Host "`n📦 Adding app directory changes..." -ForegroundColor Yellow
git add app/ --ignore-errors

Write-Host "`n📊 Updated git status:" -ForegroundColor Yellow
git status --short

Write-Host "`n💡 Recommended next steps:" -ForegroundColor Cyan
Write-Host "1. Review the staged changes: git diff --cached" -ForegroundColor White
Write-Host "2. Commit the changes: git commit -m 'Add Docker support and WhatsApp integration'" -ForegroundColor White
Write-Host "3. Push to repository: git push origin master" -ForegroundColor White

Write-Host "`n🎉 Git cleanup completed!" -ForegroundColor Green
