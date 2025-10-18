"""
Test new contact data with cURL command
"""

import requests
import json
import time

def test_new_contact():
    """Test with new contact data"""
    
    url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Generate unique email with timestamp
    timestamp = int(time.time())
    unique_email = f"sarah.johnson.{timestamp}@techcorp.com"
    
    data = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDc4OTA1MSwianRpIjoiMzY0MDI2NjctODNkNy00MjJmLWJmZmQtMThkNjI2MGUyNzM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzg5MDUxLCJjc3JmIjoiYTBlMWNkODctMjQ2Ni00ZGM1LTgxNjUtOTA0ZDhjZjgwNWUyIiwiZXhwIjoxNzYwNzkyNjUxfQ.6CRv9vx3AJHyQY4lO-t6VcUVXxJvhYPboob5OIVgqMs",
        "session_id": 1,
        "chat_message_id": 1,
        "properties": f"{{\"firstname\":\"Sarah\",\"lastname\":\"Johnson\",\"email\":\"{unique_email}\",\"phone\":\"+1987654321\",\"company\":\"TechCorp Solutions\",\"jobtitle\":\"Product Manager\",\"city\":\"San Francisco\",\"state\":\"CA\",\"country\":\"USA\",\"lifecyclestage\":\"lead\"}}"
    }
    
    print("Testing new contact data...")
    print(f"URL: {url}")
    print(f"Name: Sarah Johnson")
    print(f"Email: {unique_email}")
    print(f"Company: TechCorp Solutions")
    print(f"Job Title: Product Manager")
    print(f"Location: San Francisco, CA")
    print("\n" + "="*60)
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 201:
            print("\n[SUCCESS] New contact created successfully!")
            result = response.json()
            if 'hubspot_id' in result:
                print(f"HubSpot ID: {result['hubspot_id']}")
                print(f"Contact Name: Sarah Johnson")
                print(f"Contact Email: {unique_email}")
                return result['hubspot_id']
        elif response.status_code == 400:
            print("\n[ERROR] Bad Request - Check your data")
            print("Error details:", response.text)
        elif response.status_code == 401:
            print("\n[ERROR] Unauthorized - Token might be invalid")
        elif response.status_code == 500:
            print("\n[ERROR] Server Error - Check server logs")
        else:
            print(f"\n[ERROR] Unexpected status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection failed - server might not be running")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    return None

if __name__ == "__main__":
    contact_id = test_new_contact()
    if contact_id:
        print(f"\nSUCCESS! New contact created with ID: {contact_id}")
    else:
        print("\nFAILED! Contact creation failed")
