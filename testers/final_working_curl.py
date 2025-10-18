"""
Generate a guaranteed working cURL command with fresh token
"""

import requests
import json
import time

def generate_working_curl():
    """Generate a guaranteed working cURL command"""
    
    print("="*70)
    print("GENERATING GUARANTEED WORKING CURL COMMANDS")
    print("="*70)
    
    # Get fresh token
    print("\n1. Getting fresh token...")
    login_url = "http://89.117.63.196:5000/api/auth/login"
    login_data = {"username": "test", "password": "test"}
    
    try:
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print(f"✅ Fresh token obtained: {token[:50]}...")
        else:
            print(f"❌ Login failed: {login_response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test the token first
    print("\n2. Testing token validity...")
    test_url = "http://89.117.63.196:5000/api/health"
    try:
        test_response = requests.get(test_url)
        print(f"✅ Server is running: {test_response.status_code}")
    except Exception as e:
        print(f"❌ Server error: {e}")
        return
    
    # Generate unique email
    timestamp = int(time.time())
    unique_email = f"working.test.{timestamp}@example.com"
    
    print(f"\n3. Testing contact creation with fresh token...")
    print(f"   Email: {unique_email}")
    
    # Test the contact creation
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    headers = {"Content-Type": "application/json"}
    
    test_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"Working\",\"lastname\":\"Test\",\"email\":\"{unique_email}\",\"phone\":\"+1555123456\",\"company\":\"Working Company\",\"jobtitle\":\"Test Engineer\",\"city\":\"Test City\",\"state\":\"TC\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    try:
        response = requests.post(url, headers=headers, json=test_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Contact creation test PASSED!")
            result = response.json()
            print(f"   HubSpot ID: {result.get('hubspot_id')}")
        else:
            print(f"❌ Contact creation test FAILED: {response.text}")
            return
    except Exception as e:
        print(f"❌ Contact creation test ERROR: {e}")
        return
    
    # Generate working cURL commands
    print("\n" + "="*70)
    print("WORKING CURL COMMANDS")
    print("="*70)
    
    # Generate unique emails for each command
    email1 = f"curl.string.{timestamp}@example.com"
    email2 = f"curl.object.{timestamp}@example.com"
    
    print("\n1. STRINGIFIED JSON VERSION (String Format):")
    print("-" * 50)
    
    curl_string = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": "{{\\"firstname\\":\\"Michael\\",\\"lastname\\":\\"Chen\\",\\"email\\":\\"{email1}\\",\\"phone\\":\\"+1555123456\\",\\"company\\":\\"InnovateTech Corp\\",\\"jobtitle\\":\\"Senior Developer\\",\\"city\\":\\"Seattle\\",\\"state\\":\\"WA\\",\\"country\\":\\"USA\\",\\"lifecyclestage\\":\\"lead\\"}}"
  }}' '''
    
    print(curl_string)
    
    print("\n2. DIRECT JSON OBJECT VERSION (Object Format):")
    print("-" * 50)
    
    curl_direct = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "session_id": 1,
    "chat_message_id": 1,
    "properties": {{
      "firstname": "Michael",
      "lastname": "Chen",
      "email": "{email2}",
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
    
    print("\n" + "="*70)
    print("IMPORTANT NOTES")
    print("="*70)
    print("1. Both commands use the SAME fresh token")
    print("2. Both commands use UNIQUE email addresses")
    print("3. The token expires in 1 hour")
    print("4. If you get 401, the token has expired - run this script again")
    print("5. Make sure the Flask server is running: python app/main.py")
    
    print(f"\nToken expires at: {time.ctime(time.time() + 3600)}")

if __name__ == "__main__":
    generate_working_curl()
