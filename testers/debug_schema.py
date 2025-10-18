"""
Debug the actual schema being used
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_schema():
    """Debug the actual schema being used"""
    print("Debugging Company Search Schema")
    print("="*40)
    
    try:
        from app.api.v1.hubspot.companies import company_search_schema
        print(f"Schema type: {type(company_search_schema)}")
        print(f"Schema fields: {company_search_schema.fields}")
        
        # Check if session_id and chat_message_id are optional
        session_field = company_search_schema.fields.get('session_id')
        chat_field = company_search_schema.fields.get('chat_message_id')
        
        print(f"\nsession_id field: {session_field}")
        print(f"chat_message_id field: {chat_field}")
        
        if session_field:
            print(f"session_id missing value: {getattr(session_field, 'missing', 'Not set')}")
        if chat_field:
            print(f"chat_message_id missing value: {getattr(chat_field, 'missing', 'Not set')}")
            
    except Exception as e:
        print(f"Error importing schema: {e}")

if __name__ == "__main__":
    debug_schema()
