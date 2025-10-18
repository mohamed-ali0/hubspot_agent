"""
Simple test for body-based authentication
"""

import requests
import json
import time

def test_body_auth():
    """Test body-based authentication"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("Testing Body-Based Authentication")
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
    
    # Step 2: Test GET companies with body token
    print("\nStep 2: Testing GET companies with body token...")
    try:
        response = requests.get(
            f"{base_url}/api/hubspot/companies/companies",
            json={"token": token},  # Token in body
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
            return False
    except Exception as e:
        print(f"[ERROR] Request error: {str(e)}")
        return False
    
    # Step 3: Test GET company properties with body token
    print("\nStep 3: Testing GET company properties with body token...")
    try:
        response = requests.get(
            f"{base_url}/api/hubspot/companies/properties",
            json={"token": token}  # Token in body
        )
        
        if response.status_code == 200:
            data = response.json()
            properties = data.get('results', [])
            print(f"[SUCCESS] Found {len(properties)} company properties")
            if properties:
                print("  Sample properties:")
                for prop in properties[:3]:  # Show first 3
                    name = prop.get('name', 'N/A')
                    print(f"    - {name}")
        else:
            print(f"[ERROR] Properties request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Properties request error: {str(e)}")
        return False
    
    print("\n" + "=" * 40)
    print("[SUCCESS] Body-based authentication is working!")
    print("All endpoints now accept tokens in request body.")
    return True

if __name__ == "__main__":
    test_body_auth()
