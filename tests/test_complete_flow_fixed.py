#!/usr/bin/env python3
"""
Complete Flow Test Script - Fixed Version

This script tests the complete HubSpot Logging API by making HTTP requests to endpoints.
Tests the actual API functionality without direct database access.
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = "http://127.0.0.1:5000"

def get_auth_token():
    """Get authentication token"""
    login_data = {
        'username': 'flow_tester',
        'password': 'testpass123'
    }

    response = requests.post(
        f'{BASE_URL}/api/auth/login',
        json=login_data,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        return response.json()['token']
    return None

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f'{BASE_URL}/api/health')
    return response.status_code == 200

def test_authentication():
    """Test authentication"""
    # Try to authenticate first (user might already exist)
    token = get_auth_token()

    if token is not None:
        print("[OK] Authentication successful with existing user")
        return True

    # If that fails, try to create a test user
    print("[INFO] Trying to create test user...")
    user_data = {
        'name': 'Test User',
        'username': 'testuser',
        'password': 'testpass123',
        'phone_number': '+1234567890',
        'email': 'test@example.com',
        'hubspot_pat_token': 'test-token-123'
    }

    try:
        create_response = requests.post(
            f'{BASE_URL}/api/users',
            json=user_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"User creation status: {create_response.status_code}")

        if create_response.status_code == 201:
            print("[OK] Test user created successfully")
            # Try authentication again
            token = get_auth_token()
            return token is not None
        else:
            print(f"[ERROR] User creation failed: {create_response.text}")
            return False

    except Exception as e:
        print(f"[ERROR] User creation exception: {str(e)}")
        return False

def test_create_session():
    """Test session creation"""
    token = get_auth_token()
    if not token:
        return False

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    session_data = {'user_id': 1}  # Using test user ID

    response = requests.post(
        f'{BASE_URL}/api/sessions',
        json=session_data,
        headers=headers
    )

    return response.status_code == 201

def test_create_message():
    """Test message creation"""
    token = get_auth_token()
    if not token:
        return False

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    message_data = {
        'message_text': 'Test message for complete flow testing',
        'forwarded_from': '+1234567890'
    }

    response = requests.post(
        f'{BASE_URL}/api/sessions/1/messages',  # Using session ID 1
        json=message_data,
        headers=headers
    )

    return response.status_code == 201

def test_create_logs():
    """Test log creation"""
    token = get_auth_token()
    if not token:
        return False

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Create contact log
    contact_log_data = {
        'session_id': 1,
        'chat_message_id': 1,
        'log_type': 'contact_action',
        'hubspot_payload': {
            'properties': {
                'firstname': 'Test',
                'lastname': 'User',
                'email': 'test@example.com',
                'phone': '+1234567890'
            }
        }
    }

    response = requests.post(
        f'{BASE_URL}/api/logs',
        json=contact_log_data,
        headers=headers
    )

    return response.status_code == 201

def test_hubspot_integration():
    """Test HubSpot record creation"""
    token = get_auth_token()
    if not token:
        return False

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Create contact via API
    contact_data = {
        'session_id': 1,
        'chat_message_id': 1,
        'properties': {
            'firstname': 'API',
            'lastname': 'Test',
            'email': f'test-{int(time.time())}@example.com',
            'phone': '+1234567890'
        }
    }

    response = requests.post(
        f'{BASE_URL}/api/hubspot/contacts',
        json=contact_data,
        headers=headers
    )

    return response.status_code == 201

def test_get_logs():
    """Test getting logs"""
    token = get_auth_token()
    if not token:
        return False

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(
        f'{BASE_URL}/api/logs',
        headers=headers
    )

    return response.status_code == 200

def test_analytics():
    """Test analytics"""
    token = get_auth_token()
    if not token:
        return False

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(
        f'{BASE_URL}/api/stats/overview',
        headers=headers
    )

    return response.status_code == 200

def run_complete_flow():
    """Run the complete flow test"""
    print("Starting Complete Flow Test")
    print("=" * 60)

    tests = [
        ("Health Check", test_health_check),
        ("Authentication", test_authentication),
        ("Session Creation", test_create_session),
        ("Message Creation", test_create_message),
        ("Log Creation", test_create_logs),
        ("HubSpot Integration", test_hubspot_integration),
        ("Get Logs", test_get_logs),
        ("Analytics", test_analytics)
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"[OK] {test_name}")
            else:
                failed += 1
                print(f"[ERROR] {test_name}")
        except Exception as e:
            failed += 1
            print(f"[ERROR] {test_name}: {str(e)}")

    print("\n" + "=" * 60)
    print("COMPLETE FLOW RESULTS")
    print("=" * 60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    print(f"Success Rate: {passed/(passed+failed)*100:.1f}%" if (passed+failed) > 0 else "Success Rate: N/A")

    return failed == 0

if __name__ == "__main__":
    success = run_complete_flow()
    import sys
    sys.exit(0 if success else 1)
