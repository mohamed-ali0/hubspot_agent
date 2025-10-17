"""
Test script for Leads and Deal Stages functionality
"""

import requests
import json
import time

class LeadsAndDealStagesTester:
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
                self.print_result("Authentication", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("Authentication", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_get_leads(self):
        """Test getting leads"""
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/leads/leads", headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                lead_count = len(data.get('results', []))
                self.print_result("GET Leads", "PASS", f"Found {lead_count} leads")
                return True
            else:
                self.print_result("GET Leads", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("GET Leads", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_create_lead(self):
        """Test creating a lead"""
        try:
            lead_data = {
                "session_id": 1,
                "chat_message_id": 5,
                "firstname": "Test",
                "lastname": "Lead",
                "email": f"testlead{int(time.time())}@example.com",
                "phone": "+1234567890",
                "company": "Test Company",
                "lead_source": "WhatsApp",
                "lead_status": "NEW"
            }
            
            response = requests.post(f"{self.base_url}/api/hubspot/leads/leads", 
                                   json=lead_data, headers=self.headers)
            
            if response.status_code == 201:
                data = response.json()
                self.lead_id = data.get('hubspot_id')
                self.print_result("POST Create Lead", "PASS", f"Created lead with ID: {self.lead_id}")
                return True
            else:
                self.print_result("POST Create Lead", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("POST Create Lead", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_qualify_lead(self):
        """Test qualifying a lead"""
        if not hasattr(self, 'lead_id'):
            self.print_result("POST Qualify Lead", "SKIP", "No lead ID available")
            return False
            
        try:
            qualify_data = {
                "session_id": 1,
                "chat_message_id": 6,
                "lead_status": "QUALIFIED",
                "create_deal": True,
                "deal_name": "Test Deal - Premium Package",
                "deal_amount": "25000",
                "deal_stage": "appointmentscheduled",
                "close_date": "2025-02-15T00:00:00Z"
            }
            
            response = requests.post(f"{self.base_url}/api/hubspot/leads/leads/{self.lead_id}/qualify", 
                                   json=qualify_data, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                deal_created = data.get('deal_created', False)
                deal_id = data.get('deal_id')
                if deal_created and deal_id:
                    self.deal_id = deal_id
                    self.print_result("POST Qualify Lead", "PASS", f"Qualified lead and created deal: {deal_id}")
                else:
                    self.print_result("POST Qualify Lead", "PASS", "Qualified lead without creating deal")
                return True
            else:
                self.print_result("POST Qualify Lead", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("POST Qualify Lead", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_get_deal_pipelines(self):
        """Test getting deal pipelines"""
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/leads/pipelines", headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                pipeline_count = len(data.get('results', []))
                self.print_result("GET Deal Pipelines", "PASS", f"Found {pipeline_count} pipelines")
                return True
            else:
                self.print_result("GET Deal Pipelines", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("GET Deal Pipelines", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_update_deal_stage(self):
        """Test updating deal stage"""
        if not hasattr(self, 'deal_id'):
            self.print_result("PATCH Update Deal Stage", "SKIP", "No deal ID available")
            return False
            
        try:
            stage_data = {
                "session_id": 1,
                "chat_message_id": 7,
                "new_stage": "qualifiedtobuy",
                "reason": "Client showed strong interest in the product"
            }
            
            response = requests.patch(f"{self.base_url}/api/hubspot/leads/deals/{self.deal_id}/stages", 
                                   json=stage_data, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                new_stage = data.get('new_stage')
                self.print_result("PATCH Update Deal Stage", "PASS", f"Updated deal stage to: {new_stage}")
                return True
            else:
                self.print_result("PATCH Update Deal Stage", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("PATCH Update Deal Stage", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_get_lead_analytics(self):
        """Test getting lead analytics"""
        try:
            response = requests.get(f"{self.base_url}/api/hubspot/leads/leads/analytics", headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                total_leads = data.get('total_leads', 0)
                self.print_result("GET Lead Analytics", "PASS", f"Analytics retrieved - {total_leads} total leads")
                return True
            else:
                self.print_result("GET Lead Analytics", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("GET Lead Analytics", "FAIL", f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all leads and deal stages tests"""
        print("HubSpot Logging AI Agent - Leads & Deal Stages Test")
        print("=" * 60)
        
        # Authenticate first
        if not self.authenticate():
            print("Authentication failed. Cannot proceed with tests.")
            return
        
        # Test leads functionality
        self.print_header("LEADS FUNCTIONALITY")
        self.test_get_leads()
        self.test_create_lead()
        self.test_qualify_lead()
        
        # Test deal stages functionality
        self.print_header("DEAL STAGES FUNCTIONALITY")
        self.test_get_deal_pipelines()
        self.test_update_deal_stage()
        
        # Test analytics
        self.print_header("ANALYTICS")
        self.test_get_lead_analytics()
        
        # Print summary
        self.print_header("TEST SUMMARY")
        passed = sum(1 for result in self.test_results if result['status'] == 'PASS')
        failed = sum(1 for result in self.test_results if result['status'] == 'FAIL')
        skipped = sum(1 for result in self.test_results if result['status'] == 'SKIP')
        total = len(self.test_results)
        
        print(f"[OK] Passed: {passed}")
        print(f"[ERROR] Failed: {failed}")
        print(f"[SKIP] Skipped: {skipped}")
        print(f"[TOTAL] Total: {total}")
        
        if total > 0:
            success_rate = (passed / total) * 100
            print(f"[SUCCESS] Success Rate: {success_rate:.1f}%")
        
        if failed > 0:
            print("\n[WARNING] Some tests failed. Check the details above.")
        else:
            print("\n[SUCCESS] All tests passed!")

if __name__ == "__main__":
    tester = LeadsAndDealStagesTester()
    tester.run_all_tests()
