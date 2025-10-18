"""
Quick Test Script for HubSpot Logging AI Agent
Simple menu-driven testing interface
"""

import requests
import json
import sqlite3
import os

class QuickTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"
        self.token = None
        self.headers = {}
    
    def print_menu(self):
        """Print the main menu"""
        print("\n" + "=" * 50)
        print(" HubSpot Logging AI Agent - Quick Test")
        print("=" * 50)
        print("1. Test Health Check")
        print("2. Test Authentication")
        print("3. Test HubSpot Endpoints")
        print("4. Test All Endpoints")
        print("5. Display Database Contents")
        print("6. Test Direct HubSpot API")
        print("7. Exit")
        print("=" * 50)
    
    def test_health(self):
        """Test health check"""
        print("\n[TEST] Testing Health Check...")
        try:
            response = requests.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Status: {data.get('status')}")
                print(f"[OK] Database: {data.get('database')}")
                print(f"[OK] HubSpot API: {data.get('hubspot_api')}")
            else:
                print(f"[ERROR] Failed: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Error: {e}")
    
    def test_auth(self):
        """Test authentication"""
        print("\n🔐 Testing Authentication...")
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", 
                                   json={"username": "test", "password": "test"})
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.headers = {"Authorization": f"Bearer {self.token}"}
                print(f"✅ Login successful!")
                print(f"✅ Token: {self.token[:50]}...")
            else:
                print(f"❌ Login failed: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def test_hubspot(self):
        """Test HubSpot endpoints"""
        print("\n🎯 Testing HubSpot Endpoints...")
        
        if not self.token:
            print("⚠️ No authentication token. Testing login first...")
            self.test_auth()
        
        if not self.token:
            print("❌ Cannot test HubSpot endpoints without authentication")
            return
        
        endpoints = [
            ("/api/hubspot/test-connection", "HubSpot Connection"),
            ("/api/hubspot/contacts?limit=3", "GET Contacts"),
            ("/api/hubspot/deals?limit=3", "GET Deals"),
            ("/api/hubspot/notes?limit=3", "GET Notes"),
            ("/api/hubspot/tasks?limit=3", "GET Tasks"),
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
                if response.status_code == 200:
                    data = response.json()
                    if 'results' in data:
                        print(f"✅ {name}: Found {len(data['results'])} items")
                    else:
                        print(f"✅ {name}: Success")
                else:
                    print(f"❌ {name}: Failed ({response.status_code})")
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
    
    def test_all_endpoints(self):
        """Test all endpoints"""
        print("\n🚀 Testing All Endpoints...")
        
        # Health check
        self.test_health()
        
        # Authentication
        self.test_auth()
        
        # HubSpot endpoints
        self.test_hubspot()
        
        # Other endpoints
        if self.token:
            other_endpoints = [
                ("/api/users/1", "GET User"),
                ("/api/sessions", "GET Sessions"),
                ("/api/messages", "GET Messages"),
                ("/api/logs", "GET Logs"),
                ("/api/stats/overview", "Analytics Overview"),
            ]
            
            print("\n📊 Testing Other Endpoints...")
            for endpoint, name in other_endpoints:
                try:
                    response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
                    if response.status_code == 200:
                        print(f"✅ {name}: Success")
                    else:
                        print(f"❌ {name}: Failed ({response.status_code})")
                except Exception as e:
                    print(f"❌ {name}: Error - {e}")
    
    def display_database(self):
        """Display database contents"""
        print("\n📊 Database Contents:")
        print("-" * 40)
        
        db_path = "data/database.db"
        if not os.path.exists(db_path):
            print("❌ Database file not found")
            return
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if not tables:
                print("📋 No tables found in database")
                return
            
            for table in tables:
                table_name = table[0]
                print(f"\n📋 Table: {table_name}")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                print(f"   Rows: {count}")
                
                # Get sample data
                if count > 0:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                    rows = cursor.fetchall()
                    print("   Sample data:")
                    for i, row in enumerate(rows, 1):
                        print(f"     {i}: {row}")
                else:
                    print("   No data")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    def test_direct_hubspot(self):
        """Test direct HubSpot API"""
        print("\n🎯 Testing Direct HubSpot API...")
        print("Running direct HubSpot API tests...")
        
        try:
            import subprocess
            result = subprocess.run(["python", "tests/test_hubspot_direct_api.py"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Direct HubSpot API tests completed successfully")
                # Print last few lines of output
                lines = result.stdout.split('\n')
                for line in lines[-10:]:
                    if line.strip():
                        print(f"   {line}")
            else:
                print("❌ Direct HubSpot API tests failed")
                print(f"Error: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Error running direct HubSpot tests: {e}")
    
    def run(self):
        """Run the quick tester"""
        while True:
            self.print_menu()
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                self.test_health()
            elif choice == "2":
                self.test_auth()
            elif choice == "3":
                self.test_hubspot()
            elif choice == "4":
                self.test_all_endpoints()
            elif choice == "5":
                self.display_database()
            elif choice == "6":
                self.test_direct_hubspot()
            elif choice == "7":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

def main():
    """Main function"""
    print("HubSpot Logging AI Agent - Quick Test Interface")
    
    # Check if Flask app is running
    try:
        response = requests.get("http://127.0.0.1:5000/api/health", timeout=2)
        if response.status_code != 200:
            print("❌ Flask app is not running or not accessible")
            print("Please start the Flask app with: python app/main.py")
            return
    except:
        print("❌ Flask app is not running or not accessible")
        print("Please start the Flask app with: python app/main.py")
        return
    
    tester = QuickTester()
    tester.run()

if __name__ == "__main__":
    main()
