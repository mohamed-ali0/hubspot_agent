@echo off
REM Fix Docker SQLAlchemy Model Conflict

echo 🔧 Fixing Docker SQLAlchemy Model Conflict...

echo 1. Stopping containers...
docker-compose down

echo 2. Removing old images...
docker rmi hubspot-agent 2>nul

echo 3. Rebuilding with no cache...
docker-compose build --no-cache

echo 4. Starting containers...
docker-compose up -d

echo 5. Waiting for startup...
timeout /t 5 /nobreak >nul

echo 6. Checking logs...
docker-compose logs --tail=20

echo 7. Testing health endpoint...
curl -f http://localhost:5012/api/health && echo ✅ Health check passed! || echo ❌ Health check failed

echo.
echo 🎯 If you see 'Health check passed!', the fix worked!
echo 📊 View full logs: docker-compose logs -f
