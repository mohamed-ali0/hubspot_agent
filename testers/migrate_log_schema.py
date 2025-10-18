"""
Database migration script to update log schema for leads and deal stages
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
from sqlalchemy import text

def migrate_log_schema():
    """Migrate the log schema to add new fields for leads and deal stages"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("Starting log schema migration...")
            
            # Check if new columns already exist
            inspector = db.inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('logs')]
            
            new_columns = [
                ('lead_status', 'VARCHAR(50)'),
                ('deal_stage', 'VARCHAR(50)'),
                ('lead_source', 'VARCHAR(50)'),
                ('deal_amount', 'VARCHAR(20)'),
                ('stage_reason', 'TEXT')
            ]
            
            # Add new columns if they don't exist
            for column_name, column_type in new_columns:
                if column_name not in existing_columns:
                    try:
                        db.session.execute(text(f"ALTER TABLE logs ADD COLUMN {column_name} {column_type}"))
                        print(f"[OK] Added column: {column_name}")
                    except Exception as e:
                        print(f"[ERROR] Failed to add column {column_name}: {e}")
                else:
                    print(f"[OK] Column {column_name} already exists")
            
            # Update log_type comment to reflect new types
            try:
                # Note: SQLite doesn't support ALTER COLUMN COMMENT, so we'll just document it
                print("[OK] Log schema updated with new log types:")
                print("  - lead: Lead creation and management")
                print("  - lead_qualification: Lead qualification process")
                print("  - deal_stage_update: Deal stage transitions")
            except Exception as e:
                print(f"Note: Could not update column comment: {e}")
            
            # Commit changes
            db.session.commit()
            print("[OK] Database migration completed successfully!")
            
            # Verify the migration
            print("\nVerifying migration...")
            result = db.session.execute(text("PRAGMA table_info(logs)"))
            columns = result.fetchall()
            
            print("Current log table columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Migration failed: {e}")
            db.session.rollback()
            return False

def create_sample_data():
    """Create sample data to test the new schema"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("\nCreating sample data for testing...")
            
            # Check if we have any users
            from app.models import User, ChatSession, ChatMessage, Log
            
            user = User.query.first()
            if not user:
                print("No users found. Please create a user first.")
                return False
            
            # Create a test session and message
            session = ChatSession(
                user_id=user.id,
                started_at=db.func.now(),
                status='active'
            )
            db.session.add(session)
            db.session.flush()
            
            message = ChatMessage(
                session_id=session.id,
                message_text="Test lead creation and deal stage update",
                timestamp=db.func.now()
            )
            db.session.add(message)
            db.session.flush()
            
            # Create sample logs with new fields
            sample_logs = [
                {
                    'user_id': user.id,
                    'session_id': session.id,
                    'chat_message_id': message.id,
                    'log_type': 'lead',
                    'hubspot_id': 'lead_12345',
                    'sync_status': 'synced',
                    'lead_status': 'NEW',
                    'lead_source': 'WhatsApp',
                    'synced_at': db.func.now()
                },
                {
                    'user_id': user.id,
                    'session_id': session.id,
                    'chat_message_id': message.id,
                    'log_type': 'lead_qualification',
                    'hubspot_id': 'lead_12345',
                    'sync_status': 'synced',
                    'lead_status': 'QUALIFIED',
                    'lead_source': 'WhatsApp',
                    'synced_at': db.func.now()
                },
                {
                    'user_id': user.id,
                    'session_id': session.id,
                    'chat_message_id': message.id,
                    'log_type': 'deal_stage_update',
                    'hubspot_id': 'deal_67890',
                    'sync_status': 'synced',
                    'deal_stage': 'qualifiedtobuy',
                    'deal_amount': '50000',
                    'stage_reason': 'Client showed strong interest in the product',
                    'synced_at': db.func.now()
                }
            ]
            
            for log_data in sample_logs:
                log = Log(**log_data)
                db.session.add(log)
            
            db.session.commit()
            print("[OK] Sample data created successfully!")
            
            # Display the created logs
            logs = Log.query.filter(Log.log_type.in_(['lead', 'lead_qualification', 'deal_stage_update'])).all()
            print(f"\nCreated {len(logs)} sample logs:")
            for log in logs:
                print(f"  - {log.log_type}: {log.lead_status or log.deal_stage} (HubSpot ID: {log.hubspot_id})")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to create sample data: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("HubSpot Logging AI Agent - Log Schema Migration")
    print("=" * 50)
    
    # Run migration
    if migrate_log_schema():
        print("\n" + "=" * 50)
        print("Migration completed successfully!")
        
        # Ask if user wants to create sample data
        try:
            create_sample = input("\nCreate sample data for testing? (y/n): ").lower().strip()
            if create_sample in ['y', 'yes']:
                create_sample_data()
        except KeyboardInterrupt:
            print("\nMigration completed without sample data.")
    else:
        print("\nMigration failed. Please check the errors above.")
        sys.exit(1)
