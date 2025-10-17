#!/usr/bin/env python3
"""
Comprehensive HubSpot API Integration Tests

This script tests both:
1. Direct HubSpot API calls (using PAT from environment)
2. Our wrapper endpoints with additional logging layers

Usage:
    python tests/test_hubspot_integration.py [mode]

Modes:
    - direct: Test direct HubSpot API calls only
    - wrapper: Test our wrapper endpoints only
    - both: Test both (default)
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

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import create_app
from app.db.database import db
from app.models import User, ChatSession, ChatMessage, Log

# Configuration
BASE_URL = "http://89.117.63.196:5012"
HUBSPOT_BASE_URL = "https://api.hubapi.com"
HUBSPOT_TOKEN = os.getenv('HUBSPOT_ACCESS_TOKEN')

class HubSpotAPITester:
    """Test class for HubSpot API integration"""

    def __init__(self, mode='both'):
        self.mode = mode
        self.app = None
        self.test_user = None
        self.test_session = None
        self.test_message = None
        self.results = {
            'direct_api': {'passed': 0, 'failed': 0, 'tests': []},
            'wrapper_api': {'passed': 0, 'failed': 0, 'tests': []}
        }

    def setup_test_environment(self):
        """Set up test environment"""
        print("🔧 Setting up test environment...")

        # Create Flask app context for database operations
        self.app = create_app()
        with self.app.app_context():
            db.create_all()

            # Create test user
            self.test_user = User(
                name='API Test User',
                username='api_tester',
                password='testpass123',
                phone_number='+1234567890',
                hubspot_pat_token='test-token',
                email='api_test@example.com'
            )
            db.session.add(self.test_user)
            db.session.commit()

            # Create test session
            self.test_session = ChatSession(user_id=self.test_user.id)
            db.session.add(self.test_session)
            db.session.commit()

            # Create test message
            self.test_message = ChatMessage(
                session_id=self.test_session.id,
                message_text='Test message for HubSpot API integration testing'
            )
            db.session.add(self.test_message)
            db.session.commit()

        print(f"✅ Test user created: {self.test_user.username}")
        print(f"✅ Test session created: {self.test_session.id}")
        print(f"✅ Test message created: {self.test_message.id}")

    def get_auth_token(self):
        """Get authentication token for API calls"""
        login_data = {
            'username': 'api_tester',
            'password': 'testpass123'
        }

        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)

        if response.status_code == 200:
            return response.json()['token']
        else:
            print(f"❌ Failed to get auth token: {response.text}")
            return None

    def test_direct_hubspot_api(self):
        """Test direct HubSpot API calls"""
        print("\n🔗 Testing Direct HubSpot API Calls...")

        if not HUBSPOT_TOKEN:
            print("❌ HUBSPOT_ACCESS_TOKEN not found in environment")
            return False

        headers = {
            'Authorization': f'Bearer {HUBSPOT_TOKEN}',
            'Content-Type': 'application/json'
        }

        # Test 1: Get Contacts
        print("  📞 Testing GET contacts...")
        try:
            response = requests.get(f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts", headers=headers, params={'limit': 5})
            if response.status_code == 200:
                print("    ✅ GET contacts successful")
                self.results['direct_api']['passed'] += 1
                self.results['direct_api']['tests'].append({'name': 'GET contacts', 'status': 'PASS'})
            else:
                print(f"    ❌ GET contacts failed: {response.status_code}")
                self.results['direct_api']['failed'] += 1
                self.results['direct_api']['tests'].append({'name': 'GET contacts', 'status': 'FAIL', 'error': response.text})
        except Exception as e:
            print(f"    ❌ GET contacts error: {str(e)}")
            self.results['direct_api']['failed'] += 1
            self.results['direct_api']['tests'].append({'name': 'GET contacts', 'status': 'ERROR', 'error': str(e)})

        # Test 2: Get Deals
        print("  💰 Testing GET deals...")
        try:
            response = requests.get(f"{HUBSPOT_BASE_URL}/crm/v3/objects/deals", headers=headers, params={'limit': 5})
            if response.status_code == 200:
                print("    ✅ GET deals successful")
                self.results['direct_api']['passed'] += 1
                self.results['direct_api']['tests'].append({'name': 'GET deals', 'status': 'PASS'})
            else:
                print(f"    ❌ GET deals failed: {response.status_code}")
                self.results['direct_api']['failed'] += 1
                self.results['direct_api']['tests'].append({'name': 'GET deals', 'status': 'FAIL', 'error': response.text})
        except Exception as e:
            print(f"    ❌ GET deals error: {str(e)}")
            self.results['direct_api']['failed'] += 1
            self.results['direct_api']['tests'].append({'name': 'GET deals', 'status': 'ERROR', 'error': str(e)})

        # Test 3: Create Contact
        print("  👤 Testing POST contact...")
        try:
            timestamp = int(time.time())
            contact_data = {
                'properties': {
                    'email': f'test-{timestamp}@example.com',
                    'firstname': 'Test',
                    'lastname': 'Contact'
                }
            }

            response = requests.post(f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts", headers=headers, json=contact_data)

            if response.status_code in [200, 201]:
                print("    ✅ POST contact successful")
                self.results['direct_api']['passed'] += 1
                self.results['direct_api']['tests'].append({'name': 'POST contact', 'status': 'PASS'})

                # Clean up - delete the test contact
                contact_id = response.json().get('id')
                if contact_id:
                    delete_response = requests.delete(f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/{contact_id}", headers=headers)
                    if delete_response.status_code == 204:
                        print("    🗑️ Test contact cleaned up")
            else:
                print(f"    ❌ POST contact failed: {response.status_code}")
                self.results['direct_api']['failed'] += 1
                self.results['direct_api']['tests'].append({'name': 'POST contact', 'status': 'FAIL', 'error': response.text})
        except Exception as e:
            print(f"    ❌ POST contact error: {str(e)}")
            self.results['direct_api']['failed'] += 1
            self.results['direct_api']['tests'].append({'name': 'POST contact', 'status': 'ERROR', 'error': str(e)})

        # Test 4: Get Contact Properties
        print("  📋 Testing GET contact properties...")
        try:
            response = requests.get(f"{HUBSPOT_BASE_URL}/crm/v3/properties/contacts", headers=headers, params={'limit': 5})
            if response.status_code == 200:
                print("    ✅ GET contact properties successful")
                self.results['direct_api']['passed'] += 1
                self.results['direct_api']['tests'].append({'name': 'GET contact properties', 'status': 'PASS'})
            else:
                print(f"    ❌ GET contact properties failed: {response.status_code}")
                self.results['direct_api']['failed'] += 1
                self.results['direct_api']['tests'].append({'name': 'GET contact properties', 'status': 'FAIL', 'error': response.text})
        except Exception as e:
            print(f"    ❌ GET contact properties error: {str(e)}")
            self.results['direct_api']['failed'] += 1
            self.results['direct_api']['tests'].append({'name': 'GET contact properties', 'status': 'ERROR', 'error': str(e)})

    def test_wrapper_endpoints(self):
        """Test our wrapper endpoints with additional logging"""
        print("\n🔄 Testing Wrapper Endpoints with Additional Layers...")

        token = self.get_auth_token()
        if not token:
            print("❌ Cannot test wrapper endpoints - no auth token")
            return

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # Test 1: Health Check
        print("  [HEALTH] Testing health check...")
        try:
            response = client.get('/api/health', headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    print("    [OK] Health check successful")
                    self.results['wrapper_api']['passed'] += 1
                    self.results['wrapper_api']['tests'].append({'name': 'Health check', 'status': 'PASS'})
                else:
                    print(f"    [ERROR] Health check unhealthy: {data}")
                    self.results['wrapper_api']['failed'] += 1
                    self.results['wrapper_api']['tests'].append({'name': 'Health check', 'status': 'FAIL', 'error': data})
            else:
                print(f"    [ERROR] Health check failed: {response.status_code}")
                self.results['wrapper_api']['failed'] += 1
                self.results['wrapper_api']['tests'].append({'name': 'Health check', 'status': 'FAIL', 'error': response.text})
        except Exception as e:
            print(f"    [ERROR] Health check error: {str(e)}")
            self.results['wrapper_api']['failed'] += 1
            self.results['wrapper_api']['tests'].append({'name': 'Health check', 'status': 'ERROR', 'error': str(e)})

        # Test 2: HubSpot Connection Test
        print("  [CONNECTION] Testing HubSpot connection...")
        try:
            response = client.get('/api/hubspot/test-connection', headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('connected'):
                    print("    [OK] HubSpot connection test successful")
                    self.results['wrapper_api']['passed'] += 1
                    self.results['wrapper_api']['tests'].append({'name': 'HubSpot connection test', 'status': 'PASS'})
                else:
                    print(f"    [ERROR] HubSpot connection test failed: {data}")
                    self.results['wrapper_api']['failed'] += 1
                    self.results['wrapper_api']['tests'].append({'name': 'HubSpot connection test', 'status': 'FAIL', 'error': data})
            else:
                print(f"    [ERROR] HubSpot connection test failed: {response.status_code}")
                self.results['wrapper_api']['failed'] += 1
                self.results['wrapper_api']['tests'].append({'name': 'HubSpot connection test', 'status': 'FAIL', 'error': response.text})
        except Exception as e:
            print(f"    [ERROR] HubSpot connection test error: {str(e)}")
            self.results['wrapper_api']['failed'] += 1
            self.results['wrapper_api']['tests'].append({'name': 'HubSpot connection test', 'status': 'ERROR', 'error': str(e)})

        # Test 3: Create Contact via Wrapper (with logging)
        print("  [CONTACT] Testing POST contact via wrapper...")
        try:
            timestamp = int(time.time())
            contact_data = {
                'session_id': self.test_session.id,
                'chat_message_id': self.test_message.id,
                'properties': {
                    'email': f'wrapper-test-{timestamp}@example.com',
                    'firstname': 'Wrapper',
                    'lastname': 'Test'
                }
            }

            response = client.post('/api/hubspot/contacts', headers=headers, json=contact_data)

            if response.status_code == 201:
                data = response.json()
                if data.get('sync_status') == 'synced':
                    print("    [OK] POST contact via wrapper successful")
                    self.results['wrapper_api']['passed'] += 1
                    self.results['wrapper_api']['tests'].append({'name': 'POST contact via wrapper', 'status': 'PASS'})

                    # Verify log was created in our database
                    with self.app.app_context():
                        logs = Log.query.filter_by(
                            session_id=self.test_session.id,
                            chat_message_id=self.test_message.id,
                            log_type='contact_action'
                        ).all()

                        if logs:
                            print(f"    [OK] Log created in database: {len(logs)} log(s)")
                        else:
                            print("    [WARNING] No logs found in database")
                else:
                    print(f"    [ERROR] POST contact via wrapper not synced: {data}")
                    self.results['wrapper_api']['failed'] += 1
                    self.results['wrapper_api']['tests'].append({'name': 'POST contact via wrapper', 'status': 'FAIL', 'error': data})
            else:
                print(f"    [ERROR] POST contact via wrapper failed: {response.status_code}")
                self.results['wrapper_api']['failed'] += 1
                self.results['wrapper_api']['tests'].append({'name': 'POST contact via wrapper', 'status': 'FAIL', 'error': response.text})
        except Exception as e:
            print(f"    [ERROR] POST contact via wrapper error: {str(e)}")
            self.results['wrapper_api']['failed'] += 1
            self.results['wrapper_api']['tests'].append({'name': 'POST contact via wrapper', 'status': 'ERROR', 'error': str(e)})

        # Test 4: Get Logs (our database logs)
        print("  [LOGS] Testing GET logs...")
        try:
            response = client.get('/api/logs', headers=headers, query_string={'limit': 10})

            if response.status_code == 200:
                data = response.json()
                logs = data.get('logs', [])
                print(f"    [OK] GET logs successful - found {len(logs)} logs")

                # Check if our test log is there
                test_logs = [log for log in logs if log.get('session_id') == self.test_session.id]
                if test_logs:
                    print(f"    [OK] Found our test logs: {len(test_logs)}")

                self.results['wrapper_api']['passed'] += 1
                self.results['wrapper_api']['tests'].append({'name': 'GET logs', 'status': 'PASS'})
            else:
                print(f"    [ERROR] GET logs failed: {response.status_code}")
                self.results['wrapper_api']['failed'] += 1
                self.results['wrapper_api']['tests'].append({'name': 'GET logs', 'status': 'FAIL', 'error': response.text})
        except Exception as e:
            print(f"    [ERROR] GET logs error: {str(e)}")
            self.results['wrapper_api']['failed'] += 1
            self.results['wrapper_api']['tests'].append({'name': 'GET logs', 'status': 'ERROR', 'error': str(e)})

        # Test 5: Get HubSpot Data via Wrapper
        print("  [STATS] Testing GET HubSpot data via wrapper...")
        try:
            response = client.get('/api/hubspot/contacts', headers=headers, query_string={'limit': 5})

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                print(f"    [OK] GET contacts via wrapper successful - found {len(results)} contacts")

                self.results['wrapper_api']['passed'] += 1
                self.results['wrapper_api']['tests'].append({'name': 'GET contacts via wrapper', 'status': 'PASS'})
            else:
                print(f"    [ERROR] GET contacts via wrapper failed: {response.status_code}")
                self.results['wrapper_api']['failed'] += 1
                self.results['wrapper_api']['tests'].append({'name': 'GET contacts via wrapper', 'status': 'FAIL', 'error': response.text})
        except Exception as e:
            print(f"    [ERROR] GET contacts via wrapper error: {str(e)}")
            self.results['wrapper_api']['failed'] += 1
            self.results['wrapper_api']['tests'].append({'name': 'GET contacts via wrapper', 'status': 'ERROR', 'error': str(e)})

    def run_tests(self):
        """Run all tests"""
        print("Starting HubSpot API Integration Tests")
        print(f"Mode: {self.mode}")
        print("=" * 60)

        # Setup test environment
        self.setup_test_environment()

        # Run tests based on mode
        if self.mode in ['direct', 'both']:
            self.test_direct_hubspot_api()

        if self.mode in ['wrapper', 'both']:
            self.test_wrapper_endpoints()

        # Print results
        self.print_results()

        return self.results

    def print_results(self):
        """Print test results"""
        print("\n" + "=" * 60)
        print("[STATS] TEST RESULTS")
        print("=" * 60)

        for test_type in ['direct_api', 'wrapper_api']:
            if self.mode in [test_type.split('_')[0], 'both']:
                results = self.results[test_type]
                total = results['passed'] + results['failed']

                print(f"\n{test_type.upper().replace('_', ' ')}:")
                print(f"  Passed: {results['passed']}")
                print(f"  Failed: {results['failed']}")
                print(f"  Total: {total}")
                print(f"  Success Rate: {results['passed']/total*100:.1f}%" if total > 0 else "  Success Rate: N/A")

                # Show failed tests
                failed_tests = [test for test in results['tests'] if test['status'] in ['FAIL', 'ERROR']]
                if failed_tests:
                    print("  Failed Tests:")
                    for test in failed_tests:
                        print(f"    [ERROR] {test['name']}: {test.get('error', 'Unknown error')}")

def main():
    """Main function"""
    mode = 'both'

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

    if mode not in ['direct', 'wrapper', 'both']:
        print("Invalid mode. Use: direct, wrapper, or both")
        sys.exit(1)

    tester = HubSpotAPITester(mode)
    results = tester.run_tests()

    # Exit with appropriate code
    total_failed = results['direct_api']['failed'] + results['wrapper_api']['failed']
    if total_failed > 0:
        print(f"\n[ERROR] {total_failed} test(s) failed")
        sys.exit(1)
    else:
        print("\n[OK] All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
