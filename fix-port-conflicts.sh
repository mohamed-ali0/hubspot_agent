#!/bin/bash

echo "🔧 Fixing Port Conflicts"
echo "========================"

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Check for port conflicts
echo "🔍 Checking for port conflicts..."

# Check port 5000
if lsof -i :5000 >/dev/null 2>&1; then
    echo "⚠️  Port 5000 is in use. Using port 5012 instead."
    PORT_CONFLICT_5000=true
else
    echo "✅ Port 5000 is available"
    PORT_CONFLICT_5000=false
fi

# Check port 6379 (Redis)
if lsof -i :6379 >/dev/null 2>&1; then
    echo "⚠️  Port 6379 (Redis) is in use. Using port 6380 instead."
    REDIS_CONFLICT=true
else
    echo "✅ Port 6379 (Redis) is available"
    REDIS_CONFLICT=false
fi

# Update docker-compose.yml if needed
if [ "$PORT_CONFLICT_5000" = true ] || [ "$REDIS_CONFLICT" = true ]; then
    echo "📝 Updating docker-compose.yml with alternative ports..."
    
    # Use the clean version with correct ports
    cp docker-compose-clean.yml docker-compose.yml
    
    echo "✅ Updated docker-compose.yml with port 5012 and Redis 6380"
fi

echo ""
echo "🚀 Starting with updated configuration..."
docker-compose up --build -d

echo ""
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
else
    echo "❌ Application failed to start. Check logs:"
    echo "   docker-compose logs"
fi
