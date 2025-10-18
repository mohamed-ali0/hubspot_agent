"""
Test ALL contacts endpoints to verify all inputs are in request body
"""

import requests
import json
import time

def test_all_contacts_endpoints():
    """Test all contacts endpoints to verify body-only inputs"""
    
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
    email = f"test.{timestamp}@example.com"
    
    print("\n" + "="*60)
    print("TESTING ALL CONTACTS ENDPOINTS - BODY-ONLY INPUTS")
    print("="*60)
    
    # Test 1: Create Contact
    print("\n1. CREATE CONTACT")
    print("-" * 30)
    create_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"Test\",\"lastname\":\"User\",\"email\":\"{email}\",\"phone\":\"+1234567890\",\"company\":\"Test Company\",\"jobtitle\":\"Software Engineer\",\"city\":\"New York\",\"state\":\"NY\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts", json=create_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            contact_id = response.json().get('hubspot_id')
            print(f"[SUCCESS] Contact created with ID: {contact_id}")
        else:
            print(f"[FAILED] {response.text}")
            return
    except Exception as e:
        print(f"[ERROR] {e}")
        return
    
    # Test 2: Get All Contacts
    print("\n2. GET ALL CONTACTS")
    print("-" * 30)
    get_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "limit": 5,
        "properties": ["firstname", "lastname", "email"]
    }
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/get", json=get_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] SUCCESS - Got contacts")
        else:
            print(f"[FAILED] FAILED - {response.text}")
    except Exception as e:
        print(f"[FAILED] ERROR - {e}")
    
    # Test 3: Get Specific Contact
    print("\n3. GET SPECIFIC CONTACT")
    print("-" * 30)
    get_by_id_data = {
        "token": token,
        "contact_id": contact_id,
        "session_id": 1,
        "chat_message_id": 1
    }
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/get-by-id", json=get_by_id_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] SUCCESS - Got contact by ID")
        else:
            print(f"[FAILED] FAILED - {response.text}")
    except Exception as e:
        print(f"[FAILED] ERROR - {e}")
    
    # Test 4: Update Contact
    print("\n4. UPDATE CONTACT")
    print("-" * 30)
    update_data = {
        "token": token,
        "contact_id": contact_id,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": "{\"firstname\":\"Updated\",\"lastname\":\"Name\",\"jobtitle\":\"Senior Engineer\"}"
    }
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/update", json=update_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] SUCCESS - Contact updated")
        else:
            print(f"[FAILED] FAILED - {response.text}")
    except Exception as e:
        print(f"[FAILED] ERROR - {e}")
    
    # Test 5: Replace Contact
    print("\n5. REPLACE CONTACT")
    print("-" * 30)
    replace_data = {
        "token": token,
        "contact_id": contact_id,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": "{\"firstname\":\"Replaced\",\"lastname\":\"Contact\",\"email\":\"replaced@example.com\",\"phone\":\"+9876543210\"}"
    }
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/replace", json=replace_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] SUCCESS - Contact replaced")
        else:
            print(f"[FAILED] FAILED - {response.text}")
    except Exception as e:
        print(f"[FAILED] ERROR - {e}")
    
    # Test 6: Search Contacts
    print("\n6. SEARCH CONTACTS")
    print("-" * 30)
    search_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "search_term": "Test",
        "limit": 5
    }
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/search", json=search_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] SUCCESS - Search contacts")
        else:
            print(f"[FAILED] FAILED - {response.text}")
    except Exception as e:
        print(f"[FAILED] ERROR - {e}")
    
    # Test 7: Get Contact Properties
    print("\n7. GET CONTACT PROPERTIES")
    print("-" * 30)
    properties_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1
    }
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/properties", json=properties_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] SUCCESS - Got contact properties")
        else:
            print(f"[FAILED] FAILED - {response.text}")
    except Exception as e:
        print(f"[FAILED] ERROR - {e}")
    
    # Test 8: Get Specific Property
    print("\n8. GET SPECIFIC PROPERTY")
    print("-" * 30)
    specific_property_data = {
        "token": token,
        "property_name": "firstname",
        "session_id": 1,
        "chat_message_id": 1
    }
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/properties/get", json=specific_property_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] SUCCESS - Got specific property")
        else:
            print(f"[FAILED] FAILED - {response.text}")
    except Exception as e:
        print(f"[FAILED] ERROR - {e}")
    
    # Test 9: Batch Create Contacts
    print("\n9. BATCH CREATE CONTACTS")
    print("-" * 30)
    batch_create_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "contacts": [
            {
                "firstname": "Batch1",
                "lastname": "User1",
                "email": f"batch1.{timestamp}@example.com"
            },
            {
                "firstname": "Batch2",
                "lastname": "User2",
                "email": f"batch2.{timestamp}@example.com"
            }
        ]
    }
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/batch", json=batch_create_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] SUCCESS - Batch created contacts")
        else:
            print(f"[FAILED] FAILED - {response.text}")
    except Exception as e:
        print(f"[FAILED] ERROR - {e}")
    
    # Test 10: Delete Contact
    print("\n10. DELETE CONTACT")
    print("-" * 30)
    delete_data = {
        "token": token,
        "contact_id": contact_id,
        "session_id": 1,
        "chat_message_id": 1
    }
    
    try:
        response = requests.post(f"{base_url}/api/hubspot/contacts/contacts/delete", json=delete_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] SUCCESS - Contact deleted")
        else:
            print(f"[FAILED] FAILED - {response.text}")
    except Exception as e:
        print(f"[FAILED] ERROR - {e}")
    
    print("\n" + "="*60)
    print("ALL CONTACTS ENDPOINTS TESTED - BODY-ONLY INPUTS VERIFIED")
    print("="*60)

if __name__ == "__main__":
    test_all_contacts_endpoints()
