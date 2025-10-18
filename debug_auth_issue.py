"""
Debug the authentication issue with stringified JSON
"""

import requests
import json
import time

def debug_auth_issue():
    """Debug why stringified JSON gives 401"""
    
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
    unique_email = f"debug.auth.{timestamp}@example.com"
    
    print("\n" + "="*70)
    print("DEBUGGING AUTHENTICATION ISSUE")
    print("="*70)
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    headers = {"Content-Type": "application/json"}
    
    # Test 1: Check if the issue is with the request format
    print("\n1. Testing with Python requests (should work):")
    print("-" * 50)
    
    data1 = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"Debug\",\"lastname\":\"Auth\",\"email\":\"{unique_email}\",\"phone\":\"+1234567890\",\"company\":\"Debug Company\",\"jobtitle\":\"Debug Engineer\",\"city\":\"Debug City\",\"state\":\"DC\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    print(f"Properties type: {type(data1['properties'])}")
    print(f"Properties value: {data1['properties']}")
    
    try:
        response1 = requests.post(url, headers=headers, json=data1)
        print(f"Status: {response1.status_code}")
        print(f"Response: {response1.text}")
        
        if response1.status_code == 201:
            print("SUCCESS - Python requests works!")
        elif response1.status_code == 401:
            print("ERROR - 401 Unauthorized with Python requests too!")
        else:
            print(f"ERROR - Status {response1.status_code}")
            
    except Exception as e:
        print(f"ERROR - {e}")
    
    # Test 2: Test with raw JSON string (like cURL sends)
    print("\n2. Testing with raw JSON string (like cURL):")
    print("-" * 50)
    
    unique_email2 = f"debug.auth2.{timestamp}@example.com"
    
    # This is exactly what cURL sends
    raw_json = f'''{{
    "token": "{token}",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": "{{\\"firstname\\":\\"Debug\\",\\"lastname\\":\\"Auth2\\",\\"email\\":\\"{unique_email2}\\",\\"phone\\":\\"+1234567890\\",\\"company\\":\\"Debug Company2\\",\\"jobtitle\\":\\"Debug Engineer2\\",\\"city\\":\\"Debug City2\\",\\"state\\":\\"DC\\",\\"country\\":\\"USA\\",\\"lifecyclestage\\":\\"lead\\"}}"
}}'''
    
    print(f"Raw JSON: {raw_json[:200]}...")
    
    try:
        response2 = requests.post(url, headers=headers, data=raw_json)
        print(f"Status: {response2.status_code}")
        print(f"Response: {response2.text}")
        
        if response2.status_code == 201:
            print("SUCCESS - Raw JSON string works!")
        elif response2.status_code == 401:
            print("ERROR - 401 Unauthorized with raw JSON string!")
        else:
            print(f"ERROR - Status {response2.status_code}")
            
    except Exception as e:
        print(f"ERROR - {e}")
    
    # Test 3: Test with a simple request to see if auth works at all
    print("\n3. Testing simple request (direct JSON object):")
    print("-" * 50)
    
    unique_email3 = f"debug.auth3.{timestamp}@example.com"
    
    data3 = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": {
            "firstname": "Debug",
            "lastname": "Auth3",
            "email": unique_email3,
            "phone": "+1234567890",
            "company": "Debug Company3",
            "jobtitle": "Debug Engineer3",
            "city": "Debug City3",
            "state": "DC",
            "country": "USA",
            "lifecyclestage": "lead"
        }
    }
    
    try:
        response3 = requests.post(url, headers=headers, json=data3)
        print(f"Status: {response3.status_code}")
        print(f"Response: {response3.text}")
        
        if response3.status_code == 201:
            print("SUCCESS - Direct JSON object works!")
        elif response3.status_code == 401:
            print("ERROR - 401 Unauthorized with direct JSON object too!")
        else:
            print(f"ERROR - Status {response3.status_code}")
            
    except Exception as e:
        print(f"ERROR - {e}")
    
    print("\n" + "="*70)
    print("DEBUGGING COMPLETED")

if __name__ == "__main__":
    debug_auth_issue()
