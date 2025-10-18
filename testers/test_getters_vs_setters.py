"""
Test the difference between getters (no session/chat IDs needed) and setters (session/chat IDs required)
"""

import requests
import json
import time

def test_getters_vs_setters():
    """Test getters vs setters logic"""
    
    print("="*70)
    print("TESTING GETTERS vs SETTERS LOGIC")
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
    
    print("\n2. Testing GETTERS (should work without session/chat IDs):")
    print("-" * 60)
    
    # Test get_contacts (getter)
    print("\n   a) get_contacts (getter):")
    get_data = {
        "token": token,
        "limit": 3,
        "properties": ["firstname", "lastname", "email"]
    }
    
    print(f"   Request: {json.dumps(get_data, indent=2)}")
    
    try:
        response = requests.post(f"{url}/get", headers=headers, json=get_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   [OK] get_contacts works without session/chat IDs!")
        else:
            print(f"   [ERROR] get_contacts failed: {response.text}")
    except Exception as e:
        print(f"   [ERROR] get_contacts error: {e}")
    
    # Test search_contacts (getter)
    print("\n   b) search_contacts (getter):")
    search_data = {
        "token": token,
        "search_term": "test",
        "limit": 2
    }
    
    print(f"   Request: {json.dumps(search_data, indent=2)}")
    
    try:
        response = requests.post(f"{url}/search", headers=headers, json=search_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   [OK] search_contacts works without session/chat IDs!")
        else:
            print(f"   [ERROR] search_contacts failed: {response.text}")
    except Exception as e:
        print(f"   [ERROR] search_contacts error: {e}")
    
    # Test get_contact_by_id (getter)
    print("\n   c) get_contact_by_id (getter):")
    # First get a contact ID from the previous request
    try:
        get_response = requests.post(f"{url}/get", headers=headers, json={
            "token": token,
            "limit": 1,
            "properties": ["firstname", "lastname", "email"]
        })
        if get_response.status_code == 200:
            result = get_response.json()
            if result.get('results'):
                contact_id = result['results'][0]['id']
                print(f"   Using contact ID: {contact_id}")
                
                get_by_id_data = {
                    "token": token,
                    "contact_id": contact_id
                }
                
                print(f"   Request: {json.dumps(get_by_id_data, indent=2)}")
                
                response = requests.post(f"{url}/get-by-id", headers=headers, json=get_by_id_data)
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    print("   [OK] get_contact_by_id works without session/chat IDs!")
                else:
                    print(f"   [ERROR] get_contact_by_id failed: {response.text}")
            else:
                print("   [SKIP] No contacts found to test get_contact_by_id")
        else:
            print("   [SKIP] Could not get contact ID for testing")
    except Exception as e:
        print(f"   [ERROR] get_contact_by_id error: {e}")
    
    print("\n3. Testing SETTERS (require session/chat IDs):")
    print("-" * 60)
    
    # Test create_contact (setter)
    print("\n   a) create_contact (setter):")
    timestamp = int(time.time())
    unique_email = f"test.getter.{timestamp}@example.com"
    
    create_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": {
            "firstname": "Test",
            "lastname": "Getter",
            "email": unique_email,
            "phone": "+1234567890",
            "company": "Test Company",
            "jobtitle": "Test Engineer",
            "city": "Test City",
            "state": "TC",
            "country": "USA",
            "lifecyclestage": "lead"
        }
    }
    
    print(f"   Request: {json.dumps(create_data, indent=2)}")
    
    try:
        response = requests.post(f"{url}", headers=headers, json=create_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   [OK] create_contact works with session/chat IDs!")
            result = response.json()
            print(f"   Created contact ID: {result.get('hubspot_id')}")
        else:
            print(f"   [ERROR] create_contact failed: {response.text}")
    except Exception as e:
        print(f"   [ERROR] create_contact error: {e}")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("GETTERS (read operations) - session_id and chat_message_id are OPTIONAL:")
    print("  - get_contacts (get all contacts)")
    print("  - search_contacts (search contacts)")
    print("  - get_contact_by_id (get specific contact)")
    print("")
    print("SETTERS (write operations) - session_id and chat_message_id are REQUIRED:")
    print("  - create_contact (create new contact)")
    print("  - update_contact (update existing contact)")
    print("  - delete_contact (delete contact)")
    print("  - replace_contact (replace contact)")
    print("  - batch operations")
    
    print("\n" + "="*70)
    print("WORKING CURL COMMANDS")
    print("="*70)
    
    print("\n1. GETTERS (no session/chat IDs needed):")
    print("-" * 50)
    
    print("get_contacts:")
    curl_get = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts/get \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "limit": 5,
    "properties": ["firstname", "lastname", "email"]
  }}' '''
    print(curl_get)
    
    print("\nsearch_contacts:")
    curl_search = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts/search \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "search_term": "test",
    "limit": 3
  }}' '''
    print(curl_search)
    
    print("\n2. SETTERS (session/chat IDs required):")
    print("-" * 50)
    
    print("create_contact:")
    curl_create = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": {{
      "firstname": "John",
      "lastname": "Doe",
      "email": "john.doe@example.com",
      "phone": "+1234567890",
      "company": "Example Corp",
      "jobtitle": "Engineer",
      "city": "New York",
      "state": "NY",
      "country": "USA",
      "lifecyclestage": "lead"
    }}
  }}' '''
    print(curl_create)

if __name__ == "__main__":
    test_getters_vs_setters()
