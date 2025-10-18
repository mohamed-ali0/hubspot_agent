"""
Test if the server restart worked and simplified format now works
"""

import requests
import json
import time

def test_after_restart():
    """Test if simplified format works after server restart"""
    
    print("="*70)
    print("TESTING AFTER SERVER RESTART")
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
    
    print("\n3. Testing CONTACT SEARCH with simplified format:")
    print("-" * 60)
    
    # Test contact search with simplified format
    contact_url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts/search"
    
    simplified_contact_data = {
        "token": token,
        "search_term": "test",
        "limit": 3
    }
    
    print(f"Request data: {json.dumps(simplified_contact_data, indent=2)}")
    
    try:
        response = requests.post(contact_url, headers=headers, json=simplified_contact_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("[OK] Contact search works with simplified format!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} contacts")
        else:
            print(f"[ERROR] Contact search failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Contact search error: {e}")
    
    print("\n4. Testing CONTACT GET with simplified format:")
    print("-" * 60)
    
    # Test contact get with simplified format
    contact_get_url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts/get"
    
    simplified_get_data = {
        "token": token,
        "limit": 3,
        "properties": ["firstname", "lastname", "email"]
    }
    
    print(f"Request data: {json.dumps(simplified_get_data, indent=2)}")
    
    try:
        response = requests.post(contact_get_url, headers=headers, json=simplified_get_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("[OK] Contact get works with simplified format!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} contacts")
        else:
            print(f"[ERROR] Contact get failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Contact get error: {e}")
    
    print("\n5. Testing CONTACT GET BY ID with simplified format:")
    print("-" * 60)
    
    # Test contact get by id with simplified format
    contact_get_by_id_url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts/get-by-id"
    
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
                print(f"Using contact ID: {contact_id}")
                
                simplified_get_by_id_data = {
                    "token": token,
                    "contact_id": contact_id
                }
                
                print(f"Request data: {json.dumps(simplified_get_by_id_data, indent=2)}")
                
                response = requests.post(contact_get_by_id_url, headers=headers, json=simplified_get_by_id_data)
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text}")
                
                if response.status_code == 200:
                    print("[OK] Contact get by ID works with simplified format!")
                else:
                    print(f"[ERROR] Contact get by ID failed: {response.text}")
            else:
                print("[SKIP] No contacts found to test get by ID")
        else:
            print("[SKIP] Could not get contact ID for testing")
    except Exception as e:
        print(f"[ERROR] Contact get by ID error: {e}")
    
    print("\n" + "="*70)
    print("YOUR N8N FORMATS")
    print("="*70)
    
    print("\n1. COMPANY SEARCH (simplified):")
    print("-" * 50)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "search_term": "{{ $fromAI(\'search_term\', \'Search term to find companies\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }}')
    print('}')
    
    print("\n2. CONTACT SEARCH (simplified):")
    print("-" * 50)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "search_term": "{{ $fromAI(\'search_term\', \'Search term to find contacts\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }}')
    print('}')
    
    print("\n3. CONTACT GET (simplified):")
    print("-" * 50)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }},')
    print('  "properties": ["firstname", "lastname", "email", "phone"]')
    print('}')
    
    print("\n4. CONTACT GET BY ID (simplified):")
    print("-" * 50)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "contact_id": "{{ $fromAI(\'contact_id\', \'Contact ID to retrieve\', \'string\') }}"')
    print('}')

if __name__ == "__main__":
    test_after_restart()
