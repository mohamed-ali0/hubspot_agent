"""
Test script to verify database logging is working
"""

import requests
import json
import time

def test_logging():
    base_url = "http://127.0.0.1:5000"
    
    # Authenticate
    print("Authenticating...")
    response = requests.post(f"{base_url}/api/auth/login", 
                           json={"username": "test", "password": "test"})
    
    if response.status_code != 200:
        print(f"Authentication failed: {response.status_code}")
        return
    
    token = response.json().get('token')
    headers = {"Authorization": f"Bearer {token}"}
    print("Authentication successful!")
    
    # Create a contact to trigger logging
    print("\nCreating contact to test logging...")
    contact_data = {
        "session_id": 1,
        "chat_message_id": 1,
        "properties": {
            "firstname": "Test",
            "lastname": "Logging",
            "email": f"test.logging{int(time.time())}@example.com",
            "phone": "+1-555-9999"
        }
    }
    
    response = requests.post(f"{base_url}/api/hubspot/contacts/contacts", 
                           json=contact_data, headers=headers)
    
    if response.status_code == 201:
        print("Contact created successfully!")
        contact_id = response.json().get('hubspot_id')
        print(f"Contact ID: {contact_id}")
    else:
        print(f"Contact creation failed: {response.status_code}")
        print(f"Response: {response.text}")
        return
    
    # Check logs immediately
    print("\nChecking logs...")
    response = requests.get(f"{base_url}/api/logs", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        logs = data.get('logs', [])
        print(f"Found {len(logs)} logs in database")
        
        if logs:
            print("\nLog details:")
            for log in logs:
                print(f"  - Type: {log.get('log_type')}")
                print(f"    HubSpot ID: {log.get('hubspot_id')}")
                print(f"    Status: {log.get('sync_status')}")
                print(f"    Created: {log.get('created_at')}")
                print()
        else:
            print("No logs found. This indicates a logging issue.")
    else:
        print(f"Failed to get logs: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    test_logging()
