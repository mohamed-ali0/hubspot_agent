"""
Simple example of body-based JWT authentication
"""

import requests
import json

def demonstrate_body_auth():
    """Demonstrate the new body-based authentication"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("Body-Based JWT Authentication Demo")
    print("=" * 40)
    
    # Step 1: Get JWT Token (same as before)
    print("Step 1: Getting JWT token...")
    try:
        login_response = requests.post(f'{base_url}/api/auth/login', 
                                      json={'username': 'test', 'password': 'test'})
        
        if login_response.status_code == 200:
            token = login_response.json()['token']
            print(f"[SUCCESS] Token obtained: {token[:50]}...")
        else:
            print(f"[ERROR] Login failed: {login_response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to server. Make sure Flask is running on http://127.0.0.1:5000")
        return
    
    # Step 2: GET Companies with body token (NEW WAY)
    print("\nStep 2: GET companies with body token...")
    try:
        response = requests.get(
            f"{base_url}/api/hubspot/companies/companies",
            json={"token": token},  # Token in body instead of header
            params={"limit": 3, "properties": "name,domain"}
        )
        
        if response.status_code == 200:
            data = response.json()
            companies = data.get('results', [])
            print(f"[SUCCESS] Found {len(companies)} companies:")
            for company in companies:
                props = company.get('properties', {})
                name = props.get('name', 'N/A')
                domain = props.get('domain', 'N/A')
                print(f"  - {name} ({domain})")
        else:
            print(f"[ERROR] Request failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Request error: {str(e)}")
    
    # Step 3: CREATE Company with body token (NEW WAY)
    print("\nStep 3: CREATE company with body token...")
    try:
        create_data = {
            "token": token,  # Token in body
            "session_id": 1,
            "chat_message_id": 1,
            "properties": {
                "name": "Test Company Body Auth",
                "domain": "testbodyauth.com",
                "industry": "TECHNOLOGY",
                "phone": "+1-555-0123"
            }
        }
        
        response = requests.post(
            f"{base_url}/api/hubspot/companies/companies",
            json=create_data
        )
        
        if response.status_code == 201:
            data = response.json()
            company_id = data.get('hubspot_id')
            print(f"[SUCCESS] Company created with ID: {company_id}")
        else:
            print(f"[ERROR] Create failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Create error: {str(e)}")
    
    print("\n" + "=" * 40)
    print("Body-Based Authentication Summary:")
    print("- Token goes in request body instead of Authorization header")
    print("- All requests use JSON body format")
    print("- Simpler integration for clients")
    print("- Better logging and tracking")

if __name__ == "__main__":
    demonstrate_body_auth()
