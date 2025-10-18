"""
Test HubSpot token validity
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

import requests
from app.db.database import db
from app.models import User
from app.main import create_app

def test_hubspot_token():
    """Test if the HubSpot token is valid"""
    app = create_app()
    with app.app_context():
        try:
            # Get user and token
            user = User.query.filter_by(username='test').first()
            if not user or not user.hubspot_pat_token:
                print("[ERROR] No user or token found!")
                return False
            
            token = user.hubspot_pat_token
            print(f"[INFO] Testing token: {token[:10]}...")
            
            # Test token with a simple HubSpot API call
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # Try to get contacts (simple test)
            response = requests.get(
                'https://api.hubapi.com/crm/v3/objects/contacts?limit=1',
                headers=headers
            )
            
            print(f"[INFO] Response status: {response.status_code}")
            
            if response.status_code == 200:
                print("[OK] HubSpot token is valid!")
                data = response.json()
                print(f"[INFO] Found {len(data.get('results', []))} contacts")
                return True
            elif response.status_code == 401:
                print("[ERROR] HubSpot token is invalid or expired!")
                print("[FIX] You need to get a new token from HubSpot")
                return False
            elif response.status_code == 403:
                print("[ERROR] HubSpot token lacks required permissions!")
                print("[FIX] Check your token has the right scopes")
                return False
            else:
                print(f"[ERROR] Unexpected response: {response.status_code}")
                print(f"[INFO] Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error testing token: {e}")
            return False

def main():
    print("[TEST] HubSpot Token Validator")
    print("=" * 30)
    
    success = test_hubspot_token()
    
    if success:
        print("\n[SUCCESS] Your HubSpot token is working!")
        print("[NEXT] You can now run: python test_complete_sales_flow.py")
    else:
        print("\n[FAILED] HubSpot token is not working!")
        print("[FIX] Steps to fix:")
        print("1. Go to https://app.hubspot.com/")
        print("2. Navigate to Settings > Integrations > Private Apps")
        print("3. Create a new private app or use existing one")
        print("4. Copy the Personal Access Token (starts with 'pat-')")
        print("5. Run: python check_hubspot_auth.py")
        print("6. Enter your new token")

if __name__ == "__main__":
    main()
