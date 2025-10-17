# Docker Setup for HubSpot Agent

## Quick Start

### Option 1: Using Docker Compose (Recommended)
```bash
# 1. Update environment variables in docker-compose.yml
# 2. Run the application
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Option 2: Using Docker Run Scripts

**Linux/Mac:**
```bash
chmod +x docker-run.sh
./docker-run.sh
```

**Windows:**
```cmd
docker-run.bat
```

### Option 3: Manual Docker Commands
```bash
# Build the image
docker build -t hubspot-agent .

# Run the container
docker run -d \
  --name hubspot-agent \
  -p 5012:5012 \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=sqlite:///data/database.db \
  -e JWT_SECRET_KEY=your-jwt-secret \
  -e HUBSPOT_ACCESS_TOKEN=your-hubspot-token \
  -e TWILIO_ACCOUNT_SID=your-twilio-sid \
  -e TWILIO_AUTH_TOKEN=your-twilio-token \
  -e TWILIO_WHATSAPP_NUMBER=+14155238886 \
  -v $(pwd)/data:/app/data \
  --restart unless-stopped \
  hubspot-agent
```

## Configuration

### Environment Variables
Update these in `docker-compose.yml` or pass them via `-e` flags:

```yaml
environment:
  - SECRET_KEY=your-secret-key-change-in-production
  - DATABASE_URL=sqlite:///data/database.db
  - JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
  - HUBSPOT_ACCESS_TOKEN=your-hubspot-token-here
  - TWILIO_ACCOUNT_SID=your-twilio-account-sid
  - TWILIO_AUTH_TOKEN=your-twilio-auth-token
  - TWILIO_WHATSAPP_NUMBER=+14155238886
```

### Port Configuration
- **Internal Port:** 5012 (inside container)
- **External Port:** 5012 (host machine)
- **Access URL:** http://localhost:5012

## Management Commands

### View Logs
```bash
# Docker Compose
docker-compose logs -f

# Docker Run
docker logs hubspot-agent
```

### Stop Application
```bash
# Docker Compose
docker-compose down

# Docker Run
docker stop hubspot-agent
```

### Restart Application
```bash
# Docker Compose
docker-compose restart

# Docker Run
docker restart hubspot-agent
```

### Remove Container
```bash
# Docker Compose
docker-compose down -v

# Docker Run
docker rm hubspot-agent
```

## Health Check

The application includes automatic health checks:
- **Health Endpoint:** http://localhost:5012/api/health
- **Check Interval:** 30 seconds
- **Timeout:** 10 seconds
- **Retries:** 3

## Data Persistence

- **Database:** SQLite file stored in `./data/database.db`
- **Volume Mount:** `./data:/app/data`
- **Backup:** Copy the `./data` folder to backup your database

## Production Considerations

1. **Change Default Secrets:**
   - Update `SECRET_KEY`
   - Update `JWT_SECRET_KEY`
   - Use strong, unique values

2. **Environment Variables:**
   - Set all required environment variables
   - Use a `.env` file for local development
   - Use Docker secrets for production

3. **Database:**
   - Consider using PostgreSQL for production
   - Implement database backups
   - Monitor database size

4. **Security:**
   - Use HTTPS in production
   - Implement proper firewall rules
   - Regular security updates

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker logs hubspot-agent

# Check if port is in use
netstat -tulpn | grep 5012
```

### Database Issues
```bash
# Check database file
ls -la data/

# Reset database (WARNING: This deletes all data)
rm data/database.db
docker restart hubspot-agent
```

### Permission Issues
```bash
# Fix data directory permissions
sudo chown -R $USER:$USER data/
chmod -R 755 data/
```

## API Endpoints

Once running, the application provides:

- **Health Check:** GET http://localhost:5012/api/health
- **Authentication:** POST http://localhost:5012/api/auth/login
- **HubSpot APIs:** http://localhost:5012/api/hubspot/*
- **WhatsApp Webhook:** http://localhost:5012/api/whatsapp/webhook

## Example Usage

```bash
# Test health endpoint
curl http://localhost:5012/api/health

# Test authentication
curl -X POST http://localhost:5012/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test"}'
```

Your HubSpot Agent is now running in Docker on port 5012! 🚀
