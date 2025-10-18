"""
Debug the delete_company 500 error
"""

import requests
import json

def test_delete_with_debug():
    """Test delete_company endpoint with detailed debugging"""
    
    base_url = "http://127.0.0.1:5000"
    
    # First, get a fresh token
    print("Step 1: Getting fresh token...")
    try:
        login_data = {
            "username": "test",
            "password": "test"
        }
        
        login_response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        print(f"Login Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token = login_response.json().get('access_token')
            print(f"[SUCCESS] Got token: {token[:50]}...")
        else:
            print(f"[ERROR] Login failed: {login_response.text}")
            return
    except Exception as e:
        print(f"[ERROR] Login error: {e}")
        return
    
    # Test delete_company endpoint
    print("\nStep 2: Testing delete_company endpoint...")
    
    delete_data = {
        "token": token,
        "company_id": "264244139217",
        "session_id": 1,
        "chat_message_id": 1
    }
    
    print(f"Request URL: {base_url}/api/hubspot/companies/companies/delete")
    print(f"Request Data: {json.dumps(delete_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{base_url}/api/hubspot/companies/companies/delete", 
            json=delete_data,
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"Response JSON: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            print("\n[SUCCESS] Delete company request successful!")
        elif response.status_code == 500:
            print("\n[ERROR] 500 Internal Server Error - Check server logs")
        else:
            print(f"\n[ERROR] Delete company failed with status {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out")
    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection error - is the server running?")
    except Exception as e:
        print(f"[ERROR] Request error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_delete_with_debug()
