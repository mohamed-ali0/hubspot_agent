"""
Docker-specific configuration
Ignores database and cache for containerized deployment
"""

import os
from datetime import timedelta

class DockerConfig:
    """Configuration for Docker deployment"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'docker-secret-key-change-in-production')
    FLASK_ENV = 'production'
    
    # Database Configuration - Use in-memory SQLite for Docker
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'docker-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
    
    # HubSpot Configuration
    HUBSPOT_API_URL = os.getenv('HUBSPOT_API_URL', 'https://api.hubapi.com')
    HUBSPOT_ACCESS_TOKEN = os.getenv('HUBSPOT_ACCESS_TOKEN')
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
    TWILIO_WEBHOOK_URL = os.getenv('TWILIO_WEBHOOK_URL')
    
    # WhatsApp Configuration
    WHATSAPP_WEBHOOK_VERIFY_TOKEN = os.getenv('WHATSAPP_WEBHOOK_VERIFY_TOKEN')
    
    # Docker-specific settings
    IGNORE_DATABASE_PERSISTENCE = True
    IGNORE_CACHE = True
    USE_IN_MEMORY_DB = True
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = '/app/logs/app.log'
    
    # CORS Configuration
    CORS_ORIGINS = ['*']
    
    # Disable database migrations in Docker
    DISABLE_MIGRATIONS = True
