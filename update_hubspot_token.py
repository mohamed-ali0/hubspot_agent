"""
Update HubSpot token with the new PAT token
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.db.database import db
from app.models import User
from app.main import create_app

def update_hubspot_token():
    """Update test user with new HubSpot token"""
    app = create_app()
    with app.app_context():
        try:
            # Get the new token
            new_token = "pat-eu1-c5e5f688-74c2-43da-b574-c85b0fb787a3"
            
            # Find the test user
            user = User.query.filter_by(username='test').first()
            if not user:
                print("[ERROR] User 'test' not found!")
                return False
            
            # Update the token
            user.hubspot_pat_token = new_token
            db.session.commit()
            
            print("[OK] HubSpot token updated successfully!")
            print(f"[INFO] New token: {new_token[:10]}...")
            print(f"[INFO] Token length: {len(new_token)}")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Error updating token: {e}")
            return False

def main():
    print("[UPDATE] Updating HubSpot Token")
    print("=" * 40)
    
    success = update_hubspot_token()
    
    if success:
        print("\n[SUCCESS] Token updated successfully!")
        print("[NEXT] Run: python test_hubspot_token.py to verify")
        print("[NEXT] Run: python test_complete_sales_flow.py to test full flow")
    else:
        print("\n[ERROR] Failed to update token!")

if __name__ == "__main__":
    main()
