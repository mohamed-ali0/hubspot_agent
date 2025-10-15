"""
Authentication service
"""

import jwt
from datetime import datetime, timedelta
from flask import current_app
from werkzeug.exceptions import BadRequest
from app.models import User
from app.db.database import db

class AuthService:
    """Authentication service for JWT token management"""

    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user with username and password"""
        user = User.query.filter_by(username=username, is_active=True).first()

        if not user or not user.verify_password(password):
            return None

        return user

    @staticmethod
    def generate_token(user):
        """Generate JWT token for user"""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
        }

        token = jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )

        return token

    @staticmethod
    def verify_token(token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise BadRequest('Token has expired')
        except jwt.InvalidTokenError:
            raise BadRequest('Invalid token')

    @staticmethod
    def get_user_from_token(token):
        """Get user from JWT token"""
        payload = AuthService.verify_token(token)
        user = User.query.get(payload['user_id'])

        if not user or not user.is_active:
            raise BadRequest('User not found or inactive')

        return user

    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        import bcrypt
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password, hashed_password):
        """Verify password against hash"""
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
