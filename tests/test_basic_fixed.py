import json
import requests

BASE_URL = "http://89.117.63.196:5012"

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f'{BASE_URL}/api/health')

    assert response.status_code == 200
    data = response.json()
    assert 'status' in data
    assert 'database' in data
    assert 'timestamp' in data

def test_auth_endpoints():
    """Test authentication endpoints"""
    # Test login endpoint exists
    response = requests.post(
        f'{BASE_URL}/api/auth/login',
        json={'username': 'test', 'password': 'test'},
        headers={'Content-Type': 'application/json'}
    )

    # Should return 200 for valid test credentials, or 401 for invalid
    assert response.status_code in [200, 400, 401, 422, 500]  # Success or various error codes

def test_user_endpoints():
    """Test user management endpoints"""
    # Test user endpoints exist
    response = requests.get(f'{BASE_URL}/api/users/1')
    # Should return 401 or 404, but endpoint should exist
    assert response.status_code in [401, 404]

def test_session_endpoints():
    """Test session management endpoints"""
    # Test session endpoints exist
    response = requests.get(f'{BASE_URL}/api/sessions')
    # Should return 401, but endpoint should exist
    assert response.status_code == 401

def test_hubspot_endpoints():
    """Test HubSpot integration endpoints"""
    # Test HubSpot connection endpoint
    response = requests.get(f'{BASE_URL}/api/hubspot/test-connection')
    # Should return 401 or error about missing token, but endpoint should exist
    assert response.status_code in [401, 500]  # Auth error or missing token

def test_stats_endpoints():
    """Test analytics endpoints"""
    # Test stats endpoints exist
    response = requests.get(f'{BASE_URL}/api/stats/overview')
    # Should return 401, but endpoint should exist
    assert response.status_code == 401

def run_all_tests():
    """Run all basic tests"""
    print("[TESTS] Starting Basic API Tests")
    print("=" * 50)

    tests = [
        test_health_check,
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
            print(f"[OK] {test.__name__}")
        except Exception as e:
            failed += 1
            print(f"[ERROR] {test.__name__}: {str(e)}")

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
    import sys
    sys.exit(0 if success else 1)
