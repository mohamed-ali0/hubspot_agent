"""
Test company creation to see the actual request body format
"""

import requests
import json

def test_company_create():
    """Test company creation with minimal required fields"""
    
    base_url = "http://127.0.0.1:5000"
    
    # Get fresh token
    print("Getting fresh token...")
    try:
        login_response = requests.post(f"{base_url}/api/auth/login", json={"username": "test", "password": "test"})
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print(f"Got token: {token[:50]}...")
        else:
            print(f"Login failed: {login_response.text}")
            return
    except Exception as e:
        print(f"Login error: {e}")
        return
    
    # Test with minimal company data
    print("\nTesting with minimal company data...")
    minimal_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": {
            "name": "Test Company Minimal"
        }
    }
    
    print(f"Request: {json.dumps(minimal_data, indent=2)}")
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/companies/companies", json=minimal_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test with more complete company data
    print("\nTesting with complete company data...")
    complete_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": {
            "name": "Test Company Complete",
            "domain": "testcompany.com",
            "industry": "COMPUTER_SOFTWARE",
            "city": "New York",
            "state": "NY",
            "country": "USA",
            "phone": "+1234567890",
            "website": "https://testcompany.com"
        }
    }
    
    print(f"Request: {json.dumps(complete_data, indent=2)}")
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/companies/companies", json=complete_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_company_create()
