"""
User model for salesmen
"""

import bcrypt
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from app.db.database import db

class User(db.Model):
    """User model representing salesmen"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    hubspot_pat_token = Column(Text, nullable=False)  # Encrypted at application level
    email = Column(String(100), unique=True, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, name, username, password, phone_number, hubspot_pat_token, email=None):
        self.name = name
        self.username = username
        self.password = password  # This will trigger the password setter
        self.phone_number = phone_number
        self.hubspot_pat_token = hubspot_pat_token
        self.email = email

    @property
    def password(self):
        """Password property (read-only)"""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Hash password before storing"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'phone_number': self.phone_number,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<User {self.username}>'
