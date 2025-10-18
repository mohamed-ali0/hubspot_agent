"""
Test the exact cURL command to identify the difference
"""

import requests
import json
import time

def test_exact_curl():
    """Test the exact cURL command format"""
    
    # Get fresh token
    print("Getting fresh token...")
    login_url = "http://89.117.63.196:5000/api/auth/login"
    login_data = {"username": "test", "password": "test"}
    
    try:
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print(f"Fresh token: {token}")
        else:
            print(f"Login failed: {login_response.text}")
            return
    except Exception as e:
        print(f"Login error: {e}")
        return
    
    # Generate unique email
    timestamp = int(time.time())
    unique_email = f"curl.exact.{timestamp}@example.com"
    
    print("\n" + "="*70)
    print("TESTING EXACT CURL COMMAND")
    print("="*70)
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    headers = {"Content-Type": "application/json"}
    
    # This is the EXACT format from your cURL command
    print("\n1. Testing EXACT cURL format (stringified JSON):")
    print("-" * 50)
    
    # The exact JSON that cURL sends
    exact_curl_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"Michael\",\"lastname\":\"Chen\",\"email\":\"{unique_email}\",\"phone\":\"+1555123456\",\"company\":\"InnovateTech Corp\",\"jobtitle\":\"Senior Developer\",\"city\":\"Seattle\",\"state\":\"WA\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    print(f"Request data: {json.dumps(exact_curl_data, indent=2)}")
    print(f"Properties type: {type(exact_curl_data['properties'])}")
    print(f"Properties value: {exact_curl_data['properties']}")
    
    try:
        response = requests.post(url, headers=headers, json=exact_curl_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("SUCCESS - Exact cURL format works!")
        elif response.status_code == 401:
            print("ERROR - 401 Unauthorized with exact cURL format!")
        else:
            print(f"ERROR - Status {response.status_code}")
            
    except Exception as e:
        print(f"ERROR - {e}")
    
    # Test 2: Test with the exact cURL command as a string
    print("\n2. Testing with exact cURL command string:")
    print("-" * 50)
    
    unique_email2 = f"curl.exact2.{timestamp}@example.com"
    
    # This is the exact cURL command as a string
    curl_command = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": "{{\\"firstname\\":\\"Michael\\",\\"lastname\\":\\"Chen\\",\\"email\\":\\"{unique_email2}\\",\\"phone\\":\\"+1555123456\\",\\"company\\":\\"InnovateTech Corp\\",\\"jobtitle\\":\\"Senior Developer\\",\\"city\\":\\"Seattle\\",\\"state\\":\\"WA\\",\\"country\\":\\"USA\\",\\"lifecyclestage\\":\\"lead\\"}}"
  }}' '''
    
    print("cURL command:")
    print(curl_command)
    
    # Extract the JSON part and test it
    json_part = f'''{{
    "token": "{token}",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": "{{\\"firstname\\":\\"Michael\\",\\"lastname\\":\\"Chen\\",\\"email\\":\\"{unique_email2}\\",\\"phone\\":\\"+1555123456\\",\\"company\\":\\"InnovateTech Corp\\",\\"jobtitle\\":\\"Senior Developer\\",\\"city\\":\\"Seattle\\",\\"state\\":\\"WA\\",\\"country\\":\\"USA\\",\\"lifecyclestage\\":\\"lead\\"}}"
}}'''
    
    print(f"\nJSON part: {json_part}")
    
    try:
        response2 = requests.post(url, headers=headers, data=json_part)
        print(f"Status: {response2.status_code}")
        print(f"Response: {response2.text}")
        
        if response2.status_code == 201:
            print("SUCCESS - cURL command string works!")
        elif response2.status_code == 401:
            print("ERROR - 401 Unauthorized with cURL command string!")
        else:
            print(f"ERROR - Status {response2.status_code}")
            
    except Exception as e:
        print(f"ERROR - {e}")
    
    print("\n" + "="*70)
    print("TESTING COMPLETED")

if __name__ == "__main__":
    test_exact_curl()
