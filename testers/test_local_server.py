"""
Test with local server to verify our changes work
"""

import requests
import json

def test_local_server():
    """Test with local server"""
    print("Testing with LOCAL SERVER")
    print("="*40)
    
    # Test local server
    local_url = "http://127.0.0.1:5000"
    
    print("1. Testing local server health...")
    try:
        health_response = requests.get(f"{local_url}/api/health")
        print(f"Local server status: {health_response.status_code}")
        if health_response.status_code == 200:
            print("[OK] Local server is running")
        else:
            print("[ERROR] Local server not responding")
            return
    except Exception as e:
        print(f"[ERROR] Local server not accessible: {e}")
        print("Please start local server with: python app/main.py")
        return
    
    # Get fresh token from local server
    print("\n2. Getting fresh token from local server...")
    login_url = f"{local_url}/api/auth/login"
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
    
    # Test company search with minimal data on local server
    print("\n3. Testing company search with minimal data on local server...")
    company_search_url = f"{local_url}/api/hubspot/companies/companies/search"
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
            print("[SUCCESS] Local server company search works with minimal data!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} companies")
        else:
            print("[ERROR] Local server company search still requires session/chat IDs")
            
    except Exception as e:
        print(f"[ERROR] Request error: {e}")

if __name__ == "__main__":
    test_local_server()
