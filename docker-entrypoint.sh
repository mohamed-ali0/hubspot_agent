#!/bin/bash
set -e

echo "Starting HubSpot AI Agent in Docker mode..."

# Create logs directory if it doesn't exist
mkdir -p /app/logs

# Set Docker environment flag
export DOCKER_ENV=true

# Initialize in-memory database (no persistence)
echo "[INFO] Initializing in-memory database..."
python -c "
from app.main import create_app
from app.db.database import db

app = create_app()
with app.app_context():
    db.create_all()
    print('[OK] In-memory database initialized successfully!')
"

# Start the application
echo "[START] Starting HubSpot AI Agent..."
echo "[INFO] Server will be available at: http://0.0.0.0:5000"
echo "[INFO] Health check: http://0.0.0.0:5000/api/health"
echo "[INFO] Docker mode: Database and cache ignored (in-memory only)"

# Use Gunicorn for production
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 100 app.main:app
