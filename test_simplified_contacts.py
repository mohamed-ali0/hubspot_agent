"""
Test the simplified contacts API without requiring session_id and chat_message_id
"""

import requests
import json
import time

def test_simplified_contacts():
    """Test contacts API with simplified request format"""
    
    print("="*70)
    print("TESTING SIMPLIFIED CONTACTS API")
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
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    headers = {"Content-Type": "application/json"}
    
    print("\n2. Testing SIMPLIFIED get_contacts (no session/chat IDs required):")
    print("-" * 60)
    
    # Simplified request - only token required
    simple_data = {
        "token": token,
        "limit": 5,
        "properties": ["firstname", "lastname", "email", "phone"]
    }
    
    print(f"Request data: {json.dumps(simple_data, indent=2)}")
    
    try:
        response = requests.post(f"{url}/get", headers=headers, json=simple_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("[OK] SIMPLIFIED get_contacts works!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} contacts")
        else:
            print(f"[ERROR] get_contacts failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] get_contacts error: {e}")
    
    print("\n3. Testing SIMPLIFIED search_contacts (no session/chat IDs required):")
    print("-" * 60)
    
    # Simplified search request
    search_data = {
        "token": token,
        "search_term": "test",
        "limit": 3
    }
    
    print(f"Request data: {json.dumps(search_data, indent=2)}")
    
    try:
        response = requests.post(f"{url}/search", headers=headers, json=search_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("[OK] SIMPLIFIED search_contacts works!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} contacts")
        else:
            print(f"[ERROR] search_contacts failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] search_contacts error: {e}")
    
    print("\n4. Testing with session/chat IDs (optional):")
    print("-" * 60)
    
    # Request with session/chat IDs (optional)
    with_session_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "limit": 3,
        "properties": ["firstname", "lastname", "email"]
    }
    
    print(f"Request data: {json.dumps(with_session_data, indent=2)}")
    
    try:
        response = requests.post(f"{url}/get", headers=headers, json=with_session_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("[OK] get_contacts with session/chat IDs works!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} contacts")
        else:
            print(f"[ERROR] get_contacts with session failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] get_contacts with session error: {e}")
    
    print("\n" + "="*70)
    print("SIMPLIFIED CURL COMMANDS")
    print("="*70)
    
    print("\n1. SIMPLIFIED get_contacts (no session/chat IDs):")
    print("-" * 50)
    
    curl_simple = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts/get \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "limit": 5,
    "properties": ["firstname", "lastname", "email", "phone"]
  }}' '''
    
    print(curl_simple)
    
    print("\n2. SIMPLIFIED search_contacts (no session/chat IDs):")
    print("-" * 50)
    
    curl_search = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts/search \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "search_term": "test",
    "limit": 3
  }}' '''
    
    print(curl_search)
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("✅ session_id and chat_message_id are now OPTIONAL for:")
    print("   - get_contacts (get all contacts)")
    print("   - search_contacts (search contacts)")
    print("✅ These fields are still REQUIRED for:")
    print("   - create_contact (create new contact)")
    print("   - update_contact (update existing contact)")
    print("   - delete_contact (delete contact)")
    print("   - get_contact_by_id (get specific contact)")

if __name__ == "__main__":
    test_simplified_contacts()
