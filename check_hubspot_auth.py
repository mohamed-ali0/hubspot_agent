"""
Check and fix HubSpot authentication issues
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.db.database import db
from app.models import User
from app.main import create_app

def check_user_hubspot_token():
    """Check if test user has HubSpot token"""
    app = create_app()
    with app.app_context():
        try:
            user = User.query.filter_by(username='test').first()
            if user:
                print(f"[OK] User found: {user.username}")
                print(f"Email: {user.email}")
                print(f"Phone: {user.phone_number}")
                print(f"Has HubSpot token: {bool(user.hubspot_pat_token)}")
                if user.hubspot_pat_token:
                    print(f"Token length: {len(user.hubspot_pat_token)}")
                    print(f"Token starts with: {user.hubspot_pat_token[:10]}...")
                else:
                    print("[ERROR] No HubSpot token configured!")
                return user
            else:
                print("[ERROR] User 'test' not found!")
                return None
        except Exception as e:
            print(f"[ERROR] Error checking user: {e}")
            return None

def update_user_hubspot_token():
    """Update test user with HubSpot token"""
    app = create_app()
    with app.app_context():
        try:
            user = User.query.filter_by(username='test').first()
            if user:
                # You need to replace this with your actual HubSpot PAT token
                hubspot_token = input("Enter your HubSpot PAT token (starts with 'pat-'): ").strip()
                
                if hubspot_token and hubspot_token.startswith('pat-'):
                    user.hubspot_pat_token = hubspot_token
                    db.session.commit()
                    print("[OK] HubSpot token updated successfully!")
                    return True
                else:
                    print("[ERROR] Invalid token format. Token should start with 'pat-'")
                    return False
            else:
                print("[ERROR] User 'test' not found!")
                return False
        except Exception as e:
            print(f"[ERROR] Error updating token: {e}")
            return False

def create_test_user_with_token():
    """Create test user with HubSpot token"""
    app = create_app()
    with app.app_context():
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(username='test').first()
            if existing_user:
                print("✅ User 'test' already exists")
                return existing_user
            
            # Create new user
            from app.core.security import SecurityService
            password_hash = SecurityService.hash_password('test')
            
            hubspot_token = input("Enter your HubSpot PAT token (starts with 'pat-'): ").strip()
            
            if not hubspot_token or not hubspot_token.startswith('pat-'):
                print("[ERROR] Invalid token format. Token should start with 'pat-'")
                return None
            
            user = User(
                name='Test User',
                username='test',
                password_hash=password_hash,
                phone_number='+1234567890',
                hubspot_pat_token=hubspot_token,
                email='test@example.com'
            )
            
            db.session.add(user)
            db.session.commit()
            print("[OK] Test user created with HubSpot token!")
            return user
            
        except Exception as e:
            print(f"[ERROR] Error creating user: {e}")
            return None

def main():
    print("[CHECK] HubSpot Authentication Checker")
    print("=" * 40)
    
    # Check current user
    user = check_user_hubspot_token()
    
    if user and user.hubspot_pat_token:
        print("\n[OK] User has HubSpot token configured!")
        print("[INFO] If tests are still failing, the token might be invalid or expired.")
        print("[TIP] Try updating the token with a fresh one from HubSpot.")
    else:
        print("\n[ERROR] User needs HubSpot token!")
        print("[OPTIONS] Options:")
        print("1. Update existing user with token")
        print("2. Create new user with token")
        
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == '1':
            update_user_hubspot_token()
        elif choice == '2':
            create_test_user_with_token()
        else:
            print("[ERROR] Invalid choice")

if __name__ == "__main__":
    main()
