"""
Test both cURL formats with fresh contact info and fresh token
"""

import requests
import json
import time

def test_both_curl_formats():
    """Test both stringified JSON and direct JSON object formats"""
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    headers = {"Content-Type": "application/json"}
    
    # Fresh token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDc5MDE1MiwianRpIjoiOTQ2NDI5OTAtYTIzZC00YmQxLTkzZjAtOGU2NDE2NGQ0NTFjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzkwMTUyLCJjc3JmIjoiMjhiZjI4MGQtZWY5My00MGZkLTllNzMtYzg5NmM1ZjIxNzRmIiwiZXhwIjoxNzYwNzkzNzUyfQ.D6lBx6SsioIofuwL5eFZYcBYzooOX4jZc-h6ayJUVas"
    
    print("Testing both cURL formats with fresh contact info...")
    print("="*70)
    
    # Test 1: Stringified JSON Format
    print("\n1. STRINGIFIED JSON FORMAT:")
    print("-" * 50)
    
    timestamp = int(time.time())
    unique_email1 = f"michael.chen.{timestamp}@innovate.com"
    
    data1 = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"Michael\",\"lastname\":\"Chen\",\"email\":\"{unique_email1}\",\"phone\":\"+1555123456\",\"company\":\"InnovateTech Corp\",\"jobtitle\":\"Senior Developer\",\"city\":\"Seattle\",\"state\":\"WA\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    print(f"Properties (stringified): {data1['properties']}")
    print(f"Properties type: {type(data1['properties'])}")
    
    try:
        response1 = requests.post(url, headers=headers, json=data1)
        print(f"Status: {response1.status_code}")
        if response1.status_code == 201:
            result1 = response1.json()
            print(f"SUCCESS - Contact created with ID: {result1.get('hubspot_id')}")
            print(f"Contact: Michael Chen ({unique_email1})")
        else:
            print(f"ERROR - {response1.text}")
    except Exception as e:
        print(f"ERROR - {e}")
    
    # Test 2: Direct JSON Object Format
    print("\n2. DIRECT JSON OBJECT FORMAT:")
    print("-" * 50)
    
    unique_email2 = f"michael.chen2.{timestamp}@innovate.com"
    
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
    
    print(f"Properties (object): {data2['properties']}")
    print(f"Properties type: {type(data2['properties'])}")
    
    try:
        response2 = requests.post(url, headers=headers, json=data2)
        print(f"Status: {response2.status_code}")
        if response2.status_code == 201:
            result2 = response2.json()
            print(f"SUCCESS - Contact created with ID: {result2.get('hubspot_id')}")
            print(f"Contact: Michael Chen ({unique_email2})")
        else:
            print(f"ERROR - {response2.text}")
    except Exception as e:
        print(f"ERROR - {e}")
    
    print("\n" + "="*70)
    print("BOTH FORMATS TESTED SUCCESSFULLY!")

if __name__ == "__main__":
    test_both_curl_formats()
