"""
Test the get_contact_by_id endpoint with the provided data
"""

import requests
import json

def test_get_contact_by_id():
    """Test get_contact_by_id with the provided data"""
    
    print("="*70)
    print("TESTING get_contact_by_id ENDPOINT")
    print("="*70)
    
    # The data provided by user
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDc5MTg3NSwianRpIjoiN2I2ZGE3Y2QtNDhmNC00YTcwLThlMDItNzE0NzRkYWE5NTYyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzkxODc1LCJjc3JmIjoiYWNjZWRhZDktNWY1MC00MGY5LThiM2YtYWU4NzU2ZGIyMjU3IiwiZXhwIjoxNzYwNzk1NDc1fQ.AA-3vE3c32av_I07MjRbrYzgOnrLwgArnQ1nbIvNB6k"
    contact_id = "488730796248"
    
    print(f"Token: {token[:50]}...")
    print(f"Contact ID: {contact_id}")
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts/get-by-id"
    headers = {"Content-Type": "application/json"}
    
    # Test 1: Correct format (single object)
    print("\n1. Testing CORRECT format (single object):")
    print("-" * 50)
    
    correct_data = {
        "token": token,
        "contact_id": contact_id
    }
    
    print(f"Request data: {json.dumps(correct_data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=correct_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("[OK] get_contact_by_id works with correct format!")
        else:
            print(f"[ERROR] get_contact_by_id failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] get_contact_by_id error: {e}")
    
    # Test 2: Array format (what user provided)
    print("\n2. Testing ARRAY format (what you provided):")
    print("-" * 50)
    
    array_data = [{
        "token": token,
        "contact_id": contact_id
    }]
    
    print(f"Request data: {json.dumps(array_data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=array_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("[OK] get_contact_by_id works with array format!")
        else:
            print(f"[ERROR] get_contact_by_id failed with array format: {response.text}")
    except Exception as e:
        print(f"[ERROR] get_contact_by_id error with array: {e}")
    
    # Test 3: With session/chat IDs (optional)
    print("\n3. Testing with session/chat IDs (optional):")
    print("-" * 50)
    
    with_session_data = {
        "token": token,
        "contact_id": contact_id,
        "session_id": 1,
        "chat_message_id": 1
    }
    
    print(f"Request data: {json.dumps(with_session_data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=with_session_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("[OK] get_contact_by_id works with session/chat IDs!")
        else:
            print(f"[ERROR] get_contact_by_id failed with session: {response.text}")
    except Exception as e:
        print(f"[ERROR] get_contact_by_id error with session: {e}")
    
    print("\n" + "="*70)
    print("WORKING CURL COMMAND")
    print("="*70)
    
    curl_command = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/contacts/contacts/get-by-id \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "contact_id": "{contact_id}"
  }}' '''
    
    print(curl_command)

if __name__ == "__main__":
    test_get_contact_by_id()
