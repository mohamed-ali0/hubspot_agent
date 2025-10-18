"""
Test script for body-based JWT authentication
"""

import requests
import json

def test_body_authentication():
    """Test the new body-based authentication system"""
    
    base_url = "http://127.0.0.1:5000"
    
    # First, get a token
    print("Step 1: Getting JWT token...")
    login_response = requests.post(f'{base_url}/api/auth/login', 
                                  json={'username': 'test', 'password': 'test'})
    
    if login_response.status_code != 200:
        print(f"[ERROR] Login failed: {login_response.text}")
        return False
    
    token = login_response.json()['token']
    print(f"[SUCCESS] Token obtained: {token[:50]}...")
    
    # Test 1: GET Companies with body token
    print("\nStep 2: Testing GET companies with body token...")
    companies_data = {
        "token": token
    }
    
    response = requests.get(
        f"{base_url}/api/hubspot/companies/companies",
        json=companies_data,
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
        print(f"[ERROR] Companies API failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    # Test 2: GET Company Properties with body token
    print("\nStep 3: Testing GET company properties with body token...")
    properties_data = {
        "token": token
    }
    
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
            for prop in properties[:5]:  # Show first 5
                name = prop.get('name', 'N/A')
                print(f"    - {name}")
    else:
        print(f"[ERROR] Properties API failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    # Test 3: CREATE Company with body token
    print("\nStep 4: Testing CREATE company with body token...")
    create_data = {
        "token": token,
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
        
        # Test 4: UPDATE Company with body token
        print("\nStep 5: Testing UPDATE company with body token...")
        update_data = {
            "token": token,
            "session_id": 1,
            "chat_message_id": 1,
            "properties": {
                "name": "Updated Test Company",
                "phone": "+1-555-9999"
            }
        }
        
        response = requests.patch(
            f"{base_url}/api/hubspot/companies/companies/{company_id}",
            json=update_data
        )
        
        if response.status_code == 200:
            print("[SUCCESS] Company updated successfully")
        else:
            print(f"[ERROR] Update failed: {response.status_code}")
            print(f"Response: {response.text}")
        
        # Test 5: DELETE Company with body token
        print("\nStep 6: Testing DELETE company with body token...")
        delete_data = {
            "token": token,
            "session_id": 1,
            "chat_message_id": 1
        }
        
        response = requests.delete(
            f"{base_url}/api/hubspot/companies/companies/{company_id}",
            json=delete_data
        )
        
        if response.status_code == 200:
            print("[SUCCESS] Company deleted successfully")
        else:
            print(f"[ERROR] Delete failed: {response.status_code}")
            print(f"Response: {response.text}")
    
    else:
        print(f"[ERROR] Create company failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    return True

def main():
    """Main function"""
    print("Body-Based JWT Authentication Test")
    print("=" * 50)
    
    success = test_body_authentication()
    
    print("\n" + "=" * 50)
    if success:
        print("[SUCCESS] All body-based authentication tests passed!")
        print("\nNew API Usage:")
        print("GET /api/hubspot/companies/companies")
        print("Body: {\"token\": \"your_jwt_token\"}")
        print("\nPOST /api/hubspot/companies/companies")
        print("Body: {\"token\": \"your_jwt_token\", \"session_id\": 1, \"chat_message_id\": 1, \"properties\": {...}}")
    else:
        print("[ERROR] Some tests failed!")

if __name__ == "__main__":
    main()
