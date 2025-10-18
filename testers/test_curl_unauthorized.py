"""
Test the exact cURL command that's giving unauthorized error
"""

import requests
import json
import time

def test_unauthorized_curl():
    """Test the exact cURL command that's failing"""
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    headers = {"Content-Type": "application/json"}
    
    # Generate unique email
    timestamp = int(time.time())
    unique_email = f"sarah.johnson.{timestamp}@techcorp.com"
    
    print("Testing the EXACT cURL command that's failing...")
    print("="*60)
    
    # Test 1: Direct JSON Object (what you're using - FAILS)
    print("\n1. Testing DIRECT JSON OBJECT (your current format):")
    print("-" * 50)
    
    data1 = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDc4OTA1MSwianRpIjoiMzY0MDI2NjctODNkNy00MjJmLWJmZmQtMThkNjI2MGUyNzM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzg5MDUxLCJjc3JmIjoiYTBlMWNkODctMjQ2Ni00ZGM1LTgxNjUtOTA0ZDhjZjgwNWUyIiwiZXhwIjoxNzYwNzkyNjUxfQ.6CRv9vx3AJHyQY4lO-t6VcUVXxJvhYPboob5OIVgqMs",
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
    
    print(f"Properties type: {type(data1['properties'])}")
    print(f"Properties: {data1['properties']}")
    
    try:
        response1 = requests.post(url, headers=headers, json=data1)
        print(f"Status: {response1.status_code}")
        print(f"Response: {response1.text}")
        
        if response1.status_code == 201:
            print("SUCCESS - Direct JSON object works!")
        elif response1.status_code == 401:
            print("ERROR - Unauthorized (token issue)")
        else:
            print(f"ERROR - Status {response1.status_code}")
    except Exception as e:
        print(f"ERROR - {e}")
    
    # Test 2: Stringified JSON (correct format)
    print("\n2. Testing STRINGIFIED JSON (correct format):")
    print("-" * 50)
    
    unique_email2 = f"sarah.johnson2.{timestamp}@techcorp.com"
    
    data2 = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDc4OTA1MSwianRpIjoiMzY0MDI2NjctODNkNy00MjJmLWJmZmQtMThkNjI2MGUyNzM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzg5MDUxLCJjc3JmIjoiYTBlMWNkODctMjQ2Ni00ZGM1LTgxNjUtOTA0ZDhjZjgwNWUyIiwiZXhwIjoxNzYwNzkyNjUxfQ.6CRv9vx3AJHyQY4lO-t6VcUVXxJvhYPboob5OIVgqMs",
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"Sarah\",\"lastname\":\"Johnson\",\"email\":\"{unique_email2}\",\"phone\":\"+1987654321\",\"company\":\"TechCorp Solutions\",\"jobtitle\":\"Product Manager\",\"city\":\"San Francisco\",\"state\":\"CA\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    print(f"Properties type: {type(data2['properties'])}")
    print(f"Properties: {data2['properties']}")
    
    try:
        response2 = requests.post(url, headers=headers, json=data2)
        print(f"Status: {response2.status_code}")
        print(f"Response: {response2.text}")
        
        if response2.status_code == 201:
            print("SUCCESS - Stringified JSON works!")
        elif response2.status_code == 401:
            print("ERROR - Unauthorized (token issue)")
        else:
            print(f"ERROR - Status {response2.status_code}")
    except Exception as e:
        print(f"ERROR - {e}")
    
    print("\n" + "="*60)
    print("TEST COMPLETED")

if __name__ == "__main__":
    test_unauthorized_curl()
