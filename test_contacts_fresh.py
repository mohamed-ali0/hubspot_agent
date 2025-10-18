"""
Test contacts endpoints with fresh data
"""

import requests
import json
import time

def test_contacts():
    """Test all contacts endpoints"""
    
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
    
    # Generate unique email
    timestamp = int(time.time())
    email = f"john.doe.{timestamp}@example.com"
    
    # Test 1: Create Contact
    print("\n=== TEST 1: CREATE CONTACT ===")
    create_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"John\",\"lastname\":\"Doe\",\"email\":\"{email}\",\"phone\":\"+1234567890\",\"company\":\"Test Company\",\"jobtitle\":\"Software Engineer\",\"city\":\"New York\",\"state\":\"NY\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    raw_json = json.dumps(create_data)
    print("Raw create contact request body:")
    print(raw_json)
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts", json=create_data)
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 201:
            contact_id = response.json().get('hubspot_id')
            print(f"[SUCCESS] Contact created with ID: {contact_id}")
        else:
            print(f"[ERROR] Create contact failed: {response.text}")
            return
    except Exception as e:
        print(f"[ERROR] Create contact error: {e}")
        return
    
    # Test 2: Get All Contacts
    print("\n=== TEST 2: GET ALL CONTACTS ===")
    get_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "limit": 5,
        "properties": ["firstname", "lastname", "email"]
    }
    
    raw_json = json.dumps(get_data)
    print("Raw get contacts request body:")
    print(raw_json)
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/get", json=get_data)
        print(f"Response Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] Got contacts successfully")
        else:
            print(f"[ERROR] Get contacts failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Get contacts error: {e}")
    
    # Test 3: Get Specific Contact
    print("\n=== TEST 3: GET SPECIFIC CONTACT ===")
    get_by_id_data = {
        "token": token,
        "contact_id": contact_id,
        "session_id": 1,
        "chat_message_id": 1
    }
    
    raw_json = json.dumps(get_by_id_data)
    print("Raw get contact by ID request body:")
    print(raw_json)
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/get-by-id", json=get_by_id_data)
        print(f"Response Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] Got contact by ID successfully")
        else:
            print(f"[ERROR] Get contact by ID failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Get contact by ID error: {e}")
    
    # Test 4: Update Contact
    print("\n=== TEST 4: UPDATE CONTACT ===")
    update_data = {
        "token": token,
        "contact_id": contact_id,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": "{\"firstname\":\"Jane\",\"lastname\":\"Smith\",\"jobtitle\":\"Senior Software Engineer\",\"city\":\"San Francisco\",\"state\":\"CA\"}"
    }
    
    raw_json = json.dumps(update_data)
    print("Raw update contact request body:")
    print(raw_json)
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/update", json=update_data)
        print(f"Response Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] Contact updated successfully")
        else:
            print(f"[ERROR] Update contact failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Update contact error: {e}")
    
    # Test 5: Search Contacts
    print("\n=== TEST 5: SEARCH CONTACTS ===")
    search_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "search_term": "John",
        "limit": 5
    }
    
    raw_json = json.dumps(search_data)
    print("Raw search contacts request body:")
    print(raw_json)
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/search", json=search_data)
        print(f"Response Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] Search contacts successful")
        else:
            print(f"[ERROR] Search contacts failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Search contacts error: {e}")
    
    # Test 6: Delete Contact
    print("\n=== TEST 6: DELETE CONTACT ===")
    delete_data = {
        "token": token,
        "contact_id": contact_id,
        "session_id": 1,
        "chat_message_id": 1
    }
    
    raw_json = json.dumps(delete_data)
    print("Raw delete contact request body:")
    print(raw_json)
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/delete", json=delete_data)
        print(f"Response Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] Contact deleted successfully")
        else:
            print(f"[ERROR] Delete contact failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Delete contact error: {e}")

if __name__ == "__main__":
    test_contacts()
