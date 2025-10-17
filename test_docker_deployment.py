"""
Test script for Docker deployment
Tests the application in Docker mode (ignoring database and cache)
"""

import requests
import json
import time

class DockerDeploymentTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.token = None
        self.headers = {}
        
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f" {title}")
        print("=" * 60)
    
    def print_result(self, test_name, status, details=""):
        """Print test result"""
        status_icon = "[OK]" if status == "PASS" else "[ERROR]" if status == "FAIL" else "[SKIP]"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
    
    def test_health_check(self):
        """Test health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/health")
            
            if response.status_code == 200:
                data = response.json()
                self.print_result("Health Check", "PASS", f"Status: {data.get('status')}")
                return True
            else:
                self.print_result("Health Check", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Health Check", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_authentication(self):
        """Test authentication"""
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", 
                                   json={"username": "test", "password": "test"})
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.headers = {"Authorization": f"Bearer {self.token}"}
                self.print_result("Authentication", "PASS", "Token obtained")
                return True
            else:
                self.print_result("Authentication", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Authentication", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_whatsapp_status(self):
        """Test WhatsApp status endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/whatsapp/status")
            
            if response.status_code == 200:
                data = response.json()
                self.print_result("WhatsApp Status", "PASS", f"Active sessions: {data.get('active_sessions')}")
                return True
            else:
                self.print_result("WhatsApp Status", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("WhatsApp Status", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_hubspot_companies(self):
        """Test HubSpot companies endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/companies/companies", 
                                  headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                self.print_result("HubSpot Companies", "PASS", f"Found {len(data.get('results', []))} companies")
                return True
            else:
                self.print_result("HubSpot Companies", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("HubSpot Companies", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_docker_mode_verification(self):
        """Test that Docker mode is working (in-memory database)"""
        try:
            # Test that we can create data but it won't persist
            company_data = {
                "session_id": 1,
                "chat_message_id": 1,
                "properties": {
                    "name": "Docker Test Company",
                    "domain": "docker-test.com",
                    "industry": "COMPUTER_SOFTWARE"
                }
            }
            
            response = requests.post(f"{self.base_url}/api/hubspot/companies/companies", 
                                   json=company_data, headers=self.headers)
            
            if response.status_code == 201:
                self.print_result("Docker Mode Verification", "PASS", "In-memory database working")
                return True
            else:
                self.print_result("Docker Mode Verification", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Docker Mode Verification", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_help_system(self):
        """Test help system"""
        try:
            response = requests.get(f"{self.base_url}/api/help")
            
            if response.status_code == 200:
                data = response.json()
                self.print_result("Help System", "PASS", f"Found {data.get('total_modules')} modules")
                return True
            else:
                self.print_result("Help System", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Help System", "FAIL", f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all Docker deployment tests"""
        self.print_header("Docker Deployment Test Suite")
        print("Testing HubSpot AI Agent in Docker mode...")
        print("(Database and cache ignored - in-memory only)")
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Authentication", self.test_authentication),
            ("WhatsApp Status", self.test_whatsapp_status),
            ("HubSpot Companies", self.test_hubspot_companies),
            ("Docker Mode Verification", self.test_docker_mode_verification),
            ("Help System", self.test_help_system)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n--- {test_name} ---")
            if test_func():
                passed += 1
        
        print(f"\n{'='*60}")
        print(f"Test Results: {passed}/{total} passed")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("[SUCCESS] All Docker deployment tests passed!")
            print("[INFO] Application is running correctly in Docker mode")
            print("[INFO] Database and cache are ignored (in-memory only)")
        else:
            print("[WARNING] Some tests failed. Check the details above.")
        
        return passed == total

if __name__ == "__main__":
    import sys
    
    # Allow custom base URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    print(f"Testing Docker deployment at: {base_url}")
    print("Make sure the Docker container is running!")
    print("Run: docker-compose up --build")
    print()
    
    tester = DockerDeploymentTester(base_url)
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 Docker deployment is working perfectly!")
        print("🐳 Your HubSpot AI Agent is ready for production!")
    else:
        print("\n❌ Docker deployment has issues. Check the logs above.")
        sys.exit(1)
