"""
Get a fresh token and test the exact cURL command
"""

import requests
import json

def get_fresh_token_and_test():
    """Get fresh token and test the exact cURL command"""
    
    # Step 1: Get fresh token
    print("Getting fresh token...")
    login_url = "http://89.117.63.196:5000/api/auth/login"
    login_data = {
        "username": "test",
        "password": "test"
    }
    
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
    
    # Step 2: Test with fresh token using direct JSON object
    print("\nTesting with fresh token (direct JSON object)...")
    print("="*60)
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    headers = {"Content-Type": "application/json"}
    
    # Use unique email
    import time
    timestamp = int(time.time())
    unique_email = f"sarah.johnson.{timestamp}@techcorp.com"
    
    data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": {
            "firstname": "Sarah",
            "lastname": "Johnson",
            "email": unique_email,
            "phone": "+1987654321",
            "company": "TechCorp Solutions",
            "jobtitle": "Product Manager",
            "city": "San Francisco",
            "state": "CA",
            "country": "USA",
            "lifecyclestage": "lead"
        }
    }
    
    print(f"Using email: {unique_email}")
    print(f"Token: {token[:50]}...")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"\nSUCCESS! Contact created with ID: {result.get('hubspot_id')}")
        elif response.status_code == 401:
            print("\nERROR - Unauthorized (token issue)")
        elif response.status_code == 400:
            print("\nERROR - Bad Request (likely duplicate email)")
        else:
            print(f"\nERROR - Status {response.status_code}")
            
    except Exception as e:
        print(f"ERROR - {e}")
    
    # Step 3: Show the working cURL command
    print("\n" + "="*60)
    print("WORKING cURL COMMAND:")
    print("="*60)
    
    curl_command = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": {{
      "firstname": "Sarah",
      "lastname": "Johnson",
      "email": "sarah.johnson.unique@techcorp.com",
      "phone": "+1987654321",
      "company": "TechCorp Solutions",
      "jobtitle": "Product Manager",
      "city": "San Francisco",
      "state": "CA",
      "country": "USA",
      "lifecyclestage": "lead"
    }}
  }}' '''
    
    print(curl_command)

if __name__ == "__main__":
    get_fresh_token_and_test()
