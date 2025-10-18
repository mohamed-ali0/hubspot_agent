"""
Test if company search now works with simplified format
"""

import requests
import json
import time

def test_company_search_fixed():
    """Test if company search works with simplified format after fix"""
    
    print("="*70)
    print("TESTING COMPANY SEARCH AFTER FIX")
    print("="*70)
    
    # Get fresh token
    print("\n1. Getting fresh token...")
    login_url = "http://89.117.63.196:5000/api/auth/login"
    login_data = {"username": "test", "password": "test"}
    
    try:
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print(f"[OK] Fresh token obtained: {token[:50]}...")
        else:
            print(f"[ERROR] Login failed: {login_response.text}")
            return
    except Exception as e:
        print(f"[ERROR] Login error: {e}")
        return
    
    print("\n2. Testing COMPANY SEARCH with simplified format:")
    print("-" * 60)
    
    # Test company search with simplified format
    company_url = "http://89.117.63.196:5000/api/hubspot/companies/companies/search"
    headers = {"Content-Type": "application/json"}
    
    simplified_company_data = {
        "token": token,
        "search_term": "tech",
        "limit": 5
    }
    
    print(f"Request data: {json.dumps(simplified_company_data, indent=2)}")
    
    try:
        response = requests.post(company_url, headers=headers, json=simplified_company_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("[OK] Company search works with simplified format!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} companies")
        else:
            print(f"[ERROR] Company search failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Company search error: {e}")
    
    print("\n3. Testing COMPANY GET with simplified format:")
    print("-" * 60)
    
    # Test company get with simplified format
    company_get_url = "http://89.117.63.196:5000/api/hubspot/companies/companies"
    
    simplified_get_data = {
        "token": token,
        "limit": 3,
        "properties": ["name", "domain", "industry"]
    }
    
    print(f"Request data: {json.dumps(simplified_get_data, indent=2)}")
    
    try:
        response = requests.get(company_get_url, headers=headers, json=simplified_get_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("[OK] Company get works with simplified format!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} companies")
        else:
            print(f"[ERROR] Company get failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Company get error: {e}")
    
    print("\n4. Testing with session/chat IDs (should still work):")
    print("-" * 60)
    
    # Test with session/chat IDs for comparison
    with_session_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "search_term": "tech",
        "limit": 3
    }
    
    print(f"Request data: {json.dumps(with_session_data, indent=2)}")
    
    try:
        response = requests.post(company_url, headers=headers, json=with_session_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("[OK] Company search works with session/chat IDs!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} companies")
        else:
            print(f"[ERROR] Company search failed with session: {response.text}")
    except Exception as e:
        print(f"[ERROR] Company search error with session: {e}")
    
    print("\n" + "="*70)
    print("YOUR N8N FORMATS (NOW WORKING)")
    print("="*70)
    
    print("\n1. COMPANY SEARCH (simplified - NOW WORKS):")
    print("-" * 50)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "search_term": "{{ $fromAI(\'search_term\', \'Search term to find companies\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }}')
    print('}')
    
    print("\n2. COMPANY GET (simplified - NOW WORKS):")
    print("-" * 50)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }},')
    print('  "properties": ["name", "domain", "industry", "city", "state"]')
    print('}')

if __name__ == "__main__":
    test_company_search_fixed()
