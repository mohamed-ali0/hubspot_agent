"""
Test script to verify the Linux SQLAlchemy fix
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_model_imports():
    """Test that models can be imported without duplicate registration errors"""
    try:
        print("Testing model imports...")
        
        # Test importing models
        from app.models import User, ChatSession, ChatMessage, Log
        print("[OK] Models imported successfully")
        
        # Test creating app
        from app.main import create_app
        app = create_app()
        print("[OK] Flask app created successfully")
        
        # Test database operations
        with app.app_context():
            from app.db.database import db
            # This should not raise the "already has a primary mapper" error
            db.create_all()
            print("[OK] Database tables created successfully")
        
        print("[SUCCESS] All tests passed! Linux fix is working.")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_model_imports()
    sys.exit(0 if success else 1)
