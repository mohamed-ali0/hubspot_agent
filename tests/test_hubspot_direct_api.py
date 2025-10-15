#!/usr/bin/env python3
"""
Direct HubSpot API Test Script

This script tests the HubSpot APIs directly using the PAT from environment,
exactly as shown in the Postman collection provided.

Usage:
    python tests/test_hubspot_direct_api.py
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

class HubSpotDirectAPITester:
    """Test class for direct HubSpot API calls"""

    def __init__(self):
        self.base_url = "https://api.hubapi.com"
        self.token = os.getenv('HUBSPOT_ACCESS_TOKEN')
        self.results = {'passed': 0, 'failed': 0, 'tests': []}

    def test_headers(self):
        """Test basic API connectivity"""
        if not self.token:
            print("[ERROR] HUBSPOT_ACCESS_TOKEN not found in environment")
            return False

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        print("[CONNECTION] Testing HubSpot API connectivity...")
        print(f"Token: {self.token[:20]}...")  # Show first 20 chars for verification

        return headers

    def test_get_contacts(self):
        """Test GET contacts endpoint"""
        print("\n[CONTACTS] Testing GET contacts...")

        headers = self.test_headers()
        if not headers:
            return False

        try:
            response = requests.get(
                f"{self.base_url}/crm/v3/objects/contacts",
                headers=headers,
                params={'limit': 5}
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                print(f"[OK] GET contacts successful - found {len(results)} contacts")

                # Show sample contact
                if results:
                    contact = results[0]
                    properties = contact.get('properties', {})
                    print(f"   Sample contact: {properties.get('firstname', 'N/A')} {properties.get('lastname', 'N/A')}")

                self.results['passed'] += 1
                self.results['tests'].append({'name': 'GET contacts', 'status': 'PASS'})
                return True
            else:
                print(f"[ERROR] GET contacts failed: {response.status_code} - {response.text}")
                self.results['failed'] += 1
                self.results['tests'].append({'name': 'GET contacts', 'status': 'FAIL', 'error': response.text})
                return False

        except Exception as e:
            print(f"[ERROR] GET contacts error: {str(e)}")
            self.results['failed'] += 1
            self.results['tests'].append({'name': 'GET contacts', 'status': 'ERROR', 'error': str(e)})
            return False

    def test_get_deals(self):
        """Test GET deals endpoint"""
        print("\n[DEALS] Testing GET deals...")

        headers = self.test_headers()
        if not headers:
            return False

        try:
            response = requests.get(
                f"{self.base_url}/crm/v3/objects/deals",
                headers=headers,
                params={'limit': 5}
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                print(f"[OK] GET deals successful - found {len(results)} deals")

                # Show sample deal
                if results:
                    deal = results[0]
                    properties = deal.get('properties', {})
                    print(f"   Sample deal: {properties.get('dealname', 'N/A')} - ${properties.get('amount', 'N/A')}")

                self.results['passed'] += 1
                self.results['tests'].append({'name': 'GET deals', 'status': 'PASS'})
                return True
            else:
                print(f"[ERROR] GET deals failed: {response.status_code} - {response.text}")
                self.results['failed'] += 1
                self.results['tests'].append({'name': 'GET deals', 'status': 'FAIL', 'error': response.text})
                return False

        except Exception as e:
            print(f"[ERROR] GET deals error: {str(e)}")
            self.results['failed'] += 1
            self.results['tests'].append({'name': 'GET deals', 'status': 'ERROR', 'error': str(e)})
            return False

    def test_create_contact(self):
        """Test POST contact creation"""
        print("\n[CONTACT] Testing POST contact creation...")

        headers = self.test_headers()
        if not headers:
            return False

        try:
            timestamp = int(time.time())
            contact_data = {
                'properties': {
                    'email': f'test-{timestamp}@example.com',
                    'firstname': 'Test',
                    'lastname': 'Contact'
                }
            }

            response = requests.post(
                f"{self.base_url}/crm/v3/objects/contacts",
                headers=headers,
                json=contact_data
            )

            if response.status_code in [200, 201]:
                data = response.json()
                contact_id = data.get('id')
                print(f"[OK] POST contact successful - ID: {contact_id}")

                # Clean up - delete the test contact
                if contact_id:
                    delete_response = requests.delete(
                        f"{self.base_url}/crm/v3/objects/contacts/{contact_id}",
                        headers=headers
                    )
                    if delete_response.status_code == 204:
                        print("   [CLEANUP] Test contact cleaned up")
                    else:
                        print(f"   [WARNING] Failed to clean up contact: {delete_response.status_code}")

                self.results['passed'] += 1
                self.results['tests'].append({'name': 'POST contact', 'status': 'PASS'})
                return True
            else:
                print(f"[ERROR] POST contact failed: {response.status_code} - {response.text}")
                self.results['failed'] += 1
                self.results['tests'].append({'name': 'POST contact', 'status': 'FAIL', 'error': response.text})
                return False

        except Exception as e:
            print(f"[ERROR] POST contact error: {str(e)}")
            self.results['failed'] += 1
            self.results['tests'].append({'name': 'POST contact', 'status': 'ERROR', 'error': str(e)})
            return False

    def test_get_contact_properties(self):
        """Test GET contact properties"""
        print("\n[PROPERTIES] Testing GET contact properties...")

        headers = self.test_headers()
        if not headers:
            return False

        try:
            response = requests.get(
                f"{self.base_url}/crm/v3/properties/contacts",
                headers=headers,
                params={'limit': 5}
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                print(f"[OK] GET contact properties successful - found {len(results)} properties")

                # Show sample property
                if results:
                    prop = results[0]
                    print(f"   Sample property: {prop.get('name', 'N/A')} - {prop.get('label', 'N/A')}")

                self.results['passed'] += 1
                self.results['tests'].append({'name': 'GET contact properties', 'status': 'PASS'})
                return True
            else:
                print(f"[ERROR] GET contact properties failed: {response.status_code} - {response.text}")
                self.results['failed'] += 1
                self.results['tests'].append({'name': 'GET contact properties', 'status': 'FAIL', 'error': response.text})
                return False

        except Exception as e:
            print(f"[ERROR] GET contact properties error: {str(e)}")
            self.results['failed'] += 1
            self.results['tests'].append({'name': 'GET contact properties', 'status': 'ERROR', 'error': str(e)})
            return False

    def test_get_notes(self):
        """Test GET notes endpoint"""
        print("\n[NOTES] Testing GET notes...")

        headers = self.test_headers()
        if not headers:
            return False

        try:
            response = requests.get(
                f"{self.base_url}/crm/v3/objects/notes",
                headers=headers,
                params={'limit': 5}
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                print(f"[OK] GET notes successful - found {len(results)} notes")

                # Show sample note
                if results:
                    note = results[0]
                    properties = note.get('properties', {})
                    note_body = properties.get('hs_note_body', 'N/A')
                    # Handle Unicode characters that might cause encoding issues
                    try:
                        safe_note_body = note_body[:50] if note_body else 'N/A'
                        print(f"   Sample note: {safe_note_body}...")
                    except UnicodeEncodeError:
                        print("   Sample note: [Note content with special characters]...")

                self.results['passed'] += 1
                self.results['tests'].append({'name': 'GET notes', 'status': 'PASS'})
                return True
            else:
                print(f"[ERROR] GET notes failed: {response.status_code} - {response.text}")
                self.results['failed'] += 1
                self.results['tests'].append({'name': 'GET notes', 'status': 'FAIL', 'error': response.text})
                return False

        except Exception as e:
            print(f"[ERROR] GET notes error: {str(e)}")
            self.results['failed'] += 1
            self.results['tests'].append({'name': 'GET notes', 'status': 'ERROR', 'error': str(e)})
            return False

    def test_create_note(self):
        """Test POST note creation"""
        print("\n[NOTES] Testing POST note creation...")

        headers = self.test_headers()
        if not headers:
            return False

        try:
            timestamp = int(time.time())
            note_data = {
                'properties': {
                    'hs_note_body': f'Test note created at {timestamp} - This is a properly formatted note for API testing.',
                    'hs_timestamp': timestamp
                }
            }

            response = requests.post(
                f"{self.base_url}/crm/v3/objects/notes",
                headers=headers,
                json=note_data
            )

            if response.status_code in [200, 201]:
                data = response.json()
                note_id = data.get('id')
                print(f"[OK] POST note successful - ID: {note_id}")

                # Clean up - delete the test note
                if note_id:
                    delete_response = requests.delete(
                        f"{self.base_url}/crm/v3/objects/notes/{note_id}",
                        headers=headers
                    )
                    if delete_response.status_code == 204:
                        print("   [CLEANUP] Test note cleaned up")
                    else:
                        print(f"   [WARNING] Failed to clean up note: {delete_response.status_code}")

                self.results['passed'] += 1
                self.results['tests'].append({'name': 'POST note', 'status': 'PASS'})
                return True
            else:
                print(f"[ERROR] POST note failed: {response.status_code} - {response.text}")
                self.results['failed'] += 1
                self.results['tests'].append({'name': 'POST note', 'status': 'FAIL', 'error': response.text})
                return False

        except Exception as e:
            print(f"[ERROR] POST note error: {str(e)}")
            self.results['failed'] += 1
            self.results['tests'].append({'name': 'POST note', 'status': 'ERROR', 'error': str(e)})
            return False

    def test_get_tasks(self):
        """Test GET tasks endpoint"""
        print("\n[TASKS] Testing GET tasks...")

        headers = self.test_headers()
        if not headers:
            return False

        try:
            response = requests.get(
                f"{self.base_url}/crm/v3/objects/tasks",
                headers=headers,
                params={'limit': 5}
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                print(f"[OK] GET tasks successful - found {len(results)} tasks")

                # Show sample task
                if results:
                    task = results[0]
                    properties = task.get('properties', {})
                    task_subject = properties.get('hs_task_subject', 'N/A')
                    # Handle Unicode characters that might cause encoding issues
                    try:
                        print(f"   Sample task: {task_subject}")
                    except UnicodeEncodeError:
                        print("   Sample task: [Task with special characters]")

                self.results['passed'] += 1
                self.results['tests'].append({'name': 'GET tasks', 'status': 'PASS'})
                return True
            else:
                print(f"[ERROR] GET tasks failed: {response.status_code} - {response.text}")
                self.results['failed'] += 1
                self.results['tests'].append({'name': 'GET tasks', 'status': 'FAIL', 'error': response.text})
                return False

        except Exception as e:
            print(f"[ERROR] GET tasks error: {str(e)}")
            self.results['failed'] += 1
            self.results['tests'].append({'name': 'GET tasks', 'status': 'ERROR', 'error': str(e)})
            return False

    def run_all_tests(self):
        """Run all HubSpot API tests"""
        print("Starting Direct HubSpot API Tests")
        print(f"Base URL: {self.base_url}")
        print("=" * 60)

        # Run all test methods
        test_methods = [
            self.test_get_contacts,
            self.test_get_deals,
            self.test_create_contact,
            self.test_get_contact_properties,
            self.test_get_notes,
            self.test_create_note,
            self.test_get_tasks
        ]

        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                print(f"[ERROR] Test method {test_method.__name__} failed with exception: {str(e)}")

        # Print results
        self.print_results()

    def print_results(self):
        """Print test results"""
        print("\n" + "=" * 60)
        print("[STATS] DIRECT HUBSPOT API TEST RESULTS")
        print("=" * 60)
        print(f"Passed: {self.results['passed']}")
        print(f"Failed: {self.results['failed']}")
        total = self.results['passed'] + self.results['failed']
        print(f"Total: {total}")
        if total > 0:
            print(f"Success Rate: {self.results['passed']/total*100:.1f}%")

        # Show failed tests
        failed_tests = [test for test in self.results['tests'] if test['status'] in ['FAIL', 'ERROR']]
        if failed_tests:
            print("\n[ERROR] Failed Tests:")
            for test in failed_tests:
                print(f"  {test['name']}: {test.get('error', 'Unknown error')}")

def main():
    """Main function"""
    tester = HubSpotDirectAPITester()
    tester.run_all_tests()

    if tester.results['failed'] > 0:
        print(f"\n[ERROR] {tester.results['failed']} test(s) failed")
        sys.exit(1)
    else:
        print("\n[OK] All direct HubSpot API tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
