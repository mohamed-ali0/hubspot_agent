"""
Security utilities for token encryption and validation
"""

import secrets
import string
from cryptography.fernet import Fernet
from flask import current_app

class SecurityService:
    """Security service for encryption and validation"""

    @staticmethod
    def generate_secret_key():
        """Generate a secure secret key"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def encrypt_token(token):
        """Encrypt sensitive tokens (like HubSpot PAT)"""
        if not current_app.config.get('SECRET_KEY'):
            raise ValueError('SECRET_KEY not configured')

        # Use Fernet for symmetric encryption
        key = current_app.config['SECRET_KEY'][:32].encode()  # Fernet needs 32 bytes
        f = Fernet(key)

        return f.encrypt(token.encode()).decode()

    @staticmethod
    def decrypt_token(encrypted_token):
        """Decrypt sensitive tokens"""
        if not current_app.config.get('SECRET_KEY'):
            raise ValueError('SECRET_KEY not configured')

        key = current_app.config['SECRET_KEY'][:32].encode()
        f = Fernet(key)

        return f.decrypt(encrypted_token.encode()).decode()

    @staticmethod
    def validate_phone_number(phone_number):
        """Validate phone number format"""
        import re

        # Basic validation - should start with + and contain only digits
        pattern = r'^\+\d{10,15}$'
        return bool(re.match(pattern, phone_number))

    @staticmethod
    def validate_email(email):
        """Validate email format"""
        import re

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def sanitize_input(text):
        """Basic input sanitization"""
        if not text:
            return text

        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&']
        sanitized = text

        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')

        return sanitized
