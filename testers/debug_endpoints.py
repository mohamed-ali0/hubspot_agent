#!/usr/bin/env python3
"""
Debug script to test specific endpoints and see detailed error messages
"""

import requests
import json

def test_specific_endpoints():
    """Test specific endpoints to see detailed errors"""
    base_url = "http://127.0.0.1:5000"
    
    # First authenticate
    try:
        response = requests.post(f"{base_url}/api/auth/login", 
                               json={"username": "test", "password": "test"})
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            headers = {"Authorization": f"Bearer {token}"}
            print(f"[OK] Authentication successful")
        else:
            print(f"[ERROR] Authentication failed: {response.status_code}")
            return
    except Exception as e:
        print(f"[ERROR] Authentication error: {e}")
        return
    
    # Test companies endpoint
    print("\n=== TESTING COMPANIES ENDPOINT ===")
    try:
        response = requests.get(f"{base_url}/api/hubspot/companies/companies?limit=3", headers=headers)
        print(f"Companies Status: {response.status_code}")
        if response.status_code != 200:
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Raw Response: {response.text[:500]}")
        else:
            data = response.json()
            print(f"Success: Found {len(data.get('results', []))} companies")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test meetings endpoint
    print("\n=== TESTING MEETINGS ENDPOINT ===")
    try:
        response = requests.get(f"{base_url}/api/hubspot/activities/meetings?limit=3", headers=headers)
        print(f"Meetings Status: {response.status_code}")
        if response.status_code != 200:
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Raw Response: {response.text[:500]}")
        else:
            data = response.json()
            print(f"Success: Found {len(data.get('results', []))} meetings")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test emails endpoint
    print("\n=== TESTING EMAILS ENDPOINT ===")
    try:
        response = requests.get(f"{base_url}/api/hubspot/activities/emails?limit=3", headers=headers)
        print(f"Emails Status: {response.status_code}")
        if response.status_code != 200:
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Raw Response: {response.text[:500]}")
        else:
            data = response.json()
            print(f"Success: Found {len(data.get('results', []))} emails")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test association types endpoint
    print("\n=== TESTING ASSOCIATION TYPES ENDPOINT ===")
    try:
        response = requests.get(f"{base_url}/api/hubspot/associations/types", headers=headers)
        print(f"Association Types Status: {response.status_code}")
        if response.status_code != 200:
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Raw Response: {response.text[:500]}")
        else:
            data = response.json()
            print(f"Success: Found association types")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test legacy contacts endpoint
    print("\n=== TESTING LEGACY CONTACTS ENDPOINT ===")
    try:
        response = requests.get(f"{base_url}/api/hubspot/contacts?limit=3", headers=headers)
        print(f"Legacy Contacts Status: {response.status_code}")
        if response.status_code != 200:
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Raw Response: {response.text[:500]}")
        else:
            data = response.json()
            print(f"Success: Found {len(data.get('results', []))} contacts")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test legacy deals endpoint
    print("\n=== TESTING LEGACY DEALS ENDPOINT ===")
    try:
        response = requests.get(f"{base_url}/api/hubspot/deals?limit=3", headers=headers)
        print(f"Legacy Deals Status: {response.status_code}")
        if response.status_code != 200:
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Raw Response: {response.text[:500]}")
        else:
            data = response.json()
            print(f"Success: Found {len(data.get('results', []))} deals")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    print("HubSpot Endpoints Debug Test")
    print("=" * 50)
    test_specific_endpoints()
