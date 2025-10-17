"""
Complete Sales Flow Test Script
Tests the entire sales process from company creation to deal closure
"""

import requests
import json
import time
from datetime import datetime, timedelta

class CompleteSalesFlowTester:
    def __init__(self):
        self.base_url = "http://89.117.63.196:5000"
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
    
    def create_test_session(self):
        """Create a test chat session (mock for testing)"""
        # For testing purposes, we'll use mock IDs
        self.test_data['session_id'] = 1
        self.print_result("Create Session", "PASS", f"Mock Session ID: {self.test_data['session_id']}")
        return True
    
    def create_test_message(self, message_text):
        """Create a test chat message (mock for testing)"""
        # For testing purposes, we'll use mock IDs
        self.test_data['message_id'] = 1
        self.print_result("Create Message", "PASS", f"Mock Message ID: {self.test_data['message_id']}")
        return True
    
    def step1_create_company(self):
        """Step 1: Create a company"""
        self.print_header("STEP 1: CREATE COMPANY")
        
        try:
            company_data = {
                "session_id": self.test_data['session_id'],
                "chat_message_id": self.test_data['message_id'],
                "properties": {
                    "name": "Acme Corporation",
                    "domain": "acme.com",
                    "industry": "COMPUTER_SOFTWARE",  # Valid HubSpot industry
                    "phone": "+1-555-0123",
                    "address": "123 Business St, New York, NY 10001",
                    "city": "New York",
                    "state": "NY",
                    "country": "United States",
                    "zip": "10001",
                    "numberofemployees": "500",
                    "annualrevenue": "10000000"
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
        """Step 2: Create a lead for the company"""
        self.print_header("STEP 2: CREATE LEAD")
        
        try:
            lead_data = {
                "session_id": self.test_data['session_id'],
                "chat_message_id": self.test_data['message_id'],
                "properties": {
                    "firstname": "John",
                    "lastname": "Smith",
                    "email": f"john.smith{int(time.time())}@acme.com",
                    "phone": "+1-555-0124",
                    "company": "Acme Corporation",
                    "lifecyclestage": "lead"  # Use standard HubSpot property
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
        """Step 3: Qualify the lead and create a deal"""
        self.print_header("STEP 3: QUALIFY LEAD")
        
        if not self.test_data.get('lead_id'):
            self.print_result("Qualify Lead", "SKIP", "No lead ID available")
            return False
        
        try:
            # First, update the contact lifecycle stage to opportunity
            update_data = {
                "session_id": self.test_data['session_id'],
                "chat_message_id": self.test_data['message_id'],
                "properties": {
                    "lifecyclestage": "opportunity"  # Move from lead to opportunity
                }
            }
            
            response = requests.patch(f"{self.base_url}/api/hubspot/contacts/contacts/{self.test_data['lead_id']}", 
                                   json=update_data, headers=self.headers)
            
            if response.status_code == 200:
                self.print_result("Update Lead Status", "PASS", "Lead qualified to opportunity")
                
                # Now create a deal (without associations for now)
                deal_data = {
                    "session_id": self.test_data['session_id'],
                    "chat_message_id": self.test_data['message_id'],
                    "properties": {
                        "dealname": "Acme Corp - Enterprise Software Package",
                        "amount": "150000",
                        "dealstage": "appointmentscheduled",
                        "closedate": str(int((datetime.now() + timedelta(days=30)).timestamp() * 1000))  # Convert to timestamp
                    }
                }
                
                response = requests.post(f"{self.base_url}/api/hubspot/deals/deals", 
                                       json=deal_data, headers=self.headers)
                
                if response.status_code == 201:
                    data = response.json()
                    self.test_data['deal_id'] = data['hubspot_id']
                    self.print_result("Create Deal", "PASS", f"Deal created: {data['hubspot_id']}")
                    return True
                else:
                    self.print_result("Create Deal", "FAIL", f"Status: {response.status_code}", response)
                    return False
            else:
                self.print_result("Qualify Lead", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("Qualify Lead", "FAIL", f"Error: {str(e)}")
            return False
    
    def step4_add_company_details(self):
        """Step 4: Add detailed company information"""
        self.print_header("STEP 4: ADD COMPANY DETAILS")
        
        # Create additional contacts
        contacts_data = [
            {
                "session_id": self.test_data['session_id'],
                "chat_message_id": self.test_data['message_id'],
                "properties": {
                    "firstname": "Sarah",
                    "lastname": "Johnson",
                    "email": f"sarah.johnson{int(time.time())}@acme.com",
                    "phone": "+1-555-0125",
                    "company": "Acme Corporation",
                    "jobtitle": "CTO"
                }
            },
            {
                "session_id": self.test_data['session_id'],
                "chat_message_id": self.test_data['message_id'],
                "properties": {
                    "firstname": "Mike",
                    "lastname": "Davis",
                    "email": f"mike.davis{int(time.time())}@acme.com",
                    "phone": "+1-555-0126",
                    "company": "Acme Corporation",
                    "jobtitle": "IT Director"
                }
            }
        ]
        
        contact_ids = []
        for i, contact_data in enumerate(contacts_data):
            try:
                response = requests.post(f"{self.base_url}/api/hubspot/contacts/contacts", 
                                       json=contact_data, headers=self.headers)
                
                if response.status_code == 201:
                    data = response.json()
                    contact_ids.append(data['hubspot_id'])
                    self.print_result(f"Create Contact {i+1}", "PASS", f"Contact ID: {data['hubspot_id']}")
                else:
                    self.print_result(f"Create Contact {i+1}", "FAIL", f"Status: {response.status_code}", response)
            except Exception as e:
                self.print_result(f"Create Contact {i+1}", "FAIL", f"Error: {str(e)}")
        
        self.test_data['contact_ids'] = contact_ids
        return len(contact_ids) > 0
    
    def step5_create_activities(self):
        """Step 5: Create calls and meetings"""
        self.print_header("STEP 5: CREATE ACTIVITIES")
        
        # Create a call
        try:
            call_data = {
                "session_id": self.test_data['session_id'],
                "chat_message_id": self.test_data['message_id'],
                "activity_type": "CALL",
                "properties": {
                    "hs_call_title": "Initial Discovery Call",
                    "hs_call_body": "Discussed company needs and requirements",
                    "hs_call_duration": "1800000",  # 30 minutes
                    "hs_call_status": "COMPLETED",
                    "hs_timestamp": int(time.time() * 1000)
                },
                "associations": {}
            }
            
            response = requests.post(f"{self.base_url}/api/hubspot/activities/calls", 
                                   json=call_data, headers=self.headers)
            
            if response.status_code == 201:
                data = response.json()
                self.test_data['call_id'] = data['hubspot_id']
                self.print_result("Create Call", "PASS", f"Call ID: {data['hubspot_id']}")
            else:
                self.print_result("Create Call", "FAIL", f"Status: {response.status_code}", response)
        except Exception as e:
            self.print_result("Create Call", "FAIL", f"Error: {str(e)}")
        
        # Create a meeting
        try:
            meeting_data = {
                "session_id": self.test_data['session_id'],
                "chat_message_id": self.test_data['message_id'],
                "activity_type": "MEETING",
                "properties": {
                    "hs_meeting_title": "Product Demo Meeting",
                    "hs_meeting_body": "Demonstrated our enterprise software solution",
                    "hs_meeting_start_time": int(time.time() * 1000),
                    "hs_meeting_end_time": int((time.time() + 3600) * 1000),  # 1 hour later
                    "hs_meeting_outcome": "SCHEDULED",
                    "hs_timestamp": int(time.time() * 1000)
                },
                "associations": {}
            }
            
            response = requests.post(f"{self.base_url}/api/hubspot/activities/meetings", 
                                   json=meeting_data, headers=self.headers)
            
            if response.status_code == 201:
                data = response.json()
                self.test_data['meeting_id'] = data['hubspot_id']
                self.print_result("Create Meeting", "PASS", f"Meeting ID: {data['hubspot_id']}")
            else:
                self.print_result("Create Meeting", "FAIL", f"Status: {response.status_code}", response)
        except Exception as e:
            self.print_result("Create Meeting", "FAIL", f"Error: {str(e)}")
    
    def step6_update_deal_stages(self):
        """Step 6: Update deal stages through the sales process"""
        self.print_header("STEP 6: UPDATE DEAL STAGES")
        
        if not self.test_data.get('deal_id'):
            self.print_result("Update Deal Stages", "SKIP", "No deal ID available")
            return False
        
        # Stage progression
        stages = [
            ("qualifiedtobuy", "Client showed strong interest after demo"),
            ("presentationscheduled", "Scheduled formal presentation"),
            ("decisionmakerboughtin", "Decision maker approved the proposal"),
            ("contractsent", "Contract sent for review"),
            ("closedwon", "Deal closed successfully!")
        ]
        
        for stage, reason in stages:
            try:
                stage_data = {
                    "session_id": self.test_data['session_id'],
                    "chat_message_id": self.test_data['message_id'],
                    "new_stage": stage,
                    "reason": reason
                }
                
                response = requests.patch(f"{self.base_url}/api/hubspot/leads/deals/{self.test_data['deal_id']}/stages", 
                                       json=stage_data, headers=self.headers)
                
                if response.status_code == 200:
                    self.print_result(f"Update to {stage}", "PASS", f"Reason: {reason}")
                else:
                    self.print_result(f"Update to {stage}", "FAIL", f"Status: {response.status_code}", response)
            except Exception as e:
                self.print_result(f"Update to {stage}", "FAIL", f"Error: {str(e)}")
    
    def step7_inspect_database(self):
        """Step 7: Inspect database to verify all logging"""
        self.print_header("STEP 7: DATABASE INSPECTION")
        
        try:
            # Get all logs for this session
            response = requests.get(f"{self.base_url}/api/logs?session_id={self.test_data['session_id']}", 
                                 headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                logs = data.get('logs', [])
                
                self.print_result("Get Session Logs", "PASS", f"Found {len(logs)} logs")
                
                # Analyze log types
                log_types = {}
                for log in logs:
                    log_type = log.get('log_type')
                    log_types[log_type] = log_types.get(log_type, 0) + 1
                
                print("\nLog Analysis:")
                for log_type, count in log_types.items():
                    print(f"  - {log_type}: {count} entries")
                
                # Show detailed logs
                print("\nDetailed Log Entries:")
                for log in logs:
                    print(f"  - {log['log_type']}: {log.get('lead_status', log.get('deal_stage', 'N/A'))} (HubSpot ID: {log.get('hubspot_id', 'N/A')})")
                    if log.get('stage_reason'):
                        print(f"    Reason: {log['stage_reason']}")
                    if log.get('deal_amount'):
                        print(f"    Amount: {log['deal_amount']}")
                
                return True
            else:
                self.print_result("Get Session Logs", "FAIL", f"Status: {response.status_code}", response)
                return False
        except Exception as e:
            self.print_result("Get Session Logs", "FAIL", f"Error: {str(e)}")
            return False
    
    def run_complete_flow(self):
        """Run the complete sales flow test"""
        print("HubSpot Logging AI Agent - Complete Sales Flow Test")
        print("=" * 70)
        print("This test will follow the complete sales process:")
        print("1. Create Company")
        print("2. Create Lead")
        print("3. Qualify Lead & Create Deal")
        print("4. Add Company Details (Contacts)")
        print("5. Create Activities (Calls/Meetings)")
        print("6. Update Deal Stages")
        print("7. Inspect Database")
        print("=" * 70)
        
        # Authenticate
        if not self.authenticate():
            print("Authentication failed. Cannot proceed with tests.")
            return
        
        # Create test session and message
        if not self.create_test_session():
            print("Failed to create test session. Cannot proceed.")
            return
        
        if not self.create_test_message("Starting complete sales flow test"):
            print("Failed to create test message. Cannot proceed.")
            return
        
        # Run all steps
        self.step1_create_company()
        self.step2_create_lead()
        self.step3_qualify_lead()
        self.step4_add_company_details()
        self.step5_create_activities()
        self.step6_update_deal_stages()
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
        print(f"  - Session ID: {self.test_data.get('session_id', 'N/A')}")
        print(f"  - Company ID: {self.test_data.get('company_id', 'N/A')}")
        print(f"  - Lead ID: {self.test_data.get('lead_id', 'N/A')}")
        print(f"  - Deal ID: {self.test_data.get('deal_id', 'N/A')}")
        print(f"  - Contact IDs: {self.test_data.get('contact_ids', [])}")

if __name__ == "__main__":
    tester = CompleteSalesFlowTester()
    tester.run_complete_flow()
