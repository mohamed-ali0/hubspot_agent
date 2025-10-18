"""
Test the provided JWT token
"""

import requests
import json

def test_provided_token():
    """Test the provided JWT token"""
    
    # The token you provided
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDcxNzc5MSwianRpIjoiYjczNjhjNmEtZTZlYS00NTAyLWJlZTEtODU5MTcyOWUyYjZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzE3NzkxLCJjc3JmIjoiNGY3NjJiMmEtNjU2Mi00YjBmLTg2NTItYmY5ZmZmZjFmM2U0IiwiZXhwIjoxNzYwNzIxMzkxfQ.CgHi0_EI7Xj2asX7BvLQ2Ubv-yKMVTijg-7hN4mH9K0"
    
    base_url = "http://127.0.0.1:5000"
    headers = {"Authorization": f"Bearer {token}"}
    
    print("Testing Provided JWT Token")
    print("=" * 40)
    print(f"Token: {token[:50]}...")
    print(f"Token length: {len(token)} characters")
    print("-" * 40)
    
    # Test 1: Health Check
    print("Test 1: Health Check...")
    try:
        response = requests.get(f"{base_url}/api/health", headers=headers)
        if response.status_code == 200:
            print("[SUCCESS] Health check passed!")
            health_data = response.json()
            print(f"  Status: {health_data.get('status')}")
            print(f"  Database: {health_data.get('database')}")
            print(f"  HubSpot: {health_data.get('hubspot_api')}")
        else:
            print(f"[ERROR] Health check failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Health check error: {str(e)}")
        return False
    
    # Test 2: HubSpot Companies API
    print("\nTest 2: HubSpot Companies API...")
    try:
        response = requests.get(
            f"{base_url}/api/hubspot/companies/companies",
            params={"limit": 3, "properties": "name,domain,industry"},
            headers=headers
        )
        if response.status_code == 200:
            print("[SUCCESS] Companies API working!")
            data = response.json()
            companies = data.get('results', [])
            print(f"  Found {len(companies)} companies:")
            for company in companies:
                props = company.get('properties', {})
                name = props.get('name', 'N/A')
                domain = props.get('domain', 'N/A')
                print(f"    - {name} ({domain})")
        else:
            print(f"[ERROR] Companies API failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Companies API error: {str(e)}")
        return False
    
    # Test 3: HubSpot Contacts API
    print("\nTest 3: HubSpot Contacts API...")
    try:
        response = requests.get(
            f"{base_url}/api/hubspot/contacts/contacts",
            params={"limit": 2, "properties": "firstname,lastname,email"},
            headers=headers
        )
        if response.status_code == 200:
            print("[SUCCESS] Contacts API working!")
            data = response.json()
            contacts = data.get('results', [])
            print(f"  Found {len(contacts)} contacts:")
            for contact in contacts:
                props = contact.get('properties', {})
                firstname = props.get('firstname', 'N/A')
                lastname = props.get('lastname', 'N/A')
                email = props.get('email', 'N/A')
                print(f"    - {firstname} {lastname} ({email})")
        else:
            print(f"[ERROR] Contacts API failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Contacts API error: {str(e)}")
        return False
    
    # Test 4: Logs API
    print("\nTest 4: Logs API...")
    try:
        response = requests.get(f"{base_url}/api/logs", headers=headers)
        if response.status_code == 200:
            print("[SUCCESS] Logs API working!")
            data = response.json()
            logs = data.get('logs', [])
            print(f"  Found {len(logs)} logs")
            if logs:
                print("  Recent log types:")
                log_types = {}
                for log in logs[:10]:  # Show first 10 logs
                    log_type = log.get('log_type', 'unknown')
                    log_types[log_type] = log_types.get(log_type, 0) + 1
                for log_type, count in log_types.items():
                    print(f"    - {log_type}: {count}")
        else:
            print(f"[ERROR] Logs API failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Logs API error: {str(e)}")
        return False
    
    return True

def main():
    """Main function"""
    print("JWT Token Validation Test")
    print("=" * 40)
    
    success = test_provided_token()
    
    print("\n" + "=" * 40)
    if success:
        print("[SUCCESS] All tests passed! Token is valid and working.")
        print("You can use this token for API calls:")
        print("Authorization: Bearer YOUR_TOKEN")
    else:
        print("[ERROR] Some tests failed. Token may be invalid or expired.")
        print("Try getting a new token with: python get_test_token.py")

if __name__ == "__main__":
    main()
