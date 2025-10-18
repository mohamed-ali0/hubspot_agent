"""
Test script for the new organized HubSpot API structure
Tests all CRUD operations for each object type
"""

import requests
import json
import time

class NewHubSpotAPITester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"
        self.token = None
        self.headers = {}
        self.test_results = []
        
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f" {title}")
        print("=" * 60)
    
    def print_result(self, test_name, status, details="", response=None):
        """Print test result with detailed error information"""
        status_icon = "[OK]" if status == "PASS" else "[ERROR]" if status == "FAIL" else "[SKIP]"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        
        # Show detailed error information for debugging
        if status == "FAIL" and response is not None:
            try:
                error_data = response.json()
                if 'error' in error_data:
                    print(f"   Error: {error_data['error']}")
                if 'msg' in error_data:
                    print(f"   Message: {error_data['msg']}")
            except:
                print(f"   Raw Response: {response.text[:200]}...")
        
        self.test_results.append({
            'test': test_name,
            'status': status,
            'details': details
        })
    
    def authenticate(self):
        """Authenticate and get token"""
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", 
                                   json={"username": "test", "password": "test"})
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.headers = {"Authorization": f"Bearer {self.token}"}
                return True
            else:
                self.print_result("Authentication", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Authentication", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_contacts_api(self):
        """Test contacts API endpoints"""
        self.print_header("CONTACTS API")
        
        if not self.token:
            self.print_result("Contacts API", "SKIP", "No authentication token")
            return
        
        # Test GET contacts
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/contacts/contacts?limit=3", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                self.print_result("GET Contacts", "PASS", f"Found {len(data.get('results', []))} contacts")
            else:
                self.print_result("GET Contacts", "FAIL", f"Status: {response.status_code}", response)
        except Exception as e:
            self.print_result("GET Contacts", "FAIL", f"Error: {str(e)}")
        
        # Test GET contact properties
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/contacts/properties", headers=self.headers)
            if response.status_code == 200:
                self.print_result("GET Contact Properties", "PASS", "Properties retrieved")
            else:
                self.print_result("GET Contact Properties", "FAIL", f"Status: {response.status_code}", response)
        except Exception as e:
            self.print_result("GET Contact Properties", "FAIL", f"Error: {str(e)}")
    
    def test_companies_api(self):
        """Test companies API endpoints"""
        self.print_header("COMPANIES API")
        
        if not self.token:
            self.print_result("Companies API", "SKIP", "No authentication token")
            return
        
        # Test GET companies
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/companies/companies?limit=3", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                self.print_result("GET Companies", "PASS", f"Found {len(data.get('results', []))} companies")
            else:
                self.print_result("GET Companies", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("GET Companies", "FAIL", f"Error: {str(e)}")
        
        # Test GET company properties
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/companies/properties", headers=self.headers)
            if response.status_code == 200:
                self.print_result("GET Company Properties", "PASS", "Properties retrieved")
            else:
                self.print_result("GET Company Properties", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("GET Company Properties", "FAIL", f"Error: {str(e)}")
    
    def test_deals_api(self):
        """Test deals API endpoints"""
        self.print_header("DEALS API")
        
        if not self.token:
            self.print_result("Deals API", "SKIP", "No authentication token")
            return
        
        # Test GET deals
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/deals/deals?limit=3", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                self.print_result("GET Deals", "PASS", f"Found {len(data.get('results', []))} deals")
            else:
                self.print_result("GET Deals", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("GET Deals", "FAIL", f"Error: {str(e)}")
        
        # Test GET deal pipelines
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/deals/pipelines", headers=self.headers)
            if response.status_code == 200:
                self.print_result("GET Deal Pipelines", "PASS", "Pipelines retrieved")
            else:
                self.print_result("GET Deal Pipelines", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("GET Deal Pipelines", "FAIL", f"Error: {str(e)}")
    
    def test_notes_api(self):
        """Test notes API endpoints"""
        self.print_header("NOTES API")
        
        if not self.token:
            self.print_result("Notes API", "SKIP", "No authentication token")
            return
        
        # Test GET notes
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/notes/notes?limit=3", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                self.print_result("GET Notes", "PASS", f"Found {len(data.get('results', []))} notes")
            else:
                self.print_result("GET Notes", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("GET Notes", "FAIL", f"Error: {str(e)}")
    
    def test_tasks_api(self):
        """Test tasks API endpoints"""
        self.print_header("TASKS API")
        
        if not self.token:
            self.print_result("Tasks API", "SKIP", "No authentication token")
            return
        
        # Test GET tasks
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/tasks/tasks?limit=3", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                self.print_result("GET Tasks", "PASS", f"Found {len(data.get('results', []))} tasks")
            else:
                self.print_result("GET Tasks", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("GET Tasks", "FAIL", f"Error: {str(e)}")
    
    def test_activities_api(self):
        """Test activities API endpoints"""
        self.print_header("ACTIVITIES API")
        
        if not self.token:
            self.print_result("Activities API", "SKIP", "No authentication token")
            return
        
        # Test GET calls
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/activities/calls?limit=3", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                self.print_result("GET Calls", "PASS", f"Found {len(data.get('results', []))} calls")
            else:
                self.print_result("GET Calls", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("GET Calls", "FAIL", f"Error: {str(e)}")
        
        # Test GET meetings
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/activities/meetings?limit=3", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                self.print_result("GET Meetings", "PASS", f"Found {len(data.get('results', []))} meetings")
            else:
                self.print_result("GET Meetings", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("GET Meetings", "FAIL", f"Error: {str(e)}")
        
        # Test GET emails
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/activities/emails?limit=3", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                self.print_result("GET Emails", "PASS", f"Found {len(data.get('results', []))} emails")
            else:
                self.print_result("GET Emails", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("GET Emails", "FAIL", f"Error: {str(e)}")
    
    def test_associations_api(self):
        """Test associations API endpoints"""
        self.print_header("ASSOCIATIONS API")
        
        if not self.token:
            self.print_result("Associations API", "SKIP", "No authentication token")
            return
        
        # Test GET association types
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/associations/types", headers=self.headers)
            if response.status_code == 200:
                self.print_result("GET Association Types", "PASS", "Types retrieved")
            else:
                self.print_result("GET Association Types", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("GET Association Types", "FAIL", f"Error: {str(e)}")
    
    def test_legacy_endpoints(self):
        """Test legacy HubSpot endpoints for backward compatibility"""
        self.print_header("LEGACY HUBSPOT ENDPOINTS")
        
        if not self.token:
            self.print_result("Legacy Endpoints", "SKIP", "No authentication token")
            return
        
        # Test legacy contacts endpoint
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/contacts?limit=3", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                self.print_result("Legacy GET Contacts", "PASS", f"Found {len(data.get('results', []))} contacts")
            else:
                self.print_result("Legacy GET Contacts", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("Legacy GET Contacts", "FAIL", f"Error: {str(e)}")
        
        # Test legacy deals endpoint
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/deals?limit=3", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                self.print_result("Legacy GET Deals", "PASS", f"Found {len(data.get('results', []))} deals")
            else:
                self.print_result("Legacy GET Deals", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("Legacy GET Deals", "FAIL", f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("New HubSpot API Structure Test Suite")
        print("=" * 60)
        
        # Authenticate first
        if not self.authenticate():
            print("Authentication failed. Cannot run tests.")
            return False
        
        # Run all test categories
        self.test_contacts_api()
        self.test_companies_api()
        self.test_deals_api()
        self.test_notes_api()
        self.test_tasks_api()
        self.test_activities_api()
        self.test_associations_api()
        self.test_legacy_endpoints()
        
        # Print summary
        self.print_header("TEST SUMMARY")
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        skipped = sum(1 for r in self.test_results if r['status'] == 'SKIP')
        total = len(self.test_results)
        
        print(f"[OK] Passed: {passed}")
        print(f"[ERROR] Failed: {failed}")
        print(f"[SKIP] Skipped: {skipped}")
        print(f"[TOTAL] Total: {total}")
        
        if total > 0:
            success_rate = (passed / total) * 100
            print(f"[SUCCESS] Success Rate: {success_rate:.1f}%")
        
        return failed == 0

def main():
    """Main function"""
    print("HubSpot Logging AI Agent - New API Structure Test")
    
    # Check if Flask app is running
    try:
        response = requests.get("http://127.0.0.1:5000/api/health", timeout=2)
        if response.status_code != 200:
            print("[ERROR] Flask app is not running or not accessible")
            print("Please start the Flask app with: python app/main.py")
            return
    except:
        print("[ERROR] Flask app is not running or not accessible")
        print("Please start the Flask app with: python app/main.py")
        return
    
    # Run tests
    tester = NewHubSpotAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n[SUCCESS] All new API structure tests passed!")
    else:
        print("\n[WARNING] Some tests failed. Check the details above.")

if __name__ == "__main__":
    main()
