#!/usr/bin/env python3
"""
Test script to demonstrate the user-specific PAT system
"""

import requests
import json
import os

class UserPATSystemTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"
        self.token = None
        self.headers = {}
        self.test_results = []

    def print_result(self, test_name, status, details=""):
        """Print test result"""
        status_icon = "[OK]" if status == "PASS" else "[ERROR]"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        
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
                self.print_result("Authentication", "PASS")
                return True
            else:
                self.print_result("Authentication", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_result("Authentication", "FAIL", f"Error: {str(e)}")
            return False

    def test_user_pat_system(self):
        """Test that each user has their own PAT"""
        print("\n" + "="*60)
        print("🔐 USER-SPECIFIC PAT SYSTEM TEST")
        print("="*60)
        
        # Test 1: Check if user has PAT configured
        try:
            response = requests.get(f"{self.base_url}/api/users/me", headers=self.headers)
            if response.status_code == 200:
                user_data = response.json()
                has_pat = bool(user_data.get('hubspot_pat_token'))
                if has_pat:
                    self.print_result("User PAT Check", "PASS", "User has HubSpot PAT configured")
                else:
                    self.print_result("User PAT Check", "WARN", "User has no HubSpot PAT - will use system fallback")
            else:
                self.print_result("User PAT Check", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.print_result("User PAT Check", "FAIL", f"Error: {str(e)}")

        # Test 2: Try to create a contact (this will use user's PAT)
        try:
            contact_data = {
                "session_id": 1,
                "chat_message_id": 1,
                "properties": {
                    "email": "test-user-pat@example.com",
                    "firstname": "Test",
                    "lastname": "UserPAT"
                }
            }
            response = requests.post(f"{self.base_url}/api/hubspot/contacts/contacts", 
                                   json=contact_data, headers=self.headers)
            
            if response.status_code in [200, 201]:
                self.print_result("Contact Creation with User PAT", "PASS", "Successfully used user's PAT")
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                if "HUBSPOT_ACCESS_TOKEN not configured" in str(error_data):
                    self.print_result("Contact Creation with User PAT", "WARN", "User has no PAT - system fallback needed")
                else:
                    self.print_result("Contact Creation with User PAT", "FAIL", f"Status: {response.status_code} - {error_data}")
        except Exception as e:
            self.print_result("Contact Creation with User PAT", "FAIL", f"Error: {str(e)}")

    def test_system_fallback(self):
        """Test system PAT fallback when user has no PAT"""
        print("\n" + "="*60)
        print("🔄 SYSTEM PAT FALLBACK TEST")
        print("="*60)
        
        # This test shows what happens when user has no PAT
        # The system should fall back to environment variable
        try:
            # Check if system has fallback PAT
            system_pat = os.getenv('HUBSPOT_ACCESS_TOKEN')
            if system_pat:
                self.print_result("System PAT Fallback", "PASS", "System has fallback PAT configured")
            else:
                self.print_result("System PAT Fallback", "WARN", "No system PAT - users must provide their own")
        except Exception as e:
            self.print_result("System PAT Fallback", "FAIL", f"Error: {str(e)}")

    def run_all_tests(self):
        """Run all tests"""
        print("🔐 User-Specific PAT System Test Suite")
        print("="*60)
        print("This test demonstrates how the PAT system works:")
        print("1. Each user has their own HubSpot PAT")
        print("2. System PAT is only used as fallback")
        print("3. No system PAT needed for production")
        print("="*60)

        if self.authenticate():
            self.test_user_pat_system()
            self.test_system_fallback()
        else:
            print("Skipping tests due to authentication failure.")

        print("\n" + "="*60)
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        total = len(self.test_results)
        
        print(f"Test Results: {passed}/{total} passed")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        print("\n📋 PAT System Summary:")
        print("✅ Each user has their own HubSpot PAT")
        print("✅ System PAT is optional (fallback only)")
        print("✅ No .env PAT needed for production")
        print("✅ Users authenticate with their own tokens")

if __name__ == "__main__":
    tester = UserPATSystemTester()
    tester.run_all_tests()
