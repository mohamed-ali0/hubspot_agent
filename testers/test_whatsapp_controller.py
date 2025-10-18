"""
Test script for WhatsApp controller
"""

import requests
import json
import time

class WhatsAppControllerTester:
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
                print(f"[OK] Authentication: PASS")
                return True
            else:
                print(f"[ERROR] Authentication: FAIL - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] Authentication: FAIL - Error: {str(e)}")
            return False
    
    def test_webhook_verification(self):
        """Test webhook verification (GET request)"""
        try:
            response = requests.get(f"{self.base_url}/api/whatsapp/webhook?hub.challenge=test123")
            
            if response.status_code == 200 and response.text == "test123":
                print(f"[OK] Webhook Verification: PASS")
                return True
            else:
                print(f"[ERROR] Webhook Verification: FAIL - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] Webhook Verification: FAIL - Error: {str(e)}")
            return False
    
    def test_webhook_message(self):
        """Test webhook message processing (POST request)"""
        try:
            # Simulate Twilio webhook payload
            webhook_data = {
                "entry": [{
                    "changes": [{
                        "value": {
                            "messages": [{
                                "id": f"test_msg_{int(time.time())}",
                                "from": "+1234567890",
                                "text": {"body": "Hello, I want to create a contact"},
                                "timestamp": str(int(time.time()))
                            }]
                        }
                    }]
                }]
            }
            
            response = requests.post(f"{self.base_url}/api/whatsapp/webhook", 
                                   json=webhook_data)
            
            if response.status_code == 200:
                print(f"[OK] Webhook Message Processing: PASS")
                return True
            else:
                print(f"[ERROR] Webhook Message Processing: FAIL - Status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"[ERROR] Webhook Message Processing: FAIL - Error: {str(e)}")
            return False
    
    def test_send_message(self):
        """Test sending WhatsApp message"""
        try:
            message_data = {
                "to": "+1234567890",
                "message": "Hello from your AI agent!",
                "session_id": 1,
                "message_id": 1
            }
            
            response = requests.post(f"{self.base_url}/api/whatsapp/send", 
                                   json=message_data, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Send Message: PASS - {data.get('message')}")
                return True
            else:
                print(f"[ERROR] Send Message: FAIL - Status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"[ERROR] Send Message: FAIL - Error: {str(e)}")
            return False
    
    def test_status(self):
        """Test WhatsApp status endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/whatsapp/status")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Status Check: PASS")
                print(f"  Active Sessions: {data.get('active_sessions')}")
                print(f"  Recent Messages: {data.get('recent_messages')}")
                return True
            else:
                print(f"[ERROR] Status Check: FAIL - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] Status Check: FAIL - Error: {str(e)}")
            return False
    
    def test_sessions(self):
        """Test getting chat sessions"""
        try:
            response = requests.get(f"{self.base_url}/api/whatsapp/sessions", 
                                  headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Get Sessions: PASS - Found {data.get('total')} sessions")
                return True
            else:
                print(f"[ERROR] Get Sessions: FAIL - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] Get Sessions: FAIL - Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all WhatsApp controller tests"""
        print("WhatsApp Controller Test Suite")
        print("=" * 50)
        
        tests = [
            ("Authentication", self.authenticate),
            ("Webhook Verification", self.test_webhook_verification),
            ("Webhook Message Processing", self.test_webhook_message),
            ("Send Message", self.test_send_message),
            ("Status Check", self.test_status),
            ("Get Sessions", self.test_sessions)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n--- {test_name} ---")
            if test_func():
                passed += 1
        
        print(f"\n{'='*50}")
        print(f"Test Results: {passed}/{total} passed")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("[SUCCESS] All WhatsApp controller tests passed!")
        else:
            print("[WARNING] Some tests failed. Check the details above.")

if __name__ == "__main__":
    tester = WhatsAppControllerTester()
    tester.run_all_tests()
