"""
Test with properties as string with NO escaped quotes at all
"""

import requests
import json

def test_real_no_escapes():
    """Test with properties as string with NO escaped quotes"""
    
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
    
    # Test with properties as string with NO escaped quotes
    print("\nTesting with properties as string with NO escaped quotes...")
    
    # This is what you want - a string with regular quotes, NO escapes
    properties_string = '{"name":"Test Company Real No Escapes","domain":"testcompany.com","industry":"COMPUTER_SOFTWARE","city":"New York","state":"NY","country":"USA","phone":"+1234567890","website":"https://testcompany.com"}'
    
    # Create the request data manually to avoid JSON escaping
    request_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": properties_string
    }
    
    # Print the raw request body without any decoration
    raw_json = json.dumps(request_data)
    print("Raw request body:")
    print(raw_json)
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/companies/companies", json=request_data)
        print(f"\nResponse Status: {response.status_code}")
        
        try:
            response_json = response.json()
            print(f"Response JSON:")
            print(json.dumps(response_json, indent=2))
        except:
            print(f"Response Text: {response.text}")
        
        if response.status_code == 201:
            print("\n[SUCCESS] Company created with string with NO escaped quotes!")
            print(f"HubSpot ID: {response_json.get('hubspot_id')}")
        else:
            print(f"\n[ERROR] Company creation failed with status {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] Request error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_no_escapes()
