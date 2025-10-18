# Linux Installation Guide - HubSpot Logging AI Agent

## Quick Fix for Current Issue

The error you're seeing is due to missing dependencies. Here's how to fix it:

### 1. **Quick Fix (Recommended)**
```bash
# Make the fix script executable
chmod +x fix_dependencies.sh

# Run the fix script
./fix_dependencies.sh
```

### 2. **Manual Fix**
```bash
# Activate your virtual environment
source venv/bin/activate

# Install missing cryptography module
pip install cryptography

# Install other potentially missing modules
pip install bcrypt python-dotenv marshmallow requests

# Test the installation
python -c "from cryptography.fernet import Fernet; print('✅ Cryptography installed!')"
```

### 3. **Complete Fresh Installation**
```bash
# Make the setup script executable
chmod +x setup_linux.sh

# Run the complete setup
./setup_linux.sh
```

## Detailed Installation Steps

### Prerequisites
- Python 3.8 or higher
- pip3
- Virtual environment support

### Step 1: Check Python Installation
```bash
python3 --version
pip3 --version
```

### Step 2: Create and Activate Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
# Test all imports
python -c "
import flask
import flask_sqlalchemy
import flask_migrate
import flask_jwt_extended
import flask_cors
import sqlalchemy
import cryptography
import bcrypt
import requests
import marshmallow
import dotenv
print('✅ All dependencies installed successfully!')
"
```

### Step 5: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit the .env file with your settings
nano .env
```

### Step 6: Run the Application
```bash
# Start the Flask app
python app/main.py
```

## Common Issues and Solutions

### Issue 1: "ModuleNotFoundError: No module named 'cryptography'"
**Solution:**
```bash
pip install cryptography
```

### Issue 2: "ModuleNotFoundError: No module named 'bcrypt'"
**Solution:**
```bash
pip install bcrypt
```

### Issue 3: "ModuleNotFoundError: No module named 'dotenv'"
**Solution:**
```bash
pip install python-dotenv
```

### Issue 4: "already has a primary mapper defined"
**Solution:** This is fixed in the current version. If you still see this error:
```bash
# Make sure you're using the updated main.py
git pull origin main
```

### Issue 5: Permission Denied
**Solution:**
```bash
# Make scripts executable
chmod +x setup_linux.sh
chmod +x fix_dependencies.sh
```

## Production Deployment

### Using Gunicorn
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app.main:app
```

### Using Systemd Service
Create `/etc/systemd/system/hubspot-agent.service`:
```ini
[Unit]
Description=HubSpot Logging AI Agent
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/hubspot_agent
Environment=PATH=/root/hubspot_agent/venv/bin
ExecStart=/root/hubspot_agent/venv/bin/python app/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable hubspot-agent
sudo systemctl start hubspot-agent
sudo systemctl status hubspot-agent
```

## Environment Variables

Create a `.env` file with the following variables:
```env
# Flask Configuration
FLASK_APP=app.main:app
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///data/database.db

# HubSpot Configuration
HUBSPOT_API_URL=https://api.hubapi.com
HUBSPOT_ACCESS_TOKEN=your-hubspot-token

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600

# WhatsApp Configuration
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your-webhook-token
```

## Testing the Installation

### 1. **Health Check**
```bash
curl http://localhost:5000/api/health
```

### 2. **WhatsApp Status**
```bash
curl http://localhost:5000/api/whatsapp/status
```

### 3. **Run Test Suite**
```bash
python test_linux_fix.py
```

## Troubleshooting

### Check Virtual Environment
```bash
# Verify you're in the virtual environment
which python
# Should show: /root/hubspot_agent/venv/bin/python
```

### Check Dependencies
```bash
# List installed packages
pip list

# Check specific package
pip show cryptography
```

### Check Logs
```bash
# If using systemd
sudo journalctl -u hubspot-agent -f

# If running directly
python app/main.py
```

## Performance Optimization

### For Production
```bash
# Install production dependencies
pip install gunicorn gevent

# Run with multiple workers
gunicorn -w 4 -k gevent -b 0.0.0.0:5000 app.main:app
```

### Database Optimization
```bash
# For SQLite optimization
echo "PRAGMA journal_mode=WAL;" | sqlite3 data/database.db
echo "PRAGMA synchronous=NORMAL;" | sqlite3 data/database.db
```

## Security Considerations

1. **Change default passwords**
2. **Use strong JWT secrets**
3. **Enable HTTPS in production**
4. **Restrict database access**
5. **Use environment variables for secrets**

## Support

If you encounter issues:
1. Check the logs first
2. Verify all dependencies are installed
3. Check environment variables
4. Test with the health endpoint
5. Review the troubleshooting section

The application should now work correctly on your Linux server! 🚀
