#!/bin/bash

echo "🐳 HubSpot AI Agent - Docker Quick Start"
echo "========================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose."
    exit 1
fi

echo "✅ Docker is running"

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp env.docker.example .env
    echo "⚠️  Please edit .env file with your actual credentials:"
    echo "   - HUBSPOT_ACCESS_TOKEN"
    echo "   - TWILIO_ACCOUNT_SID"
    echo "   - TWILIO_AUTH_TOKEN"
    echo ""
    read -p "Press Enter after updating .env file..."
fi

echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting HubSpot AI Agent..."
docker-compose up -d

echo "⏳ Waiting for application to start..."
sleep 10

echo "🔍 Testing deployment..."
python test_docker_deployment.py

echo ""
echo "🎉 HubSpot AI Agent is now running in Docker!"
echo ""
echo "📊 Application URLs:"
echo "   - API: http://localhost:5000"
echo "   - Health: http://localhost:5000/api/health"
echo "   - Help: http://localhost:5000/api/help"
echo ""
echo "📋 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop: docker-compose down"
echo "   - Restart: docker-compose restart"
echo "   - Rebuild: docker-compose up --build"
echo ""
echo "🐳 Docker mode features:"
echo "   ✅ In-memory database (no persistence)"
echo "   ✅ Cache disabled"
echo "   ✅ All APIs working"
echo "   ✅ Health monitoring"
echo "   ✅ Logging enabled"
