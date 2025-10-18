"""
Test both JSON formats to fix the cURL error
"""

import requests
import json
import time

def test_json_formats():
    """Test both stringified and object JSON formats"""
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    headers = {"Content-Type": "application/json"}
    
    # Generate unique email
    timestamp = int(time.time())
    unique_email = f"sarah.johnson.{timestamp}@techcorp.com"
    
    print("Testing both JSON formats...")
    print("="*60)
    
    # Test 1: Stringified JSON (original format)
    print("\n1. Testing STRINGIFIED JSON format:")
    print("-" * 40)
    
    data1 = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDc4OTA1MSwianRpIjoiMzY0MDI2NjctODNkNy00MjJmLWJmZmQtMThkNjI2MGUyNzM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzg5MDUxLCJjc3JmIjoiYTBlMWNkODctMjQ2Ni00ZGM1LTgxNjUtOTA0ZDhjZjgwNWUyIiwiZXhwIjoxNzYwNzkyNjUxfQ.6CRv9vx3AJHyQY4lO-t6VcUVXxJvhYPboob5OIVgqMs",
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"Sarah\",\"lastname\":\"Johnson\",\"email\":\"{unique_email}\",\"phone\":\"+1987654321\",\"company\":\"TechCorp Solutions\",\"jobtitle\":\"Product Manager\",\"city\":\"San Francisco\",\"state\":\"CA\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    try:
        response1 = requests.post(url, headers=headers, json=data1)
        print(f"Status: {response1.status_code}")
        if response1.status_code == 201:
            print("SUCCESS - Stringified JSON works!")
            result1 = response1.json()
            print(f"Contact ID: {result1.get('hubspot_id')}")
        else:
            print(f"ERROR - {response1.text}")
    except Exception as e:
        print(f"ERROR - {e}")
    
    # Test 2: Direct JSON Object
    print("\n2. Testing DIRECT JSON OBJECT format:")
    print("-" * 40)
    
    unique_email2 = f"sarah.johnson2.{timestamp}@techcorp.com"
    
    data2 = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDc4OTA1MSwianRpIjoiMzY0MDI2NjctODNkNy00MjJmLWJmZmQtMThkNjI2MGUyNzM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzg5MDUxLCJjc3JmIjoiYTBlMWNkODctMjQ2Ni00ZGM1LTgxNjUtOTA0ZDhjZjgwNWUyIiwiZXhwIjoxNzYwNzkyNjUxfQ.6CRv9vx3AJHyQY4lO-t6VcUVXxJvhYPboob5OIVgqMs",
        "session_id": 1,
        "chat_message_id": 1,
        "properties": {
            "firstname": "Sarah",
            "lastname": "Johnson",
            "email": unique_email2,
            "phone": "+1987654321",
            "company": "TechCorp Solutions",
            "jobtitle": "Product Manager",
            "city": "San Francisco",
            "state": "CA",
            "country": "USA",
            "lifecyclestage": "lead"
        }
    }
    
    try:
        response2 = requests.post(url, headers=headers, json=data2)
        print(f"Status: {response2.status_code}")
        if response2.status_code == 201:
            print("SUCCESS - Direct JSON object works!")
            result2 = response2.json()
            print(f"Contact ID: {result2.get('hubspot_id')}")
        else:
            print(f"ERROR - {response2.text}")
    except Exception as e:
        print(f"ERROR - {e}")

if __name__ == "__main__":
    test_json_formats()
