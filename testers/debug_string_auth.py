"""
Debug why stringified JSON gives 401 while direct JSON works
"""

import requests
import json
import time

def debug_string_auth_issue():
    """Debug the authentication issue with stringified JSON"""
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    headers = {"Content-Type": "application/json"}
    
    # Get fresh token first
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
    unique_email = f"debug.test.{timestamp}@example.com"
    
    print("\n" + "="*70)
    print("DEBUGGING AUTHENTICATION ISSUE")
    print("="*70)
    
    # Test 1: Direct JSON Object (WORKS)
    print("\n1. Testing DIRECT JSON OBJECT (should work):")
    print("-" * 50)
    
    data1 = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": {
            "firstname": "Debug",
            "lastname": "Test",
            "email": unique_email,
            "phone": "+1234567890",
            "company": "Debug Company",
            "jobtitle": "Debug Engineer",
            "city": "Debug City",
            "state": "DC",
            "country": "USA",
            "lifecyclestage": "lead"
        }
    }
    
    print(f"Properties type: {type(data1['properties'])}")
    print(f"Token: {data1['token'][:50]}...")
    
    try:
        response1 = requests.post(url, headers=headers, json=data1)
        print(f"Status: {response1.status_code}")
        if response1.status_code == 201:
            print("SUCCESS - Direct JSON object works!")
        elif response1.status_code == 401:
            print("ERROR - 401 Unauthorized")
        else:
            print(f"ERROR - Status {response1.status_code}")
        print(f"Response: {response1.text[:200]}...")
    except Exception as e:
        print(f"ERROR - {e}")
    
    # Test 2: Stringified JSON (FAILS with 401)
    print("\n2. Testing STRINGIFIED JSON (gives 401):")
    print("-" * 50)
    
    unique_email2 = f"debug.test2.{timestamp}@example.com"
    
    data2 = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"Debug\",\"lastname\":\"Test2\",\"email\":\"{unique_email2}\",\"phone\":\"+1234567890\",\"company\":\"Debug Company2\",\"jobtitle\":\"Debug Engineer2\",\"city\":\"Debug City2\",\"state\":\"DC\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    print(f"Properties type: {type(data2['properties'])}")
    print(f"Properties value: {data2['properties']}")
    print(f"Token: {data2['token'][:50]}...")
    
    try:
        response2 = requests.post(url, headers=headers, json=data2)
        print(f"Status: {response2.status_code}")
        if response2.status_code == 201:
            print("SUCCESS - Stringified JSON works!")
        elif response2.status_code == 401:
            print("ERROR - 401 Unauthorized (this is the issue!)")
        else:
            print(f"ERROR - Status {response2.status_code}")
        print(f"Response: {response2.text}")
    except Exception as e:
        print(f"ERROR - {e}")
    
    # Test 3: Check if it's a JSON parsing issue
    print("\n3. Testing JSON parsing in the endpoint:")
    print("-" * 50)
    
    # Let's manually test the JSON parsing
    try:
        # Simulate what happens in the endpoint
        properties_str = data2['properties']
        parsed_properties = json.loads(properties_str)
        print(f"Stringified JSON parses correctly: {type(parsed_properties)}")
        print(f"Parsed content: {parsed_properties}")
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
    except Exception as e:
        print(f"Other error: {e}")
    
    print("\n" + "="*70)
    print("DEBUGGING COMPLETED")

if __name__ == "__main__":
    debug_string_auth_issue()
