"""
Test current behavior and provide working cURL commands
"""

import requests
import json
import time

def test_current_behavior():
    """Test current behavior and provide working commands"""
    
    print("="*70)
    print("TESTING CURRENT CONTACTS API BEHAVIOR")
    print("="*70)
    
    # Get fresh token
    print("\n1. Getting fresh token...")
    login_url = "http://89.117.63.196:5000/api/auth/login"
    login_data = {"username": "test", "password": "test"}
    
    try:
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print(f"[OK] Fresh token obtained: {token[:50]}...")
        else:
            print(f"[ERROR] Login failed: {login_response.text}")
            return
    except Exception as e:
        print(f"[ERROR] Login error: {e}")
        return
    
    print("\n2. Testing get_contacts with session/chat IDs (current behavior):")
    print("-" * 60)
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    headers = {"Content-Type": "application/json"}
    
    # Test with session/chat IDs (current working format)
    data_with_session = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "limit": 5,
        "properties": ["firstname", "lastname", "email", "phone"]
    }
    
    print(f"Request data: {json.dumps(data_with_session, indent=2)}")
    
    try:
        response = requests.post(f"{url}/get", headers=headers, json=data_with_session)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("[OK] get_contacts with session/chat IDs works!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} contacts")
        else:
            print(f"[ERROR] get_contacts failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] get_contacts error: {e}")
    
    print("\n3. Testing search_contacts with session/chat IDs (current behavior):")
    print("-" * 60)
    
    # Test search with session/chat IDs
    search_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "search_term": "test",
        "limit": 3
    }
    
    print(f"Request data: {json.dumps(search_data, indent=2)}")
    
    try:
        response = requests.post(f"{url}/search", headers=headers, json=search_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("[OK] search_contacts with session/chat IDs works!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} contacts")
        else:
            print(f"[ERROR] search_contacts failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] search_contacts error: {e}")
    
    print("\n" + "="*70)
    print("CURRENT WORKING CURL COMMANDS")
    print("="*70)
    print("NOTE: session_id and chat_message_id are currently REQUIRED")
    print("(The server needs to be restarted for the optional changes to take effect)")
    
    print("\n1. get_contacts (with session/chat IDs):")
    print("-" * 50)
    
    curl_get = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts/get \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "session_id": 1,
    "chat_message_id": 1,
    "limit": 5,
    "properties": ["firstname", "lastname", "email", "phone"]
  }}' '''
    
    print(curl_get)
    
    print("\n2. search_contacts (with session/chat IDs):")
    print("-" * 50)
    
    curl_search = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts/search \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "session_id": 1,
    "chat_message_id": 1,
    "search_term": "test",
    "limit": 3
  }}' '''
    
    print(curl_search)
    
    print("\n" + "="*70)
    print("TO MAKE session_id and chat_message_id OPTIONAL:")
    print("="*70)
    print("1. Stop the Flask server (Ctrl+C in the terminal running it)")
    print("2. Restart it: python app/main.py")
    print("3. Then the simplified format will work without session/chat IDs")

if __name__ == "__main__":
    test_current_behavior()
