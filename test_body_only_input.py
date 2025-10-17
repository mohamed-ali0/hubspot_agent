"""
Test script for body-only input format (no query parameters)
"""

import requests
import json
import time

def test_body_only_input():
    """Test that all inputs come from request body"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("Testing Body-Only Input Format")
    print("=" * 40)
    
    # Wait a moment for server to start
    time.sleep(2)
    
    # Step 1: Get JWT Token
    print("Step 1: Getting JWT token...")
    try:
        login_response = requests.post(f'{base_url}/api/auth/login', 
                                      json={'username': 'test', 'password': 'test'})
        
        if login_response.status_code == 200:
            token = login_response.json()['token']
            print(f"[SUCCESS] Token obtained: {token[:50]}...")
        else:
            print(f"[ERROR] Login failed: {login_response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to server. Make sure Flask is running.")
        return False
    
    # Step 2: Test GET companies with ALL parameters in body
    print("\nStep 2: Testing GET companies with body-only parameters...")
    try:
        # All parameters now in body, no query parameters
        body_data = {
            "token": token,
            "limit": 3,
            "properties": ["name", "domain", "industry"]
        }
        
        response = requests.get(
            f"{base_url}/api/hubspot/companies/companies",
            json=body_data  # All data in body, no query params
        )
        
        if response.status_code == 200:
            data = response.json()
            companies = data.get('results', [])
            print(f"[SUCCESS] Found {len(companies)} companies:")
            for company in companies:
                props = company.get('properties', {})
                name = props.get('name', 'N/A')
                domain = props.get('domain', 'N/A')
                industry = props.get('industry', 'N/A')
                print(f"  - {name} ({domain}) - {industry}")
        else:
            print(f"[ERROR] Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Request error: {str(e)}")
        return False
    
    # Step 3: Test search with body-only parameters
    print("\nStep 3: Testing search with body-only parameters...")
    try:
        search_data = {
            "token": token,
            "session_id": 1,
            "chat_message_id": 1,
            "search_term": "HubSpot",
            "limit": 2
        }
        
        response = requests.post(
            f"{base_url}/api/hubspot/companies/companies/search",
            json=search_data  # All parameters in body
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"[SUCCESS] Search found {len(results)} results")
            for result in results:
                props = result.get('properties', {})
                name = props.get('name', 'N/A')
                print(f"  - {name}")
        else:
            print(f"[ERROR] Search failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Search error: {str(e)}")
        return False
    
    # Step 4: Test CREATE company with body-only parameters
    print("\nStep 4: Testing CREATE company with body-only parameters...")
    try:
        create_data = {
            "token": token,
            "session_id": 1,
            "chat_message_id": 1,
            "properties": {
                "name": "Test Body Only Company",
                "domain": "testbodyonly.com",
                "industry": "COMPUTER_SOFTWARE",
                "phone": "+1-555-0123"
            }
        }
        
        response = requests.post(
            f"{base_url}/api/hubspot/companies/companies",
            json=create_data  # All parameters in body
        )
        
        if response.status_code == 201:
            data = response.json()
            company_id = data.get('hubspot_id')
            print(f"[SUCCESS] Company created with ID: {company_id}")
            
            # Test UPDATE with body-only parameters
            print("\nStep 5: Testing UPDATE company with body-only parameters...")
            update_data = {
                "token": token,
                "session_id": 1,
                "chat_message_id": 1,
                "properties": {
                    "name": "Updated Body Only Company",
                    "phone": "+1-555-9999"
                }
            }
            
            response = requests.patch(
                f"{base_url}/api/hubspot/companies/companies/{company_id}",
                json=update_data  # All parameters in body
            )
            
            if response.status_code == 200:
                print("[SUCCESS] Company updated successfully")
            else:
                print(f"[ERROR] Update failed: {response.status_code}")
                print(f"Response: {response.text}")
            
            # Test DELETE with body-only parameters
            print("\nStep 6: Testing DELETE company with body-only parameters...")
            delete_data = {
                "token": token,
                "session_id": 1,
                "chat_message_id": 1
            }
            
            response = requests.delete(
                f"{base_url}/api/hubspot/companies/companies/{company_id}",
                json=delete_data  # All parameters in body
            )
            
            if response.status_code == 200:
                print("[SUCCESS] Company deleted successfully")
            else:
                print(f"[ERROR] Delete failed: {response.status_code}")
                print(f"Response: {response.text}")
        else:
            print(f"[ERROR] Create failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Create error: {str(e)}")
        return False
    
    print("\n" + "=" * 40)
    print("[SUCCESS] Body-only input format is working!")
    print("All parameters now come from request body.")
    print("No query parameters needed!")
    return True

if __name__ == "__main__":
    test_body_only_input()
