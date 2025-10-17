"""
System Diagnostic - Check what's working and what's not
"""

import requests
import json

class SystemDiagnostic:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"
        self.token = None
        self.headers = {}
        self.results = {}
    
    def authenticate(self):
        """Test authentication"""
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", 
                                   json={"username": "test", "password": "test"})
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.headers = {"Authorization": f"Bearer {self.token}"}
                self.results['auth'] = {'status': 'PASS', 'message': 'Authentication working'}
                return True
            else:
                self.results['auth'] = {'status': 'FAIL', 'message': f'Status: {response.status_code}'}
                return False
        except Exception as e:
            self.results['auth'] = {'status': 'FAIL', 'message': f'Error: {str(e)}'}
            return False
    
    def test_core_apis(self):
        """Test core API endpoints"""
        endpoints = [
            ('/api/health', 'Health Check'),
            ('/api/whatsapp/status', 'WhatsApp Status'),
            ('/api/logs', 'Logs'),
            ('/api/help', 'Help System'),
            ('/api/sessions', 'Sessions'),
            ('/api/messages', 'Messages')
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
                if response.status_code == 200:
                    self.results[name] = {'status': 'PASS', 'message': 'Working'}
                else:
                    self.results[name] = {'status': 'FAIL', 'message': f'Status: {response.status_code}'}
            except Exception as e:
                self.results[name] = {'status': 'FAIL', 'message': f'Error: {str(e)}'}
    
    def test_hubspot_apis(self):
        """Test HubSpot API endpoints"""
        hubspot_endpoints = [
            ('/api/hubspot/contacts/contacts', 'Contacts API'),
            ('/api/hubspot/companies/companies', 'Companies API'),
            ('/api/hubspot/deals/deals', 'Deals API'),
            ('/api/hubspot/activities/calls', 'Calls API'),
            ('/api/hubspot/activities/meetings', 'Meetings API')
        ]
        
        for endpoint, name in hubspot_endpoints:
            try:
                # Test with a simple GET request
                response = requests.get(f"{self.base_url}{endpoint}?limit=1", headers=self.headers)
                if response.status_code == 200:
                    self.results[name] = {'status': 'PASS', 'message': 'HubSpot API working'}
                elif response.status_code == 401:
                    self.results[name] = {'status': 'FAIL', 'message': 'HubSpot token invalid'}
                else:
                    self.results[name] = {'status': 'FAIL', 'message': f'Status: {response.status_code}'}
            except Exception as e:
                self.results[name] = {'status': 'FAIL', 'message': f'Error: {str(e)}'}
    
    def test_database(self):
        """Test database operations"""
        try:
            response = requests.get(f"{self.base_url}/api/logs", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                log_count = data.get('total', 0)
                self.results['Database'] = {'status': 'PASS', 'message': f'{log_count} logs found'}
            else:
                self.results['Database'] = {'status': 'FAIL', 'message': f'Status: {response.status_code}'}
        except Exception as e:
            self.results['Database'] = {'status': 'FAIL', 'message': f'Error: {str(e)}'}
    
    def run_diagnostic(self):
        """Run complete system diagnostic"""
        print("System Diagnostic - HubSpot Logging AI Agent")
        print("=" * 60)
        
        # Test authentication first
        if not self.authenticate():
            print("[ERROR] Authentication failed! Cannot proceed with other tests.")
            return
        
        print("\n[TESTING] Core System Components...")
        self.test_core_apis()
        
        print("\n[TESTING] Database Operations...")
        self.test_database()
        
        print("\n[TESTING] HubSpot Integration...")
        self.test_hubspot_apis()
        
        # Display results
        print("\n" + "=" * 60)
        print("DIAGNOSTIC RESULTS")
        print("=" * 60)
        
        working = 0
        total = len(self.results)
        
        for component, result in self.results.items():
            status = result['status']
            message = result['message']
            
            if status == 'PASS':
                print(f"[OK] {component}: {message}")
                working += 1
            else:
                print(f"[ERROR] {component}: {message}")
        
        print(f"\n[SUMMARY] {working}/{total} components working ({working/total*100:.1f}%)")
        
        if working == total:
            print("\n[SUCCESS] ALL SYSTEMS OPERATIONAL!")
        elif working >= total * 0.8:
            print("\n[WARNING] MOSTLY WORKING - Minor issues detected")
        else:
            print("\n[CRITICAL] MAJOR ISSUES DETECTED - System needs attention")
        
        # Provide recommendations
        print("\n[RECOMMENDATIONS]")
        if 'HubSpot' in str(self.results.values()):
            print("• HubSpot integration failing - Get new PAT token")
            print("• Run: python check_hubspot_auth.py")
        if self.results.get('Database', {}).get('status') == 'PASS':
            print("• Database is working - Logging system operational")
        if self.results.get('auth', {}).get('status') == 'PASS':
            print("• Authentication is working - User system operational")
        
        return working, total

if __name__ == "__main__":
    diagnostic = SystemDiagnostic()
    diagnostic.run_diagnostic()
