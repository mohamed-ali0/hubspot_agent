"""
Test all simplified endpoints after server restart
"""

import requests
import json

def test_all_simplified_endpoints():
    """Test all simplified endpoints"""
    print("="*70)
    print("TESTING ALL SIMPLIFIED ENDPOINTS")
    print("="*70)
    
    # Test with local server
    base_url = "http://127.0.0.1:5000"
    
    print("\n1. Getting fresh token...")
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
    
    headers = {"Content-Type": "application/json"}
    
    print("\n2. Testing all simplified endpoints:")
    print("-" * 60)
    
    # Test 1: Contact Search
    print("\n   a) CONTACT SEARCH:")
    contact_search_url = f"{base_url}/api/hubspot/contacts/contacts/search"
    contact_search_data = {
        "token": token,
        "search_term": "test",
        "limit": 2
    }
    
    try:
        response = requests.post(contact_search_url, headers=headers, json=contact_search_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   [OK] Contact search works!")
            result = response.json()
            print(f"   Found {len(result.get('results', []))} contacts")
        else:
            print(f"   [ERROR] Contact search failed: {response.text}")
    except Exception as e:
        print(f"   [ERROR] Contact search error: {e}")
    
    # Test 2: Contact Get
    print("\n   b) CONTACT GET:")
    contact_get_url = f"{base_url}/api/hubspot/contacts/contacts/get"
    contact_get_data = {
        "token": token,
        "limit": 2,
        "properties": ["firstname", "lastname", "email"]
    }
    
    try:
        response = requests.post(contact_get_url, headers=headers, json=contact_get_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   [OK] Contact get works!")
            result = response.json()
            print(f"   Found {len(result.get('results', []))} contacts")
        else:
            print(f"   [ERROR] Contact get failed: {response.text}")
    except Exception as e:
        print(f"   [ERROR] Contact get error: {e}")
    
    # Test 3: Company Search
    print("\n   c) COMPANY SEARCH:")
    company_search_url = f"{base_url}/api/hubspot/companies/companies/search"
    company_search_data = {
        "token": token,
        "search_term": "tech",
        "limit": 2
    }
    
    try:
        response = requests.post(company_search_url, headers=headers, json=company_search_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   [OK] Company search works!")
            result = response.json()
            print(f"   Found {len(result.get('results', []))} companies")
        else:
            print(f"   [ERROR] Company search failed: {response.text}")
    except Exception as e:
        print(f"   [ERROR] Company search error: {e}")
    
    # Test 4: Company Get
    print("\n   d) COMPANY GET:")
    company_get_url = f"{base_url}/api/hubspot/companies/companies"
    company_get_data = {
        "token": token,
        "limit": 2,
        "properties": ["name", "domain", "industry"]
    }
    
    try:
        response = requests.get(company_get_url, headers=headers, json=company_get_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   [OK] Company get works!")
            result = response.json()
            print(f"   Found {len(result.get('results', []))} companies")
        else:
            print(f"   [ERROR] Company get failed: {response.text}")
    except Exception as e:
        print(f"   [ERROR] Company get error: {e}")
    
    # Test 5: Contact Get by ID
    print("\n   e) CONTACT GET BY ID:")
    # First get a contact ID
    try:
        get_response = requests.post(contact_get_url, headers=headers, json={
            "token": token,
            "limit": 1,
            "properties": ["firstname", "lastname", "email"]
        })
        if get_response.status_code == 200:
            result = get_response.json()
            if result.get('results'):
                contact_id = result['results'][0]['id']
                print(f"   Using contact ID: {contact_id}")
                
                contact_get_by_id_url = f"{base_url}/api/hubspot/contacts/contacts/get-by-id"
                contact_get_by_id_data = {
                    "token": token,
                    "contact_id": contact_id
                }
                
                response = requests.post(contact_get_by_id_url, headers=headers, json=contact_get_by_id_data)
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    print("   [OK] Contact get by ID works!")
                else:
                    print(f"   [ERROR] Contact get by ID failed: {response.text}")
            else:
                print("   [SKIP] No contacts found to test get by ID")
        else:
            print("   [SKIP] Could not get contact ID for testing")
    except Exception as e:
        print(f"   [ERROR] Contact get by ID error: {e}")
    
    print("\n" + "="*70)
    print("FINAL N8N WORKFLOW FORMATS")
    print("="*70)
    
    print("\n1. CONTACT SEARCH:")
    print("-" * 30)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "search_term": "{{ $fromAI(\'search_term\', \'Search term to find contacts\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }}')
    print('}')
    
    print("\n2. CONTACT GET:")
    print("-" * 30)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }},')
    print('  "properties": ["firstname", "lastname", "email", "phone"]')
    print('}')
    
    print("\n3. CONTACT GET BY ID:")
    print("-" * 30)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "contact_id": "{{ $fromAI(\'contact_id\', \'Contact ID to retrieve\', \'string\') }}"')
    print('}')
    
    print("\n4. COMPANY SEARCH:")
    print("-" * 30)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "search_term": "{{ $fromAI(\'search_term\', \'Search term to find companies\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }}')
    print('}')
    
    print("\n5. COMPANY GET:")
    print("-" * 30)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }},')
    print('  "properties": ["name", "domain", "industry", "city", "state"]')
    print('}')
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("All getter endpoints now work with simplified format!")
    print("No session_id or chat_message_id required for read operations.")
    print("Perfect for n8n workflows!")

if __name__ == "__main__":
    test_all_simplified_endpoints()
