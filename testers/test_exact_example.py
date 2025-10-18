"""
Test with the exact example provided by user
"""

import requests
import json

def test_exact_example():
    """Test with the exact request body format provided"""
    
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
    
    # Test with the EXACT example provided by user
    print("\nTesting with EXACT user example...")
    exact_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": "{\"name\":\"Test Company Complete\",\"domain\":\"testcompany.com\",\"industry\":\"COMPUTER_SOFTWARE\",\"city\":\"New York\",\"state\":\"NY\",\"country\":\"USA\",\"phone\":\"+1234567890\",\"website\":\"https://testcompany.com\"}"
    }
    
    print("Request Body:")
    print(json.dumps(exact_data, indent=2))
    print("\nProperties string (as provided):")
    print(exact_data["properties"])
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/companies/companies", json=exact_data)
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"Response JSON:")
            print(json.dumps(response_json, indent=2))
        except:
            print(f"Response Text: {response.text}")
        
        if response.status_code == 201:
            print("\n🎉 [SUCCESS] Company created with EXACT user example!")
            print(f"HubSpot ID: {response_json.get('hubspot_id')}")
        else:
            print(f"\n❌ [ERROR] Company creation failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ [ERROR] Request error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_exact_example()
