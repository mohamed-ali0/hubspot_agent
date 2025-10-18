"""
Test the user's cURL command using Python requests
"""

import requests
import json

def test_user_curl():
    """Test the user's exact cURL command"""
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDc4ODYyMCwianRpIjoiYzgwOThlY2ItYTFkOC00YWVjLWIxYzAtODEzZmU5YjViYzA3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzg4NjIwLCJjc3JmIjoiMmYzYzM4MGYtZjBiMy00NTM4LWExNGMtZDM4ZjQxODEyNGYyIiwiZXhwIjoxNzYwNzkyMjIwfQ.WItzDBCLXUcqaGGcIk3BGdoHXP9U7XQElrE8ArWgmgU",
        "session_id": 1,
        "chat_message_id": 1,
        "properties": "{\"firstname\":\"John\",\"lastname\":\"Doe\",\"email\":\"john.doe@example.com\",\"phone\":\"+1234567890\",\"company\":\"Test Company\",\"jobtitle\":\"Software Engineer\",\"city\":\"New York\",\"state\":\"NY\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}"
    }
    
    print("Testing your cURL command...")
    print(f"URL: {url}")
    print(f"Method: POST")
    print(f"Headers: {headers}")
    print(f"Data: {json.dumps(data, indent=2)}")
    print("\n" + "="*50)
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 201:
            print("\n[SUCCESS] Contact created successfully!")
            result = response.json()
            if 'hubspot_id' in result:
                print(f"HubSpot ID: {result['hubspot_id']}")
        else:
            print(f"\n[ERROR] Request failed with status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection failed - server might not be running on 89.117.63.196:5000")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    test_user_curl()
