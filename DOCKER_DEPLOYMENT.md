# Docker Deployment Guide

## Overview
This guide shows how to deploy the HubSpot AI Agent in Docker with database and cache ignored (in-memory mode).

## Quick Start

### 1. Build and Run with Docker Compose
```bash
# Copy environment file
cp env.docker.example .env

# Edit .env with your actual values
nano .env

# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### 2. Build and Run with Docker
```bash
# Build the image
docker build -t hubspot-ai-agent .

# Run the container
docker run -d \
  --name hubspot-ai-agent \
  -p 5000:5000 \
  -e HUBSPOT_ACCESS_TOKEN=your-token \
  -e TWILIO_ACCOUNT_SID=your-sid \
  -e TWILIO_AUTH_TOKEN=your-token \
  hubspot-ai-agent
```

## Configuration

### Environment Variables
```bash
# Required
HUBSPOT_ACCESS_TOKEN=your-hubspot-pat-token
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token

# Optional
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
TWILIO_WHATSAPP_NUMBER=+14155238886
```

### Docker-Specific Settings
- **Database**: Uses in-memory SQLite (no persistence)
- **Cache**: Disabled (no caching)
- **Migrations**: Disabled
- **Logs**: Stored in `/app/logs` (mounted volume)

## Production Deployment

### 1. Using Docker Compose (Recommended)
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  hubspot-agent:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - HUBSPOT_ACCESS_TOKEN=${HUBSPOT_ACCESS_TOKEN}
      - TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID}
      - TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 2. Using Kubernetes
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hubspot-ai-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hubspot-ai-agent
  template:
    metadata:
      labels:
        app: hubspot-ai-agent
    spec:
      containers:
      - name: hubspot-ai-agent
        image: hubspot-ai-agent:latest
        ports:
        - containerPort: 5000
        env:
        - name: HUBSPOT_ACCESS_TOKEN
          valueFrom:
            secretKeyRef:
              name: hubspot-secrets
              key: access-token
        - name: TWILIO_ACCOUNT_SID
          valueFrom:
            secretKeyRef:
              name: twilio-secrets
              key: account-sid
        - name: TWILIO_AUTH_TOKEN
          valueFrom:
            secretKeyRef:
              name: twilio-secrets
              key: auth-token
```

## Features in Docker Mode

### ✅ What's Enabled:
- **API Endpoints**: All HubSpot and WhatsApp APIs
- **Authentication**: JWT-based authentication
- **Logging**: In-memory logging (not persisted)
- **Health Checks**: Built-in health monitoring
- **CORS**: Cross-origin requests enabled
- **Error Handling**: Comprehensive error responses

### ❌ What's Disabled:
- **Database Persistence**: No data saved between restarts
- **Cache**: No caching mechanisms
- **Migrations**: Database migrations disabled
- **File Storage**: No persistent file storage

## Monitoring and Logs

### Health Check
```bash
curl http://localhost:5000/api/health
```

### View Logs
```bash
# Docker Compose
docker-compose logs -f hubspot-agent

# Docker
docker logs -f hubspot-ai-agent
```

### Container Status
```bash
# Check running containers
docker ps

# Check container health
docker inspect hubspot-ai-agent | grep Health
```

## Scaling

### Horizontal Scaling
```bash
# Scale with Docker Compose
docker-compose up --scale hubspot-agent=3

# Scale with Docker Swarm
docker service create --name hubspot-ai-agent --replicas 3 hubspot-ai-agent
```

### Load Balancing
Use nginx or traefik for load balancing multiple instances:
```nginx
upstream hubspot_agents {
    server hubspot-agent-1:5000;
    server hubspot-agent-2:5000;
    server hubspot-agent-3:5000;
}

server {
    listen 80;
    location / {
        proxy_pass http://hubspot_agents;
    }
}
```

## Security

### Environment Variables
Never commit sensitive data to the repository:
```bash
# Use Docker secrets
docker secret create hubspot_token your-token

# Use Kubernetes secrets
kubectl create secret generic hubspot-secrets \
  --from-literal=access-token=your-token
```

### Network Security
```yaml
# docker-compose.yml
services:
  hubspot-agent:
    networks:
      - internal
    expose:
      - "5000"
  
  nginx:
    networks:
      - internal
      - external
    ports:
      - "80:80"
      - "443:443"

networks:
  internal:
    driver: bridge
  external:
    driver: bridge
```

## Troubleshooting

### Common Issues

1. **Container won't start**
   ```bash
   docker logs hubspot-ai-agent
   ```

2. **Health check failing**
   ```bash
   curl -v http://localhost:5000/api/health
   ```

3. **Environment variables not loaded**
   ```bash
   docker exec hubspot-ai-agent env | grep HUBSPOT
   ```

### Debug Mode
```bash
# Run in debug mode
docker run -it --rm \
  -p 5000:5000 \
  -e FLASK_ENV=development \
  hubspot-ai-agent python main.py
```

## Performance Optimization

### Resource Limits
```yaml
# docker-compose.yml
services:
  hubspot-agent:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### Gunicorn Configuration
```bash
# Custom Gunicorn settings
gunicorn --bind 0.0.0.0:5000 \
  --workers 4 \
  --worker-class gevent \
  --worker-connections 1000 \
  --timeout 120 \
  --keep-alive 2 \
  --max-requests 1000 \
  --max-requests-jitter 100 \
  app.main:app
```

## Backup and Recovery

Since Docker mode uses in-memory database, there's no data persistence. For production use:

1. **Use external database** (PostgreSQL, MySQL)
2. **Implement data export** endpoints
3. **Use message queues** for reliability
4. **Implement health monitoring**

## Next Steps

1. **Set up monitoring** (Prometheus, Grafana)
2. **Configure logging** (ELK stack)
3. **Implement CI/CD** (GitHub Actions, GitLab CI)
4. **Add security scanning** (Trivy, Snyk)
5. **Set up alerting** (PagerDuty, Slack)

Your HubSpot AI Agent is now ready for Docker deployment! 🐳
