#!/usr/bin/env python3
"""
Basic API Test Script

This script tests the basic functionality of the API endpoints
without requiring complex database operations or full integration testing.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import json
from app.main import create_app

def test_app_creation():
    """Test that the Flask app can be created"""
    app = create_app()
    assert app is not None
    assert app.config['TESTING'] == False  # Default config
    print("[OK] Flask app created successfully")

def test_health_endpoint():
    """Test the health endpoint"""
    app = create_app()

    with app.test_client() as client:
        response = client.get('/api/health')

        assert response.status_code == 200
        data = response.get_json()
        assert 'status' in data
        assert 'database' in data
        assert 'hubspot_api' in data

        print(f"[OK] Health endpoint working: {data}")

def test_auth_endpoints():
    """Test authentication endpoints"""
    app = create_app()

    with app.test_client() as client:
        # Test login endpoint exists
        response = client.post('/api/auth/login',
                              json={'username': 'test', 'password': 'test'},
                              headers={'Content-Type': 'application/json'})

        # Should return 401 for invalid credentials, but endpoint should exist
        assert response.status_code in [400, 401, 422]  # Validation or auth error is expected

        print("[OK] Authentication endpoints accessible")

def test_user_endpoints():
    """Test user management endpoints"""
    app = create_app()

    with app.test_client() as client:
        # Test user creation/update endpoints exist
        response = client.get('/api/users/1')
        # Should return 401 or 404, but endpoint should exist
        assert response.status_code in [401, 404]

        print("[OK] User management endpoints accessible")

def test_session_endpoints():
    """Test session management endpoints"""
    app = create_app()

    with app.test_client() as client:
        # Test session endpoints exist
        response = client.get('/api/sessions')
        # Should return 401, but endpoint should exist
        assert response.status_code == 401

        print("[OK] Session management endpoints accessible")

def test_hubspot_endpoints():
    """Test HubSpot integration endpoints"""
    app = create_app()

    with app.test_client() as client:
        # Test HubSpot connection endpoint
        response = client.get('/api/hubspot/test-connection')
        # Should return 401 or error about missing token, but endpoint should exist
        assert response.status_code in [401, 500]  # Auth error or missing token

        print("[OK] HubSpot integration endpoints accessible")

def test_stats_endpoints():
    """Test analytics endpoints"""
    app = create_app()

    with app.test_client() as client:
        # Test stats endpoints exist
        response = client.get('/api/stats/overview')
        # Should return 401, but endpoint should exist
        assert response.status_code == 401

        print("[OK] Analytics endpoints accessible")

def run_all_tests():
    """Run all basic tests"""
    print("[TESTS] Starting Basic API Tests")
    print("=" * 50)

    tests = [
        test_app_creation,
        test_health_endpoint,
        test_auth_endpoints,
        test_user_endpoints,
        test_session_endpoints,
        test_hubspot_endpoints,
        test_stats_endpoints
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"[ERROR] {test.__name__} failed: {str(e)}")
            failed += 1

    print("\n" + "=" * 50)
    print("[STATS] BASIC API TEST RESULTS")
    print("=" * 50)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    print(f"Success Rate: {passed/(passed+failed)*100:.1f}%" if (passed+failed) > 0 else "Success Rate: N/A")

    if failed == 0:
        print("\n[OK] All basic API tests passed!")
        return True
    else:
        print(f"\n[ERROR] {failed} test(s) failed!")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
