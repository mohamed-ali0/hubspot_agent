#!/usr/bin/env python3
"""
Test script to fix HubSpot API issues
"""

import os
import sys
import requests
import json
from datetime import datetime

# Set environment variables (use actual token from environment)
hubspot_token = os.getenv('HUBSPOT_ACCESS_TOKEN')
if not hubspot_token:
    print("ERROR: HUBSPOT_ACCESS_TOKEN not found in environment variables")
    print("Please set HUBSPOT_ACCESS_TOKEN environment variable")
    exit(1)

os.environ['HUBSPOT_ACCESS_TOKEN'] = hubspot_token
os.environ['HUBSPOT_API_URL'] = 'https://api.hubapi.com'

def test_hubspot_direct():
    """Test HubSpot API directly"""
    print("Testing HubSpot API directly...")
    
    headers = {
        'Authorization': f'Bearer {os.environ["HUBSPOT_ACCESS_TOKEN"]}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Test contacts
        response = requests.get(
            'https://api.hubapi.com/crm/v3/objects/contacts?limit=5',
            headers=headers
        )
        print(f"Direct HubSpot Contacts: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data.get('results', []))} contacts")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Direct API Error: {e}")

def test_flask_endpoints():
    """Test Flask endpoints"""
    print("\nTesting Flask endpoints...")
    
    base_url = "http://localhost:5000"
    
    try:
        # Test health
        response = requests.get(f"{base_url}/api/health")
        print(f"Health: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"HubSpot API status: {data.get('hubspot_api', 'unknown')}")
        
        # Test new contacts endpoint
        response = requests.get(f"{base_url}/api/hubspot/contacts/")
        print(f"New Contacts endpoint: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
            
        # Test legacy contacts endpoint
        response = requests.get(f"{base_url}/api/hubspot/contacts")
        print(f"Legacy Contacts endpoint: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Flask API Error: {e}")

if __name__ == "__main__":
    print("HubSpot API Fix Test")
    print("=" * 50)
    
    test_hubspot_direct()
    test_flask_endpoints()
    
    print("\nTest completed!")
