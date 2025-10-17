#!/bin/bash

echo "🐧 HubSpot AI Agent - Linux Server Setup"
echo "========================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Installing Docker..."
    
    # Update package index
    sudo apt-get update
    
    # Install Docker
    sudo apt-get install -y docker.io docker-compose
    
    # Start Docker service
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    
    echo "✅ Docker installed successfully"
    echo "⚠️  Please log out and log back in for Docker permissions to take effect"
    echo "   Or run: newgrp docker"
else
    echo "✅ Docker is already installed"
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Installing..."
    sudo apt-get install -y docker-compose
    echo "✅ docker-compose installed"
else
    echo "✅ docker-compose is available"
fi

# Create logs directory
mkdir -p logs
echo "✅ Created logs directory"

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp env.production.example .env
    echo "⚠️  Please edit .env file with your actual credentials:"
    echo "   - HUBSPOT_ACCESS_TOKEN"
    echo "   - SECRET_KEY"
    echo "   - JWT_SECRET_KEY"
    echo ""
    echo "   nano .env"
    echo ""
    read -p "Press Enter after updating .env file..."
fi

# Validate docker-compose.yml
echo "🔍 Validating docker-compose.yml..."
docker-compose config > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ docker-compose.yml is valid"
else
    echo "❌ docker-compose.yml has errors"
    exit 1
fi

# Build and start the application
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting HubSpot AI Agent..."
docker-compose up -d

echo "⏳ Waiting for application to start..."
sleep 10

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
else
    echo "❌ Application failed to start. Check logs:"
    echo "   docker-compose logs"
fi
