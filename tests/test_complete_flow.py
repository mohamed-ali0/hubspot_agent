#!/usr/bin/env python3
"""
Complete Flow Test Script

This script tests the complete flow from:
1. User authentication
2. Session creation
3. Message creation
4. AI analysis of message
5. HubSpot sync with logging
6. Verification of logs in database

Usage:
    python tests/test_complete_flow.py
"""

#!/usr/bin/env python3
"""
Complete Flow Test Script

This script tests the complete HubSpot Logging API by making HTTP requests to endpoints.
Tests the actual API functionality without direct database access.
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = "http://89.117.63.196:5012"

def get_auth_token():
    """Get authentication token"""
    login_data = {
        'username': 'flow_tester',
        'password': 'testpass123'
    }

    response = requests.post(
        f'{BASE_URL}/api/auth/login',
        json=login_data,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        return response.json()['token']
    return None

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f'{BASE_URL}/api/health')
    return response.status_code == 200

def test_authentication():
    """Test authentication"""
    token = get_auth_token()
    return token is not None

def test_create_session():
    """Test session creation"""
    token = get_auth_token()
    if not token:
        return False

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    session_data = {'user_id': 1}  # Using existing user ID

    response = requests.post(
        f'{BASE_URL}/api/sessions',
        json=session_data,
        headers=headers
    )

    return response.status_code == 201

def test_create_message():
    """Test message creation"""
    token = get_auth_token()
    if not token:
        return False

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    message_data = {
        'message_text': 'Test message for complete flow testing',
        'forwarded_from': '+1234567890'
    }

    response = requests.post(
        f'{BASE_URL}/api/sessions/1/messages',  # Using session ID 1
        json=message_data,
        headers=headers
    )

    return response.status_code == 201

def test_create_logs():
    """Test log creation"""
    token = get_auth_token()
    if not token:
        return False

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Create contact log
    contact_log_data = {
        'session_id': 1,
        'chat_message_id': 1,
        'log_type': 'contact_action',
        'hubspot_payload': {
            'properties': {
                'firstname': 'Test',
                'lastname': 'User',
                'email': 'test@example.com',
                'phone': '+1234567890'
            }
        }
    }

    response = requests.post(
        f'{BASE_URL}/api/logs',
        json=contact_log_data,
        headers=headers
    )

    return response.status_code == 201

def test_hubspot_integration():
    """Test HubSpot record creation"""
    token = get_auth_token()
    if not token:
        return False

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Create contact via API
    contact_data = {
        'session_id': 1,
        'chat_message_id': 1,
        'properties': {
            'firstname': 'API',
            'lastname': 'Test',
            'email': f'test-{int(time.time())}@example.com',
            'phone': '+1234567890'
        }
    }

    response = requests.post(
        f'{BASE_URL}/api/hubspot/contacts',
        json=contact_data,
        headers=headers
    )

    return response.status_code == 201

def test_get_logs():
    """Test getting logs"""
    token = get_auth_token()
    if not token:
        return False

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(
        f'{BASE_URL}/api/logs',
        headers=headers
    )

    return response.status_code == 200

def test_analytics():
    """Test analytics"""
    token = get_auth_token()
    if not token:
        return False

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(
        f'{BASE_URL}/api/stats/overview',
        headers=headers
    )

    return response.status_code == 200

def run_complete_flow():
    """Run the complete flow test"""
    print("Starting Complete Flow Test")
    print("=" * 60)

    tests = [
        ("Health Check", test_health_check),
        ("Authentication", test_authentication),
        ("Session Creation", test_create_session),
        ("Message Creation", test_create_message),
        ("Log Creation", test_create_logs),
        ("HubSpot Integration", test_hubspot_integration),
        ("Get Logs", test_get_logs),
        ("Analytics", test_analytics)
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"[OK] {test_name}")
            else:
                failed += 1
                print(f"[ERROR] {test_name}")
        except Exception as e:
            failed += 1
            print(f"[ERROR] {test_name}: {str(e)}")

    print("\n" + "=" * 60)
    print("COMPLETE FLOW RESULTS")
    print("=" * 60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    print(f"Success Rate: {passed/(passed+failed)*100:.1f}%" if (passed+failed) > 0 else "Success Rate: N/A")

    return failed == 0

if __name__ == "__main__":
    success = run_complete_flow()
    import sys
    sys.exit(0 if success else 1)
        """Setup test environment"""
        print("[SETUP] Setting up complete flow test...")

        # Create Flask app context for database operations
        self.app = create_app()
        self.app.config['TESTING'] = True

        # Use in-memory database for testing
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        # Initialize the database
        with self.app.app_context():
            db.create_all()

            # Create test user
            self.test_user = User(
                name='Flow Test User',
                username='flow_tester',
                password='testpass123',
                phone_number='+1234567890',
                hubspot_pat_token='test-token',
                email='flow_test@example.com'
            )
            db.session.add(self.test_user)
            db.session.commit()

        print(f"[OK] Test user created: {self.test_user.username}")

    def authenticate(self):
        """Authenticate and get token"""
        print("\n[AUTH] Testing authentication...")

        with self.app.test_client() as client:
            with self.app.app_context():
                login_data = {
                    'username': 'flow_tester',
                    'password': 'testpass123'
                }

                response = client.post(
                    '/api/auth/login',
                    json=login_data,
                    headers={'Content-Type': 'application/json'}
                )

                if response.status_code == 200:
                    data = response.get_json()
                    self.auth_token = data['token']
                    print("[OK] Authentication successful")
                    return True
                else:
                    print(f"[ERROR] Authentication failed: {response.get_data(as_text=True)}")
                    return False

    def create_session(self):
        """Create chat session"""
        print("\n[SESSION] Testing session creation...")

        with self.app.test_client() as client:
            with self.app.app_context():
                headers = {
                    'Authorization': f'Bearer {self.auth_token}',
                    'Content-Type': 'application/json'
                }

                session_data = {'user_id': self.test_user.id}

                response = client.post(
                    '/api/sessions',
                    json=session_data,
                    headers=headers
                )

                if response.status_code == 201:
                    data = response.get_json()
                    self.session_id = data['id']
                    print(f"[OK] Session created: {self.session_id}")
                    return True
                else:
                    print(f"[ERROR] Session creation failed: {response.get_data(as_text=True)}")
                    return False

    def create_message(self):
        """Create chat message"""
        print("\n[MESSAGE] Testing message creation...")

        with self.app.test_client() as client:
            with self.app.app_context():
                headers = {
                    'Authorization': f'Bearer {self.auth_token}',
                    'Content-Type': 'application/json'
                }

                message_data = {
                    'message_text': 'Hi Ahmed, I met with you yesterday about the XYZ Corp project. The budget is around $50,000 and we need to follow up next week with a detailed proposal.',
                    'forwarded_from': '+201234567890'
                }

                response = client.post(
                    f'/api/sessions/{self.session_id}/messages',
                    json=message_data,
                    headers=headers
                )

                if response.status_code == 201:
                    data = response.get_json()
                    self.message_id = data['id']
                    print(f"[OK] Message created: {self.message_id}")
                    return True
                else:
                    print(f"[ERROR] Message creation failed: {response.get_data(as_text=True)}")
                    return False

    def analyze_message_ai(self):
        """Test AI analysis of message"""
        print("\n[AI] Testing AI message analysis...")

        # Get the message from database
        with self.app.app_context():
            message = ChatMessage.query.get(self.message_id)

            if message:
                # Test AI analysis
                suggestions = AIService.analyze_message(message.message_text)
                contact_info = AIService.extract_contact_info(message.message_text)
                deal_info = AIService.extract_deal_info(message.message_text)
                log_type_suggestion = AIService.suggest_log_type(message.message_text)

                print("[OK] AI Analysis Results:")
                print(f"  Suggestions: {suggestions}")
                print(f"  Contact Info: {contact_info}")
                print(f"  Deal Info: {deal_info}")
                print(f"  Suggested Log Type: {log_type_suggestion}")

                return True
            else:
                print("[ERROR] Message not found for AI analysis")
                return False

    def create_logs_manually(self):
        """Create logs manually based on AI analysis"""
        print("\n[LOGS] Testing manual log creation...")

        with self.app.test_client() as client:
            with self.app.app_context():
                headers = {
                    'Authorization': f'Bearer {self.auth_token}',
                    'Content-Type': 'application/json'
                }

            # Create contact log
                contact_log_data = {
                    'session_id': self.session_id,
                    'chat_message_id': self.message_id,
                    'log_type': 'contact_action',
                    'hubspot_payload': {
                        'properties': {
                            'firstname': 'Ahmed',
                            'lastname': 'Client',
                            'email': 'ahmed.xyz@example.com',
                            'phone': '+201234567890',
                            'company': 'XYZ Corp'
                        }
                    }
                }

                response = client.post(
                    '/api/logs',
                    json=contact_log_data,
                    headers=headers
                )

                if response.status_code == 201:
                    print("[OK] Contact log created")
                else:
                    print(f"[ERROR] Contact log creation failed: {response.get_data(as_text=True)}")

                # Create deal log
                deal_log_data = {
                    'session_id': self.session_id,
                    'chat_message_id': self.message_id,
                    'log_type': 'deal',
                    'hubspot_payload': {
                        'properties': {
                            'dealname': 'XYZ Corp Project',
                            'amount': '50000',
                            'dealstage': 'qualifiedtobuy',
                            'closedate': '2024-12-31'
                        }
                    }
                }

                response = client.post(
                    '/api/logs',
                    json=deal_log_data,
                    headers=headers
                )

                if response.status_code == 201:
                    print("[OK] Deal log created")
                else:
                    print(f"[ERROR] Deal log creation failed: {response.get_data(as_text=True)}")

                # Create task log
                task_log_data = {
                    'session_id': self.session_id,
                    'chat_message_id': self.message_id,
                    'log_type': 'task',
                    'hubspot_payload': {
                        'properties': {
                            'hs_task_subject': 'Follow up with Ahmed - Send proposal',
                            'hs_task_body': 'Send detailed proposal for XYZ Corp project',
                            'hs_task_status': 'NOT_STARTED',
                            'hs_task_priority': 'HIGH'
                        }
                    }
                }

                response = client.post(
                    '/api/logs',
                    json=task_log_data,
                    headers=headers
                )

                if response.status_code == 201:
                    print("[OK] Task log created")
                    return True
                else:
                    print(f"[ERROR] Task log creation failed: {response.get_data(as_text=True)}")
                    return False

    def create_hubspot_records_via_api(self):
        """Create HubSpot records via our API (with logging)"""
        print("\n[SYNC] Testing HubSpot record creation via API...")

        with self.app.test_client() as client:
            with self.app.app_context():
                headers = {
                    'Authorization': f'Bearer {self.auth_token}',
                    'Content-Type': 'application/json'
                }

                # Create contact via our API
                contact_data = {
                    'session_id': self.session_id,
                    'chat_message_id': self.message_id,
                    'properties': {
                        'firstname': 'Ahmed',
                        'lastname': 'Client',
                        'email': f'test-{int(time.time())}@example.com',
                        'phone': '+201234567890',
                        'company': 'XYZ Corp'
                    }
                }

                response = client.post(
                    '/api/hubspot/contacts',
                    json=contact_data,
                    headers=headers
                )

                if response.status_code == 201:
                    data = response.get_json()
                    print(f"[OK] Contact created via API: {data.get('hubspot_id')}")
                else:
                    print(f"[ERROR] Contact creation via API failed: {response.get_data(as_text=True)}")

                # Create deal via our API
                deal_data = {
                    'session_id': self.session_id,
                    'chat_message_id': self.message_id,
                    'properties': {
                        'dealname': f'XYZ Corp Project - {int(time.time())}',
                        'amount': '50000',
                        'dealstage': 'qualifiedtobuy',
                        'closedate': '2024-12-31'
                    }
                }

                response = client.post(
                    '/api/hubspot/deals',
                    json=deal_data,
                    headers=headers
                )

                if response.status_code == 201:
                    data = response.get_json()
                    print(f"[OK] Deal created via API: {data.get('hubspot_id')}")
                else:
                    print(f"[ERROR] Deal creation via API failed: {response.get_data(as_text=True)}")

    def verify_logs_in_database(self):
        """Verify logs were created in our database"""
        print("\n[DB] Testing database log verification...")

        with self.app.app_context():
            # Check all logs for this session
            logs = Log.query.filter_by(session_id=self.session_id).all()

            print(f"[OK] Found {len(logs)} logs in database for session {self.session_id}")

            for log in logs:
                print(f"  [LOGS] Log {log.id}: {log.log_type} - {log.sync_status}")

                if log.sync_status == 'synced':
                    print(f"    [SYNC] HubSpot ID: {log.hubspot_id}")
                elif log.sync_status == 'failed':
                    print(f"    [ERROR] Error: {log.sync_error}")

            # Check if we have pending logs to sync
            pending_logs = Log.query.filter_by(session_id=self.session_id, sync_status='pending').all()
            if pending_logs:
                print(f"[OK] Found {len(pending_logs)} pending logs ready for sync")

            return len(logs) > 0

    def test_analytics(self):
        """Test analytics endpoints"""
        print("\n[STATS] Testing analytics...")

        with self.app.test_client() as client:
            with self.app.app_context():
                headers = {
                    'Authorization': f'Bearer {self.auth_token}',
                    'Content-Type': 'application/json'
                }

                # Get overview stats
                response = client.get(
                    '/api/stats/overview',
                    headers=headers
                )

                if response.status_code == 200:
                    data = response.get_json()
                    print("[OK] Overview stats retrieved:")
                    print(f"  Sessions: {data.get('total_sessions', 0)}")
                    print(f"  Messages: {data.get('total_messages', 0)}")
                    print(f"  Logs: {data.get('total_logs', 0)}")
                    return True
                else:
                    print(f"[ERROR] Analytics failed: {response.get_data(as_text=True)}")
                    return False

    def run_complete_flow(self):
        """Run the complete flow test"""
        print("Starting Complete Flow Test")
        print("=" * 60)

        # Run all steps
        steps = [
            self.setup,
            self.authenticate,
            self.create_session,
            self.create_message,
            self.analyze_message_ai,
            self.create_logs_manually,
            self.create_hubspot_records_via_api,
            self.verify_logs_in_database,
            self.test_analytics
        ]

        results = []
        for i, step in enumerate(steps, 1):
            print(f"\n[STEP] Step {i}: {step.__name__}")
            try:
                result = step()
                results.append(result)
            except Exception as e:
                print(f"[ERROR] Step {i} failed with exception: {str(e)}")
                results.append(False)

        # Summary
        passed = sum(1 for result in results if result is True)
        total = len(results)

        print("\n" + "=" * 60)
        print("[STATS] COMPLETE FLOW RESULTS")
        print("=" * 60)
        print(f"Steps passed: {passed}/{total}")
        print(f"Success rate: {passed/total*100:.1f}%")

        if passed == total:
            print("[SUCCESS] Complete flow test PASSED!")
            return True
        else:
            print("[ERROR] Complete flow test FAILED!")
            return False

def main():
    """Main function"""
    tester = CompleteFlowTester()
    success = tester.run_complete_flow()

    if success:
        print("\n[OK] Complete flow test completed successfully!")
        sys.exit(0)
    else:
        print("\n[ERROR] Complete flow test had failures!")
        sys.exit(1)

if __name__ == "__main__":
    main()
