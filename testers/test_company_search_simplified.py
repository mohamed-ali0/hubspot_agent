"""
Test company search endpoint with simplified format (no session/chat IDs)
"""

import requests
import json
import time

def test_company_search_simplified():
    """Test company search with simplified format"""
    
    print("="*70)
    print("TESTING COMPANY SEARCH SIMPLIFIED FORMAT")
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
    
    url = "http://89.117.63.196:5000/api/hubspot/companies/companies/search"
    headers = {"Content-Type": "application/json"}
    
    print("\n2. Testing SIMPLIFIED format (no session/chat IDs):")
    print("-" * 60)
    
    # Test the exact format you provided
    simplified_data = {
        "token": token,
        "search_term": "tech",
        "limit": 5
    }
    
    print(f"Request data: {json.dumps(simplified_data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=simplified_data)
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
    
    print("\n3. Testing with properties field:")
    print("-" * 60)
    
    # Test with properties field added
    with_properties_data = {
        "token": token,
        "search_term": "tech",
        "limit": 3,
        "properties": ["name", "domain", "industry", "city", "state"]
    }
    
    print(f"Request data: {json.dumps(with_properties_data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=with_properties_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("[OK] Company search works with properties field!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} companies")
        else:
            print(f"[ERROR] Company search failed with properties: {response.text}")
    except Exception as e:
        print(f"[ERROR] Company search error with properties: {e}")
    
    print("\n4. Testing current format (with session/chat IDs):")
    print("-" * 60)
    
    # Test current format for comparison
    current_data = {
        "token": token,
        "session_id": 1,
        "chat_message_id": 1,
        "search_term": "tech",
        "limit": 3
    }
    
    print(f"Request data: {json.dumps(current_data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=current_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("[OK] Company search works with current format!")
            result = response.json()
            print(f"Found {len(result.get('results', []))} companies")
        else:
            print(f"[ERROR] Company search failed with current format: {response.text}")
    except Exception as e:
        print(f"[ERROR] Company search error with current format: {e}")
    
    print("\n" + "="*70)
    print("WORKING CURL COMMANDS")
    print("="*70)
    
    print("\n1. SIMPLIFIED format (your n8n format):")
    print("-" * 50)
    
    curl_simplified = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/companies/companies/search \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "search_term": "tech",
    "limit": 5
  }}' '''
    
    print(curl_simplified)
    
    print("\n2. With properties field:")
    print("-" * 50)
    
    curl_with_properties = f'''curl -X POST http://89.117.63.196:5000/api/hubspot/companies/companies/search \\
  -H "Content-Type: application/json" \\
  -d '{{
    "token": "{token}",
    "search_term": "tech",
    "limit": 3,
    "properties": ["name", "domain", "industry", "city", "state"]
  }}' '''
    
    print(curl_with_properties)
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("Your n8n format:")
    print('{')
    print('  "token": "{{ $fromAI(\'token\', \'JWT token provided by AI agent or manual input\', \'string\') }}",')
    print('  "search_term": "{{ $fromAI(\'search_term\', \'Search term to find contacts or companies\', \'string\') }}",')
    print('  "limit": {{ $fromAI(\'limit\', \'Maximum number of results to return\', \'number\') }}')
    print('}')
    print("")
    print("This format should work if the server has been restarted with the updated schema!")

if __name__ == "__main__":
    test_company_search_simplified()
