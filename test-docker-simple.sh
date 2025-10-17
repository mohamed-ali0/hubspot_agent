#!/bin/bash

echo "🔧 Testing Simple Docker Setup (No Redis/PostgreSQL)"
echo "=================================================="

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Use simple docker-compose (no Redis/PostgreSQL)
echo "📋 Using simple docker-compose.yml..."
cp docker-compose-simple.yml docker-compose.yml

# Validate the docker-compose.yml
echo "🔍 Validating docker-compose.yml..."
docker-compose config > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ docker-compose.yml is valid"
else
    echo "❌ docker-compose.yml has errors"
    docker-compose config
    exit 1
fi

# Build and start
echo "🔨 Building and starting application..."
docker-compose up --build -d

echo "⏳ Waiting for application to start..."
sleep 15

# Test the application
echo "🔍 Testing application..."
curl -f http://localhost:5012/api/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Application is running successfully!"
    echo ""
    echo "🎉 HubSpot AI Agent is now running!"
    echo ""
    echo "📊 Application URLs:"
    echo "   - API: http://localhost:5012"
    echo "   - Health: http://localhost:5012/api/health"
    echo "   - Help: http://localhost:5012/api/help"
    echo ""
    echo "📋 What's included:"
    echo "   ✅ Flask application (port 5012)"
    echo "   ✅ In-memory SQLite database"
    echo "   ✅ All HubSpot APIs"
    echo "   ✅ WhatsApp integration"
    echo "   ❌ Redis (not needed for basic operation)"
    echo "   ❌ PostgreSQL (using SQLite instead)"
    echo ""
    echo "📋 Useful commands:"
    echo "   - View logs: docker-compose logs -f"
    echo "   - Stop: docker-compose down"
    echo "   - Restart: docker-compose restart"
else
    echo "❌ Application failed to start. Check logs:"
    echo "   docker-compose logs"
    echo ""
    echo "🔍 Common issues:"
    echo "   - SQLAlchemy model conflicts"
    echo "   - Missing environment variables"
    echo "   - Port conflicts"
fi
