"""
Test company search fix with running server
"""

import requests
import json

def test_company_search_fix():
    """Test company search fix"""
    print("Testing Company Search Fix")
    print("="*40)
    
    # Test with local server
    base_url = "http://127.0.0.1:5000"
    
    print("1. Getting fresh token...")
    login_url = f"{base_url}/api/auth/login"
    login_data = {"username": "test", "password": "test"}
    
    try:
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print(f"[OK] Token obtained: {token[:50]}...")
        else:
            print(f"[ERROR] Login failed: {login_response.text}")
            return
    except Exception as e:
        print(f"[ERROR] Login error: {e}")
        return
    
    print("\n2. Testing company search with minimal data...")
    company_search_url = f"{base_url}/api/hubspot/companies/companies/search"
    company_search_data = {
        "token": token,
        "search_term": "tech",
        "limit": 2
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(company_search_url, headers=headers, json=company_search_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("[SUCCESS] Company search works with minimal data!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} companies")
        else:
            print("[ERROR] Company search still requires session/chat IDs")
            
    except Exception as e:
        print(f"[ERROR] Request error: {e}")

if __name__ == "__main__":
    test_company_search_fix()
