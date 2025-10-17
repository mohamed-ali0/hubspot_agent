#!/bin/bash

echo "🔍 Testing YAML Syntax for docker-compose files..."

# Test original docker-compose.yml
echo "📋 Testing docker-compose.yml..."
docker-compose -f docker-compose.yml config > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ docker-compose.yml is valid"
else
    echo "❌ docker-compose.yml has errors"
    docker-compose -f docker-compose.yml config
fi

echo ""

# Test clean version
echo "📋 Testing docker-compose-clean.yml..."
docker-compose -f docker-compose-clean.yml config > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ docker-compose-clean.yml is valid"
else
    echo "❌ docker-compose-clean.yml has errors"
    docker-compose -f docker-compose-clean.yml config
fi

echo ""

# Test no-PAT version
echo "📋 Testing docker-compose-no-pat.yml..."
docker-compose -f docker-compose-no-pat.yml config > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ docker-compose-no-pat.yml is valid"
else
    echo "❌ docker-compose-no-pat.yml has errors"
    docker-compose -f docker-compose-no-pat.yml config
fi

echo ""
echo "🎯 Recommendation: Use docker-compose-clean.yml for production"
