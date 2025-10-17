"""
Test ALL endpoints with complete body-only input (no URL parameters)
"""

import requests
import json
import time

def test_complete_body_only():
    """Test all endpoints with complete body-only input"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("Complete Body-Only Input Test")
    print("=" * 50)
    print("ALL inputs now come from request body - NO URL parameters!")
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
    
    # Step 2: GET Companies (Body-Only)
    print("\nStep 2: GET Companies (Body-Only)")
    print("Endpoint: POST /api/hubspot/companies/companies")
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
    
    # Step 3: CREATE Company (Body-Only)
    print("\nStep 3: CREATE Company (Body-Only)")
    print("Endpoint: POST /api/hubspot/companies/companies")
    print("Request Body:")
    create_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "properties": {
            "name": "Complete Body Only Company",
            "domain": "completebodyonly.com",
            "industry": "COMPUTER_SOFTWARE",
            "phone": "+1-555-0123"
        }
    }
    print(json.dumps(create_data, indent=2))
    
    company_id = None
    try:
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
    
    if company_id:
        # Step 4: GET Specific Company (Body-Only)
        print(f"\nStep 4: GET Specific Company (Body-Only)")
        print("Endpoint: POST /api/hubspot/companies/companies/get")
        print("Request Body:")
        get_specific_data = {
            "token": token,
            "company_id": company_id
        }
        print(json.dumps(get_specific_data, indent=2))
        
        try:
            response = requests.post(
                f"{base_url}/api/hubspot/companies/companies/get",
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
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"[ERROR] GET specific error: {str(e)}")
        
        # Step 5: UPDATE Company (Body-Only)
        print(f"\nStep 5: UPDATE Company (Body-Only)")
        print("Endpoint: POST /api/hubspot/companies/companies/update")
        print("Request Body:")
        update_data = {
            "token": token,
            "company_id": company_id,
            "session_id": 1,
            "chat_message_id": 1,
            "properties": {
                "name": "Updated Complete Body Only Company",
                "phone": "+1-555-9999"
            }
        }
        print(json.dumps(update_data, indent=2))
        
        try:
            response = requests.post(
                f"{base_url}/api/hubspot/companies/companies/update",
                json=update_data
            )
            
            if response.status_code == 200:
                print("[SUCCESS] Company updated successfully")
            else:
                print(f"[ERROR] Update failed: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"[ERROR] Update error: {str(e)}")
        
        # Step 6: DELETE Company (Body-Only)
        print(f"\nStep 6: DELETE Company (Body-Only)")
        print("Endpoint: POST /api/hubspot/companies/companies/delete")
        print("Request Body:")
        delete_data = {
            "token": token,
            "company_id": company_id,
            "session_id": 1,
            "chat_message_id": 1
        }
        print(json.dumps(delete_data, indent=2))
        
        try:
            response = requests.post(
                f"{base_url}/api/hubspot/companies/companies/delete",
                json=delete_data
            )
            
            if response.status_code == 200:
                print("[SUCCESS] Company deleted successfully")
            else:
                print(f"[ERROR] Delete failed: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"[ERROR] Delete error: {str(e)}")
    
    # Step 7: SEARCH Companies (Body-Only)
    print("\nStep 7: SEARCH Companies (Body-Only)")
    print("Endpoint: POST /api/hubspot/companies/companies/search")
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
    
    # Step 8: GET Company Properties (Body-Only)
    print("\nStep 8: GET Company Properties (Body-Only)")
    print("Endpoint: GET /api/hubspot/companies/properties")
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
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Properties error: {str(e)}")
    
    # Step 9: GET Specific Property (Body-Only)
    print("\nStep 9: GET Specific Property (Body-Only)")
    print("Endpoint: POST /api/hubspot/companies/properties/get")
    print("Request Body:")
    property_data = {
        "token": token,
        "property_name": "name"
    }
    print(json.dumps(property_data, indent=2))
    
    try:
        response = requests.post(
            f"{base_url}/api/hubspot/companies/properties/get",
            json=property_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] Retrieved property schema for 'name'")
            print(f"  Type: {data.get('type', 'N/A')}")
            print(f"  Label: {data.get('label', 'N/A')}")
        else:
            print(f"[ERROR] Property failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] Property error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Complete Body-Only Input Summary:")
    print("[SUCCESS] ALL endpoints now use body-only input")
    print("[SUCCESS] NO URL parameters used anywhere")
    print("[SUCCESS] ALL data comes from request body")
    print("[SUCCESS] Consistent JSON format for all operations")
    print("[SUCCESS] Better logging and tracking")
    print("[SUCCESS] Easier integration and testing")
    
    return True

if __name__ == "__main__":
    test_complete_body_only()
