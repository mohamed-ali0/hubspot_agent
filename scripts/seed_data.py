#!/usr/bin/env python3
"""
Seed database with test data
"""

import os
import sys
from datetime import datetime, timedelta
from app.main import create_app
from app.db.database import db
from app.models import User, ChatSession, ChatMessage, Log

def seed_data():
    """Seed database with test data"""
    app = create_app()

    with app.app_context():
        # Create test users
        users_data = [
            {
                'name': 'John Doe',
                'username': 'johndoe',
                'password': 'password123',
                'phone_number': '+1234567890',
                'hubspot_pat_token': 'encrypted-token-1',
                'email': 'john@example.com'
            },
            {
                'name': 'Jane Smith',
                'username': 'janesmith',
                'password': 'password456',
                'phone_number': '+0987654321',
                'hubspot_pat_token': 'encrypted-token-2',
                'email': 'jane@example.com'
            }
        ]

        users = []
        for user_data in users_data:
            user = User(**user_data)
            db.session.add(user)
            users.append(user)

        db.session.commit()

        # Create test sessions
        sessions_data = [
            {'user_id': users[0].id, 'status': 'active'},
            {'user_id': users[0].id, 'status': 'closed', 'ended_at': datetime.utcnow()},
            {'user_id': users[1].id, 'status': 'active'}
        ]

        sessions = []
        for session_data in sessions_data:
            session = ChatSession(**session_data)
            db.session.add(session)
            sessions.append(session)

        db.session.commit()

        # Create test messages
        messages_data = [
            {
                'session_id': sessions[0].id,
                'message_text': 'Had a great call with Ahmed from XYZ Corp. He is interested in our premium package.',
                'timestamp': datetime.utcnow() - timedelta(hours=2)
            },
            {
                'session_id': sessions[0].id,
                'message_text': 'Discussed pricing - he mentioned budget around $50,000 for the project.',
                'timestamp': datetime.utcnow() - timedelta(hours=1)
            },
            {
                'session_id': sessions[0].id,
                'message_text': 'Need to follow up next week with proposal and demo.',
                'timestamp': datetime.utcnow() - timedelta(minutes=30)
            },
            {
                'session_id': sessions[1].id,
                'message_text': 'Met with Sarah from TechStart Inc. She wants to explore partnership opportunities.',
                'timestamp': datetime.utcnow() - timedelta(hours=3)
            }
        ]

        messages = []
        for message_data in messages_data:
            message = ChatMessage(**message_data)
            db.session.add(message)
            messages.append(message)

        db.session.commit()

        # Create test logs
        logs_data = [
            {
                'user_id': users[0].id,
                'session_id': sessions[0].id,
                'chat_message_id': messages[0].id,
                'log_type': 'note',
                'sync_status': 'synced',
                'hubspot_id': 'note_12345',
                'synced_at': datetime.utcnow()
            },
            {
                'user_id': users[0].id,
                'session_id': sessions[0].id,
                'chat_message_id': messages[1].id,
                'log_type': 'deal',
                'sync_status': 'synced',
                'hubspot_id': 'deal_67890',
                'synced_at': datetime.utcnow()
            },
            {
                'user_id': users[0].id,
                'session_id': sessions[0].id,
                'chat_message_id': messages[2].id,
                'log_type': 'task',
                'sync_status': 'pending'
            },
            {
                'user_id': users[1].id,
                'session_id': sessions[1].id,
                'chat_message_id': messages[3].id,
                'log_type': 'contact_action',
                'sync_status': 'failed',
                'sync_error': 'HubSpot API rate limit exceeded'
            }
        ]

        for log_data in logs_data:
            log = Log(**log_data)
            db.session.add(log)

        db.session.commit()

        print("Test data seeded successfully!")
        print(f"Created {len(users)} users, {len(sessions)} sessions, {len(messages)} messages, {len(logs_data)} logs")

if __name__ == '__main__':
    seed_data()
