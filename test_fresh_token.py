"""
Test with the fresh token provided by user
"""

import requests
import json

def test_fresh_token():
    """Test with fresh token"""
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDc4OTA1MSwianRpIjoiMzY0MDI2NjctODNkNy00MjJmLWJmZmQtMThkNjI2MGUyNzM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzg5MDUxLCJjc3JmIjoiYTBlMWNkODctMjQ2Ni00ZGM1LTgxNjUtOTA0ZDhjZjgwNWUyIiwiZXhwIjoxNzYwNzkyNjUxfQ.6CRv9vx3AJHyQY4lO-t6VcUVXxJvhYPboob5OIVgqMs",
        "session_id": 1,
        "chat_message_id": 1,
        "properties": "{\"firstname\":\"John\",\"lastname\":\"Doe\",\"email\":\"john.doe@example.com\",\"phone\":\"+1234567890\",\"company\":\"Test Company\",\"jobtitle\":\"Software Engineer\",\"city\":\"New York\",\"state\":\"NY\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}"
    }
    
    print("Testing with fresh token...")
    print(f"URL: {url}")
    print(f"Token: {data['token'][:50]}...")
    print("\n" + "="*50)
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 201:
            print("\n[SUCCESS] Contact created successfully!")
            result = response.json()
            if 'hubspot_id' in result:
                print(f"HubSpot ID: {result['hubspot_id']}")
        elif response.status_code == 400:
            print("\n[ERROR] Bad Request - Check your data")
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

if __name__ == "__main__":
    test_fresh_token()
