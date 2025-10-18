"""
Simple Test Script for HubSpot Logging AI Agent
No emojis, Windows-compatible
"""

import requests
import json
import sqlite3
import os

def test_health():
    """Test health check"""
    print("\n[TEST] Testing Health Check...")
    try:
        response = requests.get("http://127.0.0.1:5000/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Status: {data.get('status')}")
            print(f"[OK] Database: {data.get('database')}")
            print(f"[OK] HubSpot API: {data.get('hubspot_api')}")
            return True
        else:
            print(f"[ERROR] Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

def test_auth():
    """Test authentication"""
    print("\n[TEST] Testing Authentication...")
    try:
        response = requests.post("http://127.0.0.1:5000/api/auth/login", 
                               json={"username": "test", "password": "test"})
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print(f"[OK] Login successful!")
            print(f"[OK] Token: {token[:50]}...")
            return token
        else:
            print(f"[ERROR] Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return None

def test_hubspot_endpoints(token):
    """Test HubSpot endpoints"""
    print("\n[TEST] Testing HubSpot Endpoints...")
    
    if not token:
        print("[ERROR] No authentication token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    endpoints = [
        ("/api/hubspot/test-connection", "HubSpot Connection"),
        ("/api/hubspot/contacts?limit=3", "GET Contacts"),
        ("/api/hubspot/deals?limit=3", "GET Deals"),
        ("/api/hubspot/notes?limit=3", "GET Notes"),
        ("/api/hubspot/tasks?limit=3", "GET Tasks"),
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"http://127.0.0.1:5000{endpoint}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if 'results' in data:
                    print(f"[OK] {name}: Found {len(data['results'])} items")
                else:
                    print(f"[OK] {name}: Success")
            else:
                print(f"[ERROR] {name}: Failed ({response.status_code})")
        except Exception as e:
            print(f"[ERROR] {name}: Error - {e}")

def test_other_endpoints(token):
    """Test other endpoints"""
    print("\n[TEST] Testing Other Endpoints...")
    
    if not token:
        print("[ERROR] No authentication token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    endpoints = [
        ("/api/users/1", "GET User"),
        ("/api/sessions", "GET Sessions"),
        ("/api/messages", "GET Messages"),
        ("/api/logs", "GET Logs"),
        ("/api/stats/overview", "Analytics Overview"),
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"http://127.0.0.1:5000{endpoint}", headers=headers)
            if response.status_code == 200:
                print(f"[OK] {name}: Success")
            else:
                print(f"[ERROR] {name}: Failed ({response.status_code})")
        except Exception as e:
            print(f"[ERROR] {name}: Error - {e}")

def display_database():
    """Display database contents"""
    print("\n[DATABASE] Database Contents:")
    print("-" * 40)
    
    db_path = "data/database.db"
    if not os.path.exists(db_path):
        print("[ERROR] Database file not found")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("[INFO] No tables found in database")
            return
        
        for table in tables:
            table_name = table[0]
            print(f"\n[TABLE] {table_name}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"  Rows: {count}")
            
            # Get sample data
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                rows = cursor.fetchall()
                print("  Sample data:")
                for i, row in enumerate(rows, 1):
                    print(f"    {i}: {row}")
            else:
                print("  No data")
        
        conn.close()
        
    except Exception as e:
        print(f"[ERROR] Database error: {e}")

def main():
    """Main function"""
    print("HubSpot Logging AI Agent - Simple Test")
    print("=" * 50)
    
    # Check if Flask app is running
    if not test_health():
        print("\n[ERROR] Flask app is not running or not accessible")
        print("Please start the Flask app with: python app/main.py")
        return
    
    # Test authentication
    token = test_auth()
    
    # Test HubSpot endpoints
    test_hubspot_endpoints(token)
    
    # Test other endpoints
    test_other_endpoints(token)
    
    # Display database
    display_database()
    
    print("\n[COMPLETE] Test completed!")

if __name__ == "__main__":
    main()
