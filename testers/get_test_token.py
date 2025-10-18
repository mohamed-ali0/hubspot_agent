"""
Get JWT Token for Test User
Simple script to authenticate and get the JWT token
"""

import requests
import json
import sys

def get_test_token():
    """Get JWT token for test user"""
    
    # Configuration
    base_url = "http://89.117.63.196:5000"
    username = "test"
    password = "test"
    
    print("Getting JWT token for test user...")
    print(f"Username : {username}")
    print(f"Server: {base_url}")
    print("-" * 40)
    
    try:
        # Login request
        login_data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            
            print("[SUCCESS] Login successful!")
            print(f"Token: {token}")
            print(f"Token length: {len(token)} characters")
            print(f"Token preview: {token[:50]}...")
            
            # Save token to file for easy use
            with open('test_token.txt', 'w') as f:
                f.write(token)
            print(f"\n[SAVED] Token saved to: test_token.txt")
            
            # Test the token with a simple API call
            print("\n[TEST] Testing token with health check...")
            test_response = requests.get(
                f"{base_url}/api/health",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if test_response.status_code == 200:
                print("[SUCCESS] Token is valid and working!")
                return token
            else:
                print(f"[ERROR] Token test failed: {test_response.status_code}")
                return None
                
        else:
            print(f"[ERROR] Login failed!")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection failed!")
        print("Make sure the Flask server is running on http://127.0.0.1:5000")
        return None
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        return None

def main():
    """Main function"""
    print("JWT Token Generator for Test User")
    print("=" * 40)
    
    token = get_test_token()
    
    if token:
        print("\n" + "=" * 40)
        print("[SUCCESS] SUCCESS!")
        print("You can now use this token for API calls:")
        print(f"Authorization: Bearer {token}")
        print("\nExample usage:")
        print("curl -H \"Authorization: Bearer YOUR_TOKEN\" \\")
        print("     http://127.0.0.1:5000/api/hubspot/companies/companies")
    else:
        print("\n" + "=" * 40)
        print("[ERROR] FAILED!")
        print("Could not get JWT token. Check the server status.")

if __name__ == "__main__":
    main()
