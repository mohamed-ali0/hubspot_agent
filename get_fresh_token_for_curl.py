"""
Get a fresh token and generate working cURL commands
"""

import requests
import json
import time

def get_fresh_token_and_curl():
    """Get fresh token and generate cURL commands"""
    
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
    unique_email = f"curl.test.{timestamp}@example.com"
    
    print("\n" + "="*80)
    print("WORKING CURL COMMANDS WITH FRESH TOKEN")
    print("="*80)
    
    print("\n1. STRINGIFIED JSON VERSION:")
    print("-" * 50)
    
    curl_string = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": "{{\\"firstname\\":\\"Michael\\",\\"lastname\\":\\"Chen\\",\\"email\\":\\"{unique_email}\\",\\"phone\\":\\"+1555123456\\",\\"company\\":\\"InnovateTech Corp\\",\\"jobtitle\\":\\"Senior Developer\\",\\"city\\":\\"Seattle\\",\\"state\\":\\"WA\\",\\"country\\":\\"USA\\",\\"lifecyclestage\\":\\"lead\\"}}"
  }}' '''
    
    print(curl_string)
    
    print("\n2. DIRECT JSON OBJECT VERSION:")
    print("-" * 50)
    
    unique_email2 = f"curl.test2.{timestamp}@example.com"
    
    curl_direct = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": {{
      "firstname": "Michael",
      "lastname": "Chen",
      "email": "{unique_email2}",
      "phone": "+1555123456",
      "company": "InnovateTech Corp",
      "jobtitle": "Senior Developer",
      "city": "Seattle",
      "state": "WA",
      "country": "USA",
      "lifecyclestage": "lead"
    }}
  }}' '''
    
    print(curl_direct)
    
    print("\n" + "="*80)
    print("TESTING BOTH COMMANDS")
    print("="*80)
    
    # Test both commands
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    headers = {"Content-Type": "application/json"}
    
    # Test stringified
    print("\nTesting STRINGIFIED JSON:")
    data1 = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"Michael\",\"lastname\":\"Chen\",\"email\":\"{unique_email}\",\"phone\":\"+1555123456\",\"company\":\"InnovateTech Corp\",\"jobtitle\":\"Senior Developer\",\"city\":\"Seattle\",\"state\":\"WA\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    try:
        response1 = requests.post(url, headers=headers, json=data1)
        print(f"Status: {response1.status_code}")
        if response1.status_code == 201:
            print("✅ STRINGIFIED JSON WORKS!")
        else:
            print(f"❌ Error: {response1.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test direct
    print("\nTesting DIRECT JSON OBJECT:")
    data2 = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": {
            "firstname": "Michael",
            "lastname": "Chen",
            "email": unique_email2,
            "phone": "+1555123456",
            "company": "InnovateTech Corp",
            "jobtitle": "Senior Developer",
            "city": "Seattle",
            "state": "WA",
            "country": "USA",
            "lifecyclestage": "lead"
        }
    }
    
    try:
        response2 = requests.post(url, headers=headers, json=data2)
        print(f"Status: {response2.status_code}")
        if response2.status_code == 201:
            print("✅ DIRECT JSON OBJECT WORKS!")
        else:
            print(f"❌ Error: {response2.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_fresh_token_and_curl()
