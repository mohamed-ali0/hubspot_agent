"""
Setup test user with HubSpot token for testing
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.db.database import db
from app.models import User
from app.main import create_app
from app.core.security import SecurityService

def setup_test_user():
    """Setup test user with HubSpot token"""
    app = create_app()
    with app.app_context():
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(username='test').first()
            if existing_user:
                print("[OK] User 'test' already exists")
                print(f"Email: {existing_user.email}")
                print(f"Has HubSpot token: {bool(existing_user.hubspot_pat_token)}")
                
                if not existing_user.hubspot_pat_token:
                    print("[ERROR] User exists but has no HubSpot token!")
                    print("[FIX] You need to add a HubSpot PAT token to this user.")
                    print("[TIP] Run: python check_hubspot_auth.py")
                else:
                    print("[OK] User has HubSpot token configured!")
                
                return existing_user
            
            # Create new user with a placeholder token
            password_hash = SecurityService.hash_password('test')
            
            # Use a placeholder token - user needs to replace with real token
            placeholder_token = "pat-placeholder-token-replace-with-real-token"
            
            user = User(
                name='Test User',
                username='test',
                password_hash=password_hash,
                phone_number='+1234567890',
                hubspot_pat_token=placeholder_token,
                email='test@example.com'
            )
            
            db.session.add(user)
            db.session.commit()
            print("[OK] Test user created!")
            print("[WARNING] IMPORTANT: You need to update the HubSpot token!")
            print("[FIX] Run: python check_hubspot_auth.py")
            print("[NOTE] Replace the placeholder token with your real HubSpot PAT token")
            
            return user
            
        except Exception as e:
            print(f"[ERROR] Error creating user: {e}")
            return None

def main():
    print("[SETUP] Setting up test user...")
    print("=" * 30)
    
    user = setup_test_user()
    
    if user:
        print("\n[NEXT STEPS] Next steps:")
        print("1. Get your HubSpot PAT token from HubSpot Developer Settings")
        print("2. Run: python check_hubspot_auth.py")
        print("3. Enter your real HubSpot PAT token")
        print("4. Run: python test_complete_sales_flow.py")
        
        print("\n[HOW TO GET TOKEN] How to get HubSpot PAT token:")
        print("1. Go to https://app.hubspot.com/")
        print("2. Navigate to Settings > Integrations > Private Apps")
        print("3. Create a new private app or use existing one")
        print("4. Copy the Personal Access Token (starts with 'pat-')")
        print("5. Make sure it has the following scopes:")
        print("   - crm.objects.contacts.read")
        print("   - crm.objects.contacts.write")
        print("   - crm.objects.companies.read")
        print("   - crm.objects.companies.write")
        print("   - crm.objects.deals.read")
        print("   - crm.objects.deals.write")
        print("   - crm.objects.meetings.read")
        print("   - crm.objects.meetings.write")
        print("   - crm.objects.calls.read")
        print("   - crm.objects.calls.write")

if __name__ == "__main__":
    main()
