"""
Test contacts endpoints with stringified JSON properties
"""

import requests
import json
import time

def test_contacts_string_support():
    """Test contacts endpoints with stringified JSON properties"""
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    headers = {"Content-Type": "application/json"}
    
    # Generate unique email
    timestamp = int(time.time())
    unique_email = f"test.string.{timestamp}@example.com"
    
    print("Testing contacts endpoints with STRINGIFIED JSON properties...")
    print("="*70)
    
    # Test 1: Create Contact with Stringified JSON
    print("\n1. CREATE CONTACT with stringified JSON:")
    print("-" * 50)
    
    create_data = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDc4OTA1MSwianRpIjoiMzY0MDI2NjctODNkNy00MjJmLWJmZmQtMThkNjI2MGUyNzM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzg5MDUxLCJjc3JmIjoiYTBlMWNkODctMjQ2Ni00ZGM1LTgxNjUtOTA0ZDhjZjgwNWUyIiwiZXhwIjoxNzYwNzkyNjUxfQ.6CRv9vx3AJHyQY4lO-t6VcUVXxJvhYPboob5OIVgqMs",
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"String\",\"lastname\":\"Test\",\"email\":\"{unique_email}\",\"phone\":\"+1234567890\",\"company\":\"String Company\",\"jobtitle\":\"String Engineer\",\"city\":\"String City\",\"state\":\"SC\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    print(f"Properties (stringified): {create_data['properties']}")
    
    try:
        response = requests.post(url, headers=headers, json=create_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            contact_id = result.get('hubspot_id')
            print(f"SUCCESS - Contact created with ID: {contact_id}")
        else:
            print(f"ERROR - {response.text}")
            return
    except Exception as e:
        print(f"ERROR - {e}")
        return
    
    # Test 2: Update Contact with Stringified JSON
    print("\n2. UPDATE CONTACT with stringified JSON:")
    print("-" * 50)
    
    update_url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts/update"
    update_data = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDc4OTA1MSwianRpIjoiMzY0MDI2NjctODNkNy00MjJmLWJmZmQtMThkNjI2MGUyNzM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzg5MDUxLCJjc3JmIjoiYTBlMWNkODctMjQ2Ni00ZGM1LTgxNjUtOTA0ZDhjZjgwNWUyIiwiZXhwIjoxNzYwNzkyNjUxfQ.6CRv9vx3AJHyQY4lO-t6VcUVXxJvhYPboob5OIVgqMs",
        "contact_id": contact_id,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": "{\"firstname\":\"Updated\",\"lastname\":\"String\",\"jobtitle\":\"Senior String Engineer\",\"city\":\"Updated String City\"}"
    }
    
    print(f"Properties (stringified): {update_data['properties']}")
    
    try:
        response = requests.post(update_url, headers=headers, json=update_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS - Contact updated with stringified JSON")
        else:
            print(f"ERROR - {response.text}")
    except Exception as e:
        print(f"ERROR - {e}")
    
    # Test 3: Replace Contact with Stringified JSON
    print("\n3. REPLACE CONTACT with stringified JSON:")
    print("-" * 50)
    
    replace_url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts/replace"
    replace_data = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDc4OTA1MSwianRpIjoiMzY0MDI2NjctODNkNy00MjJmLWJmZmQtMThkNjI2MGUyNzM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzg5MDUxLCJjc3JmIjoiYTBlMWNkODctMjQ2Ni00ZGM1LTgxNjUtOTA0ZDhjZjgwNWUyIiwiZXhwIjoxNzYwNzkyNjUxfQ.6CRv9vx3AJHyQY4lO-t6VcUVXxJvhYPboob5OIVgqMs",
        "contact_id": contact_id,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": "{\"firstname\":\"Replaced\",\"lastname\":\"String\",\"email\":\"replaced.string@example.com\",\"phone\":\"+9876543210\",\"company\":\"Replaced String Company\"}"
    }
    
    print(f"Properties (stringified): {replace_data['properties']}")
    
    try:
        response = requests.post(replace_url, headers=headers, json=replace_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS - Contact replaced with stringified JSON")
        else:
            print(f"ERROR - {response.text}")
    except Exception as e:
        print(f"ERROR - {e}")
    
    print("\n" + "="*70)
    print("STRING SUPPORT TEST COMPLETED")

if __name__ == "__main__":
    test_contacts_string_support()
