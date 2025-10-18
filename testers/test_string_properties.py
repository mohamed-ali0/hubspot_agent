"""
Test company creation with stringified properties
"""

import requests
import json

def test_string_properties():
    """Test company creation with properties as string"""
    
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
    
    # Test with properties as string (your format)
    print("\nTesting with properties as string...")
    string_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": '{"name":"Test Company String","domain":"testcompany.com","industry":"COMPUTER_SOFTWARE","city":"New York","state":"NY","country":"USA","phone":"+1234567890","website":"https://testcompany.com"}'
    }
    
    print(f"Request: {json.dumps(string_data, indent=2)}")
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/companies/companies", json=string_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("\n[SUCCESS] Company created with string properties!")
        else:
            print(f"\n[ERROR] Company creation failed with status {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Test with properties as object (original format)
    print("\nTesting with properties as object...")
    object_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": {
            "name": "Test Company Object",
            "domain": "testcompany.com",
            "industry": "COMPUTER_SOFTWARE",
            "city": "New York",
            "state": "NY",
            "country": "USA",
            "phone": "+1234567890",
            "website": "https://testcompany.com"
        }
    }
    
    print(f"Request: {json.dumps(object_data, indent=2)}")
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/companies/companies", json=object_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("\n[SUCCESS] Company created with object properties!")
        else:
            print(f"\n[ERROR] Company creation failed with status {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_string_properties()
