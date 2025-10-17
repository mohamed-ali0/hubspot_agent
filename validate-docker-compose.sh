#!/bin/bash

echo "🔍 Validating docker-compose.yml..."

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose first."
    exit 1
fi

# Validate the docker-compose.yml file
echo "📋 Checking docker-compose.yml syntax..."
docker-compose config > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ docker-compose.yml is valid!"
    echo ""
    echo "📊 Configuration summary:"
    docker-compose config --services
    echo ""
    echo "🚀 You can now run:"
    echo "   docker-compose up --build -d"
else
    echo "❌ docker-compose.yml has errors:"
    docker-compose config
    exit 1
fi
