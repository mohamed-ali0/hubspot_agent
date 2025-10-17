#!/bin/bash

echo "Stopping and removing existing containers..."
docker-compose down

echo "Rebuilding Docker image..."
docker-compose build --no-cache

echo "Starting containers..."
docker-compose up -d

echo "Checking container status..."
docker-compose ps

echo "Viewing logs..."
docker-compose logs -f
