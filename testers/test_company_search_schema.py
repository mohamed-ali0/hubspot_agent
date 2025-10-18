"""
Test company search schema directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.v1.hubspot.companies import company_search_schema

def test_schema():
    """Test the company search schema"""
    print("Testing Company Search Schema")
    print("="*40)
    
    # Test data without session_id and chat_message_id
    test_data = {
        "token": "test_token",
        "search_term": "test",
        "limit": 5
    }
    
    try:
        result = company_search_schema.load(test_data)
        print("[OK] Schema validation PASSED")
        print(f"Result: {result}")
        print(f"session_id: {result.get('session_id')}")
        print(f"chat_message_id: {result.get('chat_message_id')}")
    except Exception as e:
        print(f"[ERROR] Schema validation FAILED: {e}")
    
    # Test data with session_id and chat_message_id
    test_data_with_ids = {
        "token": "test_token",
        "search_term": "test",
        "limit": 5,
        "session_id": 1,
        "chat_message_id": 1
    }
    
    try:
        result = company_search_schema.load(test_data_with_ids)
        print("\n[OK] Schema validation with IDs PASSED")
        print(f"Result: {result}")
        print(f"session_id: {result.get('session_id')}")
        print(f"chat_message_id: {result.get('chat_message_id')}")
    except Exception as e:
        print(f"\n[ERROR] Schema validation with IDs FAILED: {e}")

if __name__ == "__main__":
    test_schema()
