"""
Example script to get JWT token and use it for API calls
"""

import requests
import json

def get_token_and_test_api():
    """Get JWT token and test HubSpot companies API"""
    
    base_url = "http://127.0.0.1:5000"
    
    # Step 1: Login to get token
    print("Step 1: Logging in to get JWT token...")
    login_response = requests.post(f'{base_url}/api/auth/login', 
                                  json={'username': 'test', 'password': 'test'})
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        token = token_data['token']
        print(f"[SUCCESS] Login successful!")
        print(f"Token: {token[:50]}...")
        
        # Step 2: Use token to call HubSpot companies API
        print("\nStep 2: Calling HubSpot companies API...")
        headers = {'Authorization': f'Bearer {token}'}
        
        companies_response = requests.get(
            f'{base_url}/api/hubspot/companies/companies',
            params={'limit': 5, 'properties': 'name,domain,industry'},
            headers=headers
        )
        
        if companies_response.status_code == 200:
            companies = companies_response.json()
            print("[SUCCESS] Companies API successful!")
            print(f"Found {len(companies.get('results', []))} companies")
            
            # Display companies
            for company in companies.get('results', []):
                props = company.get('properties', {})
                print(f"  - {props.get('name', 'N/A')} ({props.get('domain', 'N/A')})")
                
        else:
            print(f"[ERROR] Companies API failed: {companies_response.status_code}")
            print(f"Error: {companies_response.text}")
            
    else:
        print(f"[ERROR] Login failed: {login_response.status_code}")
        print(f"Error: {login_response.text}")

if __name__ == "__main__":
    get_token_and_test_api()
