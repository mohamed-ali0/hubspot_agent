"""
Test edit company endpoint with string properties
"""

import requests
import json

def test_edit_company():
    """Test edit company endpoint with string properties"""
    
    base_url = "http://127.0.0.1:5000"
    
    # Get fresh token
    print("Getting fresh token...")
    try:
        login_response = requests.post(f"{base_url}/api/auth/login", json={"username": "test", "password": "test"})
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print(f"Got token: {token[:50]}...")
        else:
            print(f"Login failed: {login_response.text}")
            return
    except Exception as e:
        print(f"Login error: {e}")
        return
    
    # First, create a company to edit
    print("\nStep 1: Creating a company to edit...")
    create_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": "{\"name\":\"Original Company Name\",\"domain\":\"original.com\",\"industry\":\"COMPUTER_SOFTWARE\",\"city\":\"Boston\",\"state\":\"MA\",\"country\":\"USA\"}"
    }
    
    try:
        create_response = requests.post(f"{base_url}/api/hubspot/companies/companies", json=create_data)
        if create_response.status_code == 201:
            company_id = create_response.json().get('hubspot_id')
            print(f"[SUCCESS] Created company with ID: {company_id}")
        else:
            print(f"[ERROR] Failed to create company: {create_response.text}")
            return
    except Exception as e:
        print(f"[ERROR] Create company error: {e}")
        return
    
    # Now edit the company
    print("\nStep 2: Editing the company...")
    edit_data = {
        "token": token,
        "company_id": company_id,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": "{\"name\":\"Updated Company Name\",\"domain\":\"updated.com\",\"industry\":\"COMPUTER_SOFTWARE\",\"city\":\"San Francisco\",\"state\":\"CA\",\"country\":\"USA\",\"phone\":\"+1987654321\",\"website\":\"https://updated.com\"}"
    }
    
    # Print the raw request body
    raw_json = json.dumps(edit_data)
    print("Raw edit company request body:")
    print(raw_json)
    
    try:
        edit_response = requests.post(f"{base_url}/api/hubspot/companies/companies/update", json=edit_data)
        print(f"\nResponse Status: {edit_response.status_code}")
        
        try:
            response_json = edit_response.json()
            print(f"Response JSON:")
            print(json.dumps(response_json, indent=2))
        except:
            print(f"Response Text: {edit_response.text}")
        
        if edit_response.status_code == 200:
            print("\n[SUCCESS] Company updated successfully!")
            print(f"Updated HubSpot ID: {response_json.get('hubspot_id')}")
        else:
            print(f"\n[ERROR] Company update failed with status {edit_response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] Edit company error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_edit_company()
