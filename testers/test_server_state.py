"""
Test current server state for company search
"""

import requests
import json

def test_server_state():
    """Test current server state"""
    print("Testing Current Server State")
    print("="*40)
    
    # Get fresh token
    print("1. Getting fresh token...")
    login_url = "http://89.117.63.196:5000/api/auth/login"
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
    
    # Test company search with minimal data
    print("\n2. Testing company search with minimal data...")
    company_search_url = "http://89.117.63.196:5000/api/hubspot/companies/companies/search"
    company_search_data = {
        "token": token,
        "search_term": "test"
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(company_search_url, headers=headers, json=company_search_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("[SUCCESS] Company search works with minimal data!")
        else:
            print("[ERROR] Company search still requires session/chat IDs")
            
    except Exception as e:
        print(f"[ERROR] Request error: {e}")

if __name__ == "__main__":
    test_server_state()
