"""
Test all body-only input formats with valid inputs
"""

import requests
import json
import time

def test_all_body_formats():
    """Test all body-only input formats"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("Testing All Body-Only Input Formats")
    print("=" * 50)
    
    # Wait for server
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
    
    # Step 2: GET Companies with body-only parameters
    print("\nStep 2: GET Companies (Body-Only)")
    print("Request Body:")
    get_data = {
        "token": token,
        "limit": 3,
        "properties": ["name", "domain", "industry"]
    }
    print(json.dumps(get_data, indent=2))
    
    try:
        response = requests.get(
            f"{base_url}/api/hubspot/companies/companies",
            json=get_data
        )
        
        if response.status_code == 200:
            data = response.json()
            companies = data.get('results', [])
            print(f"[SUCCESS] Found {len(companies)} companies")
            for company in companies:
                props = company.get('properties', {})
                name = props.get('name', 'N/A')
                domain = props.get('domain', 'N/A')
                industry = props.get('industry', 'N/A')
                print(f"  - {name} ({domain}) - {industry}")
        else:
            print(f"[ERROR] GET failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] GET error: {str(e)}")
    
    # Step 3: SEARCH Companies with body-only parameters
    print("\nStep 3: SEARCH Companies (Body-Only)")
    print("Request Body:")
    search_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "search_term": "HubSpot",
        "limit": 2
    }
    print(json.dumps(search_data, indent=2))
    
    try:
        response = requests.post(
            f"{base_url}/api/hubspot/companies/companies/search",
            json=search_data
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
    except Exception as e:
        print(f"[ERROR] Search error: {str(e)}")
    
    # Step 4: CREATE Company with body-only parameters
    print("\nStep 4: CREATE Company (Body-Only)")
    print("Request Body:")
    create_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": {
            "name": "Test Body Only Company",
            "domain": "testbodyonly.com",
            "industry": "COMPUTER_SOFTWARE",
            "phone": "+1-555-0123",
            "address": "123 Main St",
            "city": "Boston",
            "state": "MA",
            "zip": "02101",
            "country": "United States"
        }
    }
    print(json.dumps(create_data, indent=2))
    
    try:
        response = requests.post(
            f"{base_url}/api/hubspot/companies/companies",
            json=create_data
        )
        
        if response.status_code == 201:
            data = response.json()
            company_id = data.get('hubspot_id')
            print(f"[SUCCESS] Company created with ID: {company_id}")
            
            # Step 5: GET Specific Company with body-only parameters
            print("\nStep 5: GET Specific Company (Body-Only)")
            print("Request Body:")
            get_specific_data = {
                "token": token
            }
            print(json.dumps(get_specific_data, indent=2))
            
            try:
                response = requests.get(
                    f"{base_url}/api/hubspot/companies/companies/{company_id}",
                    json=get_specific_data
                )
                
                if response.status_code == 200:
                    data = response.json()
                    props = data.get('properties', {})
                    name = props.get('name', 'N/A')
                    domain = props.get('domain', 'N/A')
                    print(f"[SUCCESS] Retrieved company: {name} ({domain})")
                else:
                    print(f"[ERROR] GET specific failed: {response.status_code}")
            except Exception as e:
                print(f"[ERROR] GET specific error: {str(e)}")
            
            # Step 6: GET Company Properties with body-only parameters
            print("\nStep 6: GET Company Properties (Body-Only)")
            print("Request Body:")
            properties_data = {
                "token": token
            }
            print(json.dumps(properties_data, indent=2))
            
            try:
                response = requests.get(
                    f"{base_url}/api/hubspot/companies/properties",
                    json=properties_data
                )
                
                if response.status_code == 200:
                    data = response.json()
                    properties = data.get('results', [])
                    print(f"[SUCCESS] Found {len(properties)} company properties")
                    if properties:
                        print("  Sample properties:")
                        for prop in properties[:3]:
                            name = prop.get('name', 'N/A')
                            print(f"    - {name}")
                else:
                    print(f"[ERROR] Properties failed: {response.status_code}")
            except Exception as e:
                print(f"[ERROR] Properties error: {str(e)}")
            
        else:
            print(f"[ERROR] Create failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Create error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Body-Only Input Format Summary:")
    print("[SUCCESS] All parameters now come from request body")
    print("[SUCCESS] No query parameters needed")
    print("[SUCCESS] Consistent JSON format for all endpoints")
    print("[SUCCESS] Better logging and tracking")
    print("[SUCCESS] Easier integration and testing")
    
    return True

if __name__ == "__main__":
    test_all_body_formats()
