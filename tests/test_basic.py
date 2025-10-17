"""
Basic tests for the HubSpot Logging API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import json
import requests
from app.main import create_app

BASE_URL = "http://89.117.63.196:5012"

@pytest.fixture
def client():
    """Create HTTP client for testing endpoints"""
    return requests.Session()

@pytest.fixture
def test_user(app):
    """Create test user"""
    with app.app_context():
        user = User(
            name='Test User',
            username='testuser',
            password='testpass123',
            phone_number='+1234567890',
            hubspot_pat_token='encrypted-token',
            email='test@example.com'
        )
        db.session.add(user)
        db.session.commit()
        return user

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'status' in data
    assert 'database' in data
    assert 'timestamp' in data

def test_create_session(app, test_user):
    """Test session creation"""
    with app.app_context():
        # Create a test session in the database first
        from app.models import ChatSession
        session = ChatSession(user_id=test_user.id)
        db.session.add(session)
        db.session.commit()
        session_id = session.id

        session_data = {'user_id': test_user.id}

        response = app.test_client().post(
            '/api/sessions',
            data=json.dumps(session_data),
            content_type='application/json'
        )

        assert response.status_code == 201

        data = json.loads(response.data)
        assert 'id' in data
        assert 'user_id' in data
        assert 'status' in data

def test_create_message(app, test_user):
    """Test message creation"""
    with app.app_context():
        # First create a session
        from app.models import ChatSession, ChatMessage
        session = ChatSession(user_id=test_user.id)
        db.session.add(session)
        db.session.commit()
        session_id = session.id

        message_data = {
            'message_text': 'Test message for API testing',
            'forwarded_from': '+1234567890'
        }

        response = app.test_client().post(
            f'/api/sessions/{session_id}/messages',
            data=json.dumps(message_data),
            content_type='application/json'
        )

        assert response.status_code == 201

        data = json.loads(response.data)
        assert 'id' in data
        assert 'message_text' in data
        assert data['message_text'] == message_data['message_text']

def test_get_sessions(app, test_user):
    """Test getting user sessions"""
    with app.app_context():
        # Create a test session first
        from app.models import ChatSession
        session = ChatSession(user_id=test_user.id)
        db.session.add(session)
        db.session.commit()

        response = app.test_client().get('/api/sessions')

        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'sessions' in data
        assert 'total' in data
        assert len(data['sessions']) >= 1

if __name__ == '__main__':
    pytest.main([__file__])
