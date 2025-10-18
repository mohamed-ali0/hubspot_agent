"""
Test script for the Help API system
"""

import requests
import json

class HelpSystemTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"
        self.token = None
        self.headers = {}
        
    def authenticate(self):
        """Authenticate and get token"""
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", 
                                   json={"username": "test", "password": "test"})
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.headers = {"Authorization": f"Bearer {self.token}"}
                print("[OK] Authentication successful")
                return True
            else:
                print(f"[ERROR] Authentication failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] Authentication error: {e}")
            return False
    
    def test_help_overview(self):
        """Test help overview endpoint"""
        print("\n=== TESTING HELP OVERVIEW ===")
        try:
            response = requests.get(f"{self.base_url}/api/help")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Title: {data.get('title')}")
                print(f"Modules: {list(data.get('modules', {}).keys())}")
                print(f"Total modules: {len(data.get('modules', {}))}")
                return True
            else:
                print(f"Error: {response.text}")
                return False
        except Exception as e:
            print(f"Exception: {e}")
            return False
    
    def test_help_modules(self):
        """Test help modules endpoint"""
        print("\n=== TESTING HELP MODULES ===")
        try:
            response = requests.get(f"{self.base_url}/api/help/modules")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Modules: {[m['name'] for m in data.get('modules', [])]}")
                print(f"Total modules: {data.get('count')}")
                return True
            else:
                print(f"Error: {response.text}")
                return False
        except Exception as e:
            print(f"Exception: {e}")
            return False
    
    def test_help_module(self, module):
        """Test help for specific module"""
        print(f"\n=== TESTING HELP FOR MODULE: {module} ===")
        try:
            response = requests.get(f"{self.base_url}/api/help/{module}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Module: {data.get('module')}")
                print(f"Endpoints: {list(data.get('endpoints', {}).keys())}")
                print(f"Count: {data.get('count')}")
                return True
            else:
                print(f"Error: {response.text}")
                return False
        except Exception as e:
            print(f"Exception: {e}")
            return False
    
    def test_help_endpoint(self, module, endpoint):
        """Test help for specific endpoint"""
        print(f"\n=== TESTING HELP FOR ENDPOINT: {module}/{endpoint} ===")
        try:
            response = requests.get(f"{self.base_url}/api/help/{module}/{endpoint}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                doc = data.get('documentation', {})
                print(f"Title: {doc.get('title')}")
                print(f"Method: {doc.get('method')}")
                print(f"Endpoint: {doc.get('endpoint')}")
                print(f"Tips: {len(doc.get('tips', []))} tips available")
                return True
            else:
                print(f"Error: {response.text}")
                return False
        except Exception as e:
            print(f"Exception: {e}")
            return False
    
    def test_help_search(self, query):
        """Test help search functionality"""
        print(f"\n=== TESTING HELP SEARCH: '{query}' ===")
        try:
            response = requests.get(f"{self.base_url}/api/help/search?q={query}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Query: {data.get('query')}")
                print(f"Results: {data.get('count')} found")
                for result in data.get('results', [])[:3]:  # Show first 3 results
                    print(f"  - {result.get('module')}/{result.get('endpoint')}: {result.get('title')}")
                return True
            else:
                print(f"Error: {response.text}")
                return False
        except Exception as e:
            print(f"Exception: {e}")
            return False
    
    def run_all_tests(self):
        """Run all help system tests"""
        print("HubSpot Logging AI Agent - Help System Test")
        print("=" * 60)
        
        # Test help overview
        self.test_help_overview()
        
        # Test help modules
        self.test_help_modules()
        
        # Test specific modules
        modules_to_test = ['contacts', 'auth', 'health']
        for module in modules_to_test:
            self.test_help_module(module)
        
        # Test specific endpoints
        endpoints_to_test = [
            ('contacts', 'get_contacts'),
            ('contacts', 'create_contact'),
            ('auth', 'login'),
            ('health', 'health_check')
        ]
        
        for module, endpoint in endpoints_to_test:
            self.test_help_endpoint(module, endpoint)
        
        # Test search functionality
        search_queries = ['contact', 'login', 'health', 'create']
        for query in search_queries:
            self.test_help_search(query)
        
        print("\n" + "=" * 60)
        print("Help System Test Complete!")

if __name__ == "__main__":
    tester = HelpSystemTester()
    tester.run_all_tests()
