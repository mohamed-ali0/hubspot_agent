"""
Test contact creation with unique email to ensure success
"""

import requests
import json
import time

def test_successful_contact():
    """Test contact creation with unique email"""
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Generate unique email with timestamp
    timestamp = int(time.time())
    unique_email = f"john.doe.{timestamp}@example.com"
    
    data = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDc4OTA1MSwianRpIjoiMzY0MDI2NjctODNkNy00MjJmLWJmZmQtMThkNjI2MGUyNzM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzg5MDUxLCJjc3JmIjoiYTBlMWNkODctMjQ2Ni00ZGM1LTgxNjUtOTA0ZDhjZjgwNWUyIiwiZXhwIjoxNzYwNzkyNjUxfQ.6CRv9vx3AJHyQY4lO-t6VcUVXxJvhYPboob5OIVgqMs",
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"John\",\"lastname\":\"Doe\",\"email\":\"{unique_email}\",\"phone\":\"+1234567890\",\"company\":\"Test Company\",\"jobtitle\":\"Software Engineer\",\"city\":\"New York\",\"state\":\"NY\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    print("Testing contact creation with unique email...")
    print(f"URL: {url}")
    print(f"Unique Email: {unique_email}")
    print(f"Token: {data['token'][:50]}...")
    print("\n" + "="*60)
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 201:
            print("\n[SUCCESS] Contact created successfully!")
            result = response.json()
            if 'hubspot_id' in result:
                print(f"HubSpot ID: {result['hubspot_id']}")
                print(f"Contact Email: {unique_email}")
                return result['hubspot_id']
        elif response.status_code == 400:
            print("\n[ERROR] Bad Request - Check your data")
            print("Error details:", response.text)
        elif response.status_code == 401:
            print("\n[ERROR] Unauthorized - Token might be invalid")
        elif response.status_code == 500:
            print("\n[ERROR] Server Error - Check server logs")
        else:
            print(f"\n[ERROR] Unexpected status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection failed - server might not be running")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    return None

if __name__ == "__main__":
    contact_id = test_successful_contact()
    if contact_id:
        print(f"\n🎉 SUCCESS! Contact created with ID: {contact_id}")
    else:
        print("\n❌ FAILED! Contact creation failed")
