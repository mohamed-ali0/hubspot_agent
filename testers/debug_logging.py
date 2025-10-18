"""
Debug script to check logging functionality
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
from app.models import Log, User

def debug_logging():
    """Debug the logging functionality"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("Checking database connection...")
            
            # Check if we can query logs
            logs = Log.query.all()
            print(f"Current logs in database: {len(logs)}")
            
            # Check if we have a user
            user = User.query.filter_by(username='test').first()
            if user:
                print(f"Found user: {user.username} (ID: {user.id})")
            else:
                print("No test user found")
                return
            
            # Try to create a log manually
            print("\nCreating a test log manually...")
            try:
                log = Log(
                    user_id=user.id,
                    session_id=1,
                    chat_message_id=1,
                    log_type='test_log',
                    hubspot_id='test_123',
                    sync_status='synced'
                )
                db.session.add(log)
                db.session.commit()
                print("Test log created successfully!")
                
                # Check logs again
                logs = Log.query.all()
                print(f"Logs after manual creation: {len(logs)}")
                
                for log in logs:
                    print(f"  - {log.log_type}: {log.hubspot_id} ({log.sync_status})")
                
            except Exception as e:
                print(f"Failed to create test log: {e}")
                db.session.rollback()
            
        except Exception as e:
            print(f"Debug failed: {e}")

if __name__ == "__main__":
    debug_logging()
