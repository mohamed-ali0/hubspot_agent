#!/usr/bin/env python3
"""
Database initialization script
"""

import os
import sys
from pathlib import Path

# Add parent directory to Python path so we can import app modules
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from app.main import create_app
from app.db.database import db
from app.models import User, ChatSession, ChatMessage, Log

def init_db():
    """Initialize database with tables"""
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if we need to create a test user
        if not User.query.filter_by(username='testuser').first():
            print("Creating test user...")

            # Create test user
            test_user = User(
                name='Test User',
                username='testuser',
                password='testpass123',
                phone_number='+1234567890',
                hubspot_pat_token='test-token-encrypted',  # In real app, this would be encrypted
                email='test@example.com'
            )

            db.session.add(test_user)
            db.session.commit()

            print("Test user created: username='testuser', password='testpass123'")

        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
