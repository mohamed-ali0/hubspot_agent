"""
Setup test user with HubSpot token
"""

import os
import sys
from pathlib import Path

# Add parent directory to Python path
parent_dir = Path(__file__).parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from app.main import create_app
from app.db.database import db
from app.models import User
import bcrypt

def setup_test_user():
    """Setup test user with HubSpot token"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("Setting up test user with HubSpot token...")
            
            # Check if test user already exists
            existing_user = User.query.filter_by(username='test').first()
            
            if existing_user:
                print(f"[OK] Test user already exists (ID: {existing_user.id})")
                
                # Update HubSpot token if not set
                if not existing_user.hubspot_pat_token:
                    # Use the token from environment or a default test token
                    hubspot_token = os.getenv('HUBSPOT_ACCESS_TOKEN', 'pat-eu1-df4fa9c7-df17-4174-a492-37f6091b2e21')
                    existing_user.hubspot_pat_token = hubspot_token
                    db.session.commit()
                    print(f"[OK] Updated HubSpot token for user {existing_user.id}")
                else:
                    print(f"[OK] User {existing_user.id} already has HubSpot token")
                
                return existing_user.id
            else:
                # Create new test user
                password_hash = bcrypt.hashpw('test'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                hubspot_token = os.getenv('HUBSPOT_ACCESS_TOKEN', 'pat-eu1-df4fa9c7-df17-4174-a492-37f6091b2e21')
                
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
                
                print(f"[OK] Created test user with ID: {user.id}")
                print(f"[OK] HubSpot token configured")
                return user.id
                
        except Exception as e:
            print(f"[ERROR] Failed to setup test user: {e}")
            db.session.rollback()
            return None

def verify_setup():
    """Verify the setup"""
    app = create_app()
    
    with app.app_context():
        try:
            user = User.query.filter_by(username='test').first()
            if user and user.hubspot_pat_token:
                print(f"[OK] Setup verified - User {user.id} has HubSpot token")
                return True
            else:
                print("[ERROR] Setup verification failed")
                return False
        except Exception as e:
            print(f"[ERROR] Verification failed: {e}")
            return False

if __name__ == "__main__":
    print("HubSpot Logging AI Agent - Test User Setup")
    print("=" * 50)
    
    user_id = setup_test_user()
    if user_id:
        print("\n" + "=" * 50)
        print("Setup completed successfully!")
        verify_setup()
    else:
        print("\n" + "=" * 50)
        print("Setup failed!")
        sys.exit(1)
