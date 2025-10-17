"""
Working Complete Sales Flow Test Script
Tests the entire sales process with valid HubSpot API calls
"""

import requests
import json
import time
from datetime import datetime, timedelta

class WorkingCompleteSalesFlowTester:
    def __init__(self):
        self.base_url = "http://89.117.63.196:5012"
        self.token = None
        self.headers = {}
        self.test_data = {}
        self.test_results = []
        
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "=" * 70)
        print(f" {title}")
        print("=" * 70)
    
    def print_result(self, test_name, status, details="", response=None):
        """Print test result with detailed information"""
        status_icon = "[OK]" if status == "PASS" else "[ERROR]" if status == "FAIL" else "[SKIP]"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        
        if status == "FAIL" and response is not None:
            try:
                error_data = response.json()
                if 'error' in error_data:
                    print(f"   Error: {error_data['error']}")
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
                self.print_result("Authentication", "PASS", "Successfully authenticated")
                return True
            else:
                self.print_result("Authentication", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("Authentication", "FAIL", f"Error: {str(e)}")
            return False
    
    def step1_create_company(self):
        """Step 1: Create a company"""
        self.print_header("STEP 1: CREATE COMPANY")
        
        try:
            company_data = {
                "session_id": 1,
                "chat_message_id": 1,
                "properties": {
                    "name": "Acme Corporation",
                    "domain": "acme.com",
                    "industry": "COMPUTER_SOFTWARE",
                    "phone": "+1-555-0123",
                    "city": "New York",
                    "state": "NY",
                    "country": "United States"
                }
            }
            
            response = requests.post(f"{self.base_url}/api/hubspot/companies/companies", 
                                   json=company_data, headers=self.headers)
            
            if response.status_code == 201:
                data = response.json()
                self.test_data['company_id'] = data['hubspot_id']
                self.print_result("Create Company", "PASS", f"Company ID: {data['hubspot_id']}")
                return True
            else:
                self.print_result("Create Company", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("Create Company", "FAIL", f"Error: {str(e)}")
            return False
    
    def step2_create_lead(self):
        """Step 2: Create a lead (contact with lead lifecycle stage)"""
        self.print_header("STEP 2: CREATE LEAD")
        
        try:
            lead_data = {
                "session_id": 1,
                "chat_message_id": 1,
                "properties": {
                    "firstname": "John",
                    "lastname": "Smith",
                    "email": f"john.smith{int(time.time())}@acme.com",
                    "phone": "+1-555-0124",
                    "company": "Acme Corporation",
                    "lifecyclestage": "lead"
                }
            }
            
            response = requests.post(f"{self.base_url}/api/hubspot/contacts/contacts", 
                                   json=lead_data, headers=self.headers)
            
            if response.status_code == 201:
                data = response.json()
                self.test_data['lead_id'] = data['hubspot_id']
                self.print_result("Create Lead", "PASS", f"Lead ID: {data['hubspot_id']}")
                return True
            else:
                self.print_result("Create Lead", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("Create Lead", "FAIL", f"Error: {str(e)}")
            return False
    
    def step3_qualify_lead(self):
        """Step 3: Qualify the lead by updating lifecycle stage"""
        self.print_header("STEP 3: QUALIFY LEAD")
        
        if not self.test_data.get('lead_id'):
            self.print_result("Qualify Lead", "SKIP", "No lead ID available")
            return False
        
        try:
            # Update contact lifecycle stage to opportunity
            update_data = {
                "session_id": 1,
                "chat_message_id": 1,
                "properties": {
                    "lifecyclestage": "opportunity"
                }
            }
            
            response = requests.patch(f"{self.base_url}/api/hubspot/contacts/contacts/{self.test_data['lead_id']}", 
                                   json=update_data, headers=self.headers)
            
            if response.status_code == 200:
                self.print_result("Qualify Lead", "PASS", "Lead qualified to opportunity")
                return True
            else:
                self.print_result("Qualify Lead", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("Qualify Lead", "FAIL", f"Error: {str(e)}")
            return False
    
    def step4_create_deal(self):
        """Step 4: Create a deal"""
        self.print_header("STEP 4: CREATE DEAL")
        
        try:
            deal_data = {
                "session_id": 1,
                "chat_message_id": 1,
                "properties": {
                    "dealname": "Acme Corp - Enterprise Software Package",
                    "amount": "150000",
                    "dealstage": "appointmentscheduled",
                    "closedate": (datetime.now() + timedelta(days=30)).isoformat()
                },
                "associations": [
                    {
                        "to": {"id": self.test_data.get('lead_id', '')},
                        "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3}]
                    },
                    {
                        "to": {"id": self.test_data.get('company_id', '')},
                        "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 5}]
                    }
                ]
            }
            
            response = requests.post(f"{self.base_url}/api/hubspot/deals/deals", 
                                   json=deal_data, headers=self.headers)
            
            if response.status_code == 201:
                data = response.json()
                self.test_data['deal_id'] = data['hubspot_id']
                self.print_result("Create Deal", "PASS", f"Deal ID: {data['hubspot_id']}")
                return True
            else:
                self.print_result("Create Deal", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("Create Deal", "FAIL", f"Error: {str(e)}")
            return False
    
    def step5_create_activities(self):
        """Step 5: Create activities (notes and tasks)"""
        self.print_header("STEP 5: CREATE ACTIVITIES")
        
        # Create a note
        try:
            note_data = {
                "session_id": 1,
                "chat_message_id": 1,
                "properties": {
                    "hs_note_body": "Initial meeting with client. Discussed their requirements for enterprise software solution. Client showed strong interest in our platform."
                },
                "associations": [
                    {
                        "to": {"id": self.test_data.get('lead_id', '')},
                        "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3}]
                    }
                ]
            }
            
            response = requests.post(f"{self.base_url}/api/hubspot/notes/notes", 
                                   json=note_data, headers=self.headers)
            
            if response.status_code == 201:
                data = response.json()
                self.test_data['note_id'] = data['hubspot_id']
                self.print_result("Create Note", "PASS", f"Note ID: {data['hubspot_id']}")
            else:
                self.print_result("Create Note", "FAIL", f"Status: {response.status_code}", response)
        except Exception as e:
            self.print_result("Create Note", "FAIL", f"Error: {str(e)}")
        
        # Create a task
        try:
            task_data = {
                "session_id": 1,
                "chat_message_id": 1,
                "properties": {
                    "hs_task_subject": "Follow up with client",
                    "hs_task_body": "Send proposal and schedule demo meeting",
                    "hs_task_status": "NOT_STARTED",
                    "hs_task_priority": "HIGH",
                    "hs_timestamp": int(time.time() * 1000)
                },
                "associations": [
                    {
                        "to": {"id": self.test_data.get('lead_id', '')},
                        "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3}]
                    }
                ]
            }
            
            response = requests.post(f"{self.base_url}/api/hubspot/tasks/tasks", 
                                   json=task_data, headers=self.headers)
            
            if response.status_code == 201:
                data = response.json()
                self.test_data['task_id'] = data['hubspot_id']
                self.print_result("Create Task", "PASS", f"Task ID: {data['hubspot_id']}")
            else:
                self.print_result("Create Task", "FAIL", f"Status: {response.status_code}", response)
        except Exception as e:
            self.print_result("Create Task", "FAIL", f"Error: {str(e)}")
    
    def step6_update_deal_stage(self):
        """Step 6: Update deal stage"""
        self.print_header("STEP 6: UPDATE DEAL STAGE")
        
        if not self.test_data.get('deal_id'):
            self.print_result("Update Deal Stage", "SKIP", "No deal ID available")
            return False
        
        try:
            stage_data = {
                "session_id": 1,
                "chat_message_id": 1,
                "new_stage": "qualifiedtobuy",
                "reason": "Client showed strong interest after initial meeting"
            }
            
            response = requests.patch(f"{self.base_url}/api/hubspot/leads/deals/{self.test_data['deal_id']}/stages", 
                                   json=stage_data, headers=self.headers)
            
            if response.status_code == 200:
                self.print_result("Update Deal Stage", "PASS", "Deal stage updated to qualifiedtobuy")
                return True
            else:
                self.print_result("Update Deal Stage", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("Update Deal Stage", "FAIL", f"Error: {str(e)}")
            return False
    
    def step7_inspect_database(self):
        """Step 7: Inspect database to verify all logging"""
        self.print_header("STEP 7: DATABASE INSPECTION")
        
        try:
            # Get all logs
            response = requests.get(f"{self.base_url}/api/logs", headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                logs = data.get('logs', [])
                
                self.print_result("Get All Logs", "PASS", f"Found {len(logs)} total logs")
                
                # Analyze log types
                log_types = {}
                for log in logs:
                    log_type = log.get('log_type')
                    log_types[log_type] = log_types.get(log_type, 0) + 1
                
                print("\nLog Analysis:")
                for log_type, count in log_types.items():
                    print(f"  - {log_type}: {count} entries")
                
                # Show recent logs (last 10)
                recent_logs = logs[-10:] if len(logs) > 10 else logs
                print(f"\nRecent Log Entries (last {len(recent_logs)}):")
                for log in recent_logs:
                    print(f"  - {log['log_type']}: HubSpot ID {log.get('hubspot_id', 'N/A')} - {log.get('sync_status', 'N/A')}")
                    if log.get('lead_status'):
                        print(f"    Lead Status: {log['lead_status']}")
                    if log.get('deal_stage'):
                        print(f"    Deal Stage: {log['deal_stage']}")
                    if log.get('stage_reason'):
                        print(f"    Reason: {log['stage_reason']}")
                
                return True
            else:
                self.print_result("Get All Logs", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("Get All Logs", "FAIL", f"Error: {str(e)}")
            return False
    
    def run_complete_flow(self):
        """Run the complete sales flow test"""
        print("HubSpot Logging AI Agent - Working Complete Sales Flow Test")
        print("=" * 70)
        print("This test will follow the complete sales process:")
        print("1. Create Company")
        print("2. Create Lead")
        print("3. Qualify Lead")
        print("4. Create Deal")
        print("5. Create Activities")
        print("6. Update Deal Stage")
        print("7. Inspect Database")
        print("=" * 70)
        
        # Authenticate
        if not self.authenticate():
            print("Authentication failed. Cannot proceed with tests.")
            return
        
        # Run all steps
        self.step1_create_company()
        self.step2_create_lead()
        self.step3_qualify_lead()
        self.step4_create_deal()
        self.step5_create_activities()
        self.step6_update_deal_stage()
        self.step7_inspect_database()
        
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
            print("\n[SUCCESS] Complete sales flow test completed!")
        
        print(f"\nTest Data Summary:")
        print(f"  - Company ID: {self.test_data.get('company_id', 'N/A')}")
        print(f"  - Lead ID: {self.test_data.get('lead_id', 'N/A')}")
        print(f"  - Deal ID: {self.test_data.get('deal_id', 'N/A')}")
        print(f"  - Note ID: {self.test_data.get('note_id', 'N/A')}")
        print(f"  - Task ID: {self.test_data.get('task_id', 'N/A')}")

if __name__ == "__main__":
    tester = WorkingCompleteSalesFlowTester()
    tester.run_complete_flow()
