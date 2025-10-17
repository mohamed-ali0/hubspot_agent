@echo off
REM Simple Docker run script for HubSpot Agent (Windows)

echo Starting HubSpot Agent in Docker...

REM Build the image
echo Building Docker image...
docker build -t hubspot-agent .

REM Run the container
echo Starting container on port 5012...
docker run -d ^
  --name hubspot-agent ^
  -p 5012:5012 ^
  -e SECRET_KEY=your-secret-key-change-in-production ^
  -e DATABASE_URL=sqlite:///data/database.db ^
  -e JWT_SECRET_KEY=your-jwt-secret-key-change-in-production ^
  -e HUBSPOT_ACCESS_TOKEN=your-hubspot-token-here ^
  -e TWILIO_ACCOUNT_SID=your-twilio-account-sid ^
  -e TWILIO_AUTH_TOKEN=your-twilio-auth-token ^
  -e TWILIO_WHATSAPP_NUMBER=+14155238886 ^
  -v %cd%/data:/app/data ^
  --restart unless-stopped ^
  hubspot-agent

echo HubSpot Agent is running on http://localhost:5012
echo Health check: http://localhost:5012/api/health
echo.
echo To view logs: docker logs hubspot-agent
echo To stop: docker stop hubspot-agent
echo To remove: docker rm hubspot-agent
