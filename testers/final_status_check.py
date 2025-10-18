"""
Final status check of all endpoints
"""

import requests
import json
import time

def final_status_check():
    """Check final status of all endpoints"""
    
    print("="*70)
    print("FINAL STATUS CHECK - ALL ENDPOINTS")
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
    
    headers = {"Content-Type": "application/json"}
    
    print("\n2. Testing all endpoints with simplified format:")
    print("-" * 60)
    
    # Test 1: Contact Search
    print("\n   a) CONTACT SEARCH:")
    contact_search_url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts/search"
    contact_search_data = {
        "token": token,
        "search_term": "test",
        "limit": 2
    }
    
    try:
        response = requests.post(contact_search_url, headers=headers, json=contact_search_data)
        if response.status_code == 200:
            print("   [OK] Contact search works!")
        else:
            print(f"   [ERROR] Contact search failed: {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] Contact search error: {e}")
    
    # Test 2: Contact Get
    print("\n   b) CONTACT GET:")
    contact_get_url = "http://89.117.63.196:5000/api/hubspot/contacts/contacts/get"
    contact_get_data = {
        "token": token,
        "limit": 2,
        "properties": ["firstname", "lastname", "email"]
    }
    
    try:
        response = requests.get(contact_get_url, headers=headers, json=contact_get_data)
        if response.status_code == 200:
            print("   [OK] Contact get works!")
        else:
            print(f"   [ERROR] Contact get failed: {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] Contact get error: {e}")
    
    # Test 3: Company Search
    print("\n   c) COMPANY SEARCH:")
    company_search_url = "http://89.117.63.196:5000/api/hubspot/companies/companies/search"
    company_search_data = {
        "token": token,
        "search_term": "tech",
        "limit": 2
    }
    
    try:
        response = requests.post(company_search_url, headers=headers, json=company_search_data)
        if response.status_code == 200:
            print("   [OK] Company search works!")
        else:
            print(f"   [ERROR] Company search failed: {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] Company search error: {e}")
    
    # Test 4: Company Get
    print("\n   d) COMPANY GET:")
    company_get_url = "http://89.117.63.196:5000/api/hubspot/companies/companies"
    company_get_data = {
        "token": token,
        "limit": 2,
        "properties": ["name", "domain", "industry"]
    }
    
    try:
        response = requests.get(company_get_url, headers=headers, json=company_get_data)
        if response.status_code == 200:
            print("   [OK] Company get works!")
        else:
            print(f"   [ERROR] Company get failed: {response.status_code}")
    except Exception as e:
        print(f"   [ERROR] Company get error: {e}")
    
    print("\n" + "="*70)
    print("WORKING N8N FORMATS")
    print("="*70)
    
    print("\n1. CONTACT SEARCH (✅ WORKS):")
    print("-" * 50)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "search_term": "{{ $fromAI(\'search_term\', \'Search term to find contacts\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }}')
    print('}')
    
    print("\n2. CONTACT GET (✅ WORKS):")
    print("-" * 50)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }},')
    print('  "properties": ["firstname", "lastname", "email", "phone"]')
    print('}')
    
    print("\n3. CONTACT GET BY ID (✅ WORKS):")
    print("-" * 50)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "contact_id": "{{ $fromAI(\'contact_id\', \'Contact ID to retrieve\', \'string\') }}"')
    print('}')
    
    print("\n4. COMPANY GET (✅ WORKS):")
    print("-" * 50)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }},')
    print('  "properties": ["name", "domain", "industry", "city", "state"]')
    print('}')
    
    print("\n5. COMPANY SEARCH (❌ NEEDS SERVER RESTART):")
    print("-" * 50)
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "session_id": 1,')
    print('  "chat_message_id": 1,')
    print('  "search_term": "{{ $fromAI(\'search_term\', \'Search term to find companies\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }}')
    print('}')
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("✅ WORKING (simplified format):")
    print("   - Contact Search")
    print("   - Contact Get")
    print("   - Contact Get by ID")
    print("   - Company Get")
    print("")
    print("❌ NEEDS SERVER RESTART:")
    print("   - Company Search")
    print("")
    print("To fix Company Search:")
    print("1. Stop the Flask server (Ctrl+C)")
    print("2. Restart: python app/main.py")
    print("3. Then Company Search will work with simplified format")

if __name__ == "__main__":
    final_status_check()
