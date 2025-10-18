"""
Test the exact cURL command equivalent to see if there's a difference
"""

import requests
import json
import time

def test_curl_equivalent():
    """Test the exact equivalent of the cURL command"""
    
    # Get fresh token
    print("Getting fresh token...")
    login_url = "http://89.117.63.196:5000/api/auth/login"
    login_data = {"username": "test", "password": "test"}
    
    try:
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print(f"Fresh token: {token[:50]}...")
        else:
            print(f"Login failed: {login_response.text}")
            return
    except Exception as e:
        print(f"Login error: {e}")
        return
    
    # Generate unique email
    timestamp = int(time.time())
    unique_email = f"curl.test.{timestamp}@example.com"
    
    print("\n" + "="*70)
    print("TESTING CURL EQUIVALENT")
    print("="*70)
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    headers = {"Content-Type": "application/json"}
    
    # Test the exact cURL command format
    print("\n1. Testing STRINGIFIED JSON (cURL equivalent):")
    print("-" * 50)
    
    # This is exactly what the cURL command sends
    data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"Michael\",\"lastname\":\"Chen\",\"email\":\"{unique_email}\",\"phone\":\"+1555123456\",\"company\":\"InnovateTech Corp\",\"jobtitle\":\"Senior Developer\",\"city\":\"Seattle\",\"state\":\"WA\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    print(f"Request data type: {type(data)}")
    print(f"Properties type: {type(data['properties'])}")
    print(f"Properties value: {data['properties']}")
    print(f"Token length: {len(data['token'])}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("SUCCESS - Stringified JSON works!")
        elif response.status_code == 401:
            print("ERROR - 401 Unauthorized (this is what you got)")
        else:
            print(f"ERROR - Status {response.status_code}")
            
    except Exception as e:
        print(f"ERROR - {e}")
    
    print("\n2. Testing with raw JSON string (like cURL -d):")
    print("-" * 50)
    
    # Test with raw JSON string like cURL sends
    raw_json = f'''{{
    "token": "{token}",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": "{{\\"firstname\\":\\"Michael\\",\\"lastname\\":\\"Chen\\",\\"email\\":\\"{unique_email}2\\",\\"phone\\":\\"+1555123456\\",\\"company\\":\\"InnovateTech Corp\\",\\"jobtitle\\":\\"Senior Developer\\",\\"city\\":\\"Seattle\\",\\"state\\":\\"WA\\",\\"country\\":\\"USA\\",\\"lifecyclestage\\":\\"lead\\"}}"
}}'''
    
    print(f"Raw JSON: {raw_json[:200]}...")
    
    try:
        response = requests.post(url, headers=headers, data=raw_json)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("SUCCESS - Raw JSON string works!")
        elif response.status_code == 401:
            print("ERROR - 401 Unauthorized")
        else:
            print(f"ERROR - Status {response.status_code}")
            
    except Exception as e:
        print(f"ERROR - {e}")

if __name__ == "__main__":
    test_curl_equivalent()
