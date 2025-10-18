"""
Use saved JWT token for API calls
"""

import requests
import os

def load_token():
    """Load token from file"""
    try:
        with open('test_token.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("[ERROR] Token file not found. Run get_test_token.py first.")
        return None

def test_companies_api():
    """Test the companies API with the token"""
    token = load_token()
    if not token:
        return
    
    base_url = "http://127.0.0.1:5000"
    headers = {"Authorization": f"Bearer {token}"}
    
    print("Testing HubSpot Companies API...")
    print(f"Token: {token[:50]}...")
    print("-" * 40)
    
    try:
        # Test companies API
        response = requests.get(
            f"{base_url}/api/hubspot/companies/companies",
            params={"limit": 3, "properties": "name,domain,industry"},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            companies = data.get('results', [])
            print(f"[SUCCESS] Found {len(companies)} companies:")
            
            for company in companies:
                props = company.get('properties', {})
                name = props.get('name', 'N/A')
                domain = props.get('domain', 'N/A')
                industry = props.get('industry', 'N/A')
                print(f"  - {name} ({domain}) - {industry}")
        else:
            print(f"[ERROR] API call failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"[ERROR] Request failed: {str(e)}")

def main():
    """Main function"""
    print("Using Saved JWT Token")
    print("=" * 30)
    test_companies_api()

if __name__ == "__main__":
    main()
