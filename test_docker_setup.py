"""
Test script to verify Docker setup
"""

import requests
import time
import subprocess
import sys

def test_docker_build():
    """Test if Docker can build the image"""
    print("Testing Docker build...")
    try:
        result = subprocess.run(['docker', 'build', '-t', 'hubspot-agent', '.'], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("[OK] Docker build successful")
            return True
        else:
            print(f"[ERROR] Docker build failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("[ERROR] Docker build timed out")
        return False
    except FileNotFoundError:
        print("[ERROR] Docker not found. Please install Docker first.")
        return False

def test_docker_run():
    """Test if Docker can run the container"""
    print("Testing Docker run...")
    try:
        # Stop and remove existing container if it exists
        subprocess.run(['docker', 'stop', 'hubspot-agent'], capture_output=True)
        subprocess.run(['docker', 'rm', 'hubspot-agent'], capture_output=True)
        
        # Run the container
        result = subprocess.run([
            'docker', 'run', '-d',
            '--name', 'hubspot-agent',
            '-p', '5012:5012',
            '-e', 'SECRET_KEY=test-secret',
            '-e', 'DATABASE_URL=sqlite:///data/database.db',
            '-e', 'JWT_SECRET_KEY=test-jwt-secret',
            '-e', 'HUBSPOT_ACCESS_TOKEN=test-token',
            'hubspot-agent'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[OK] Docker container started")
            return True
        else:
            print(f"[ERROR] Docker run failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Docker run error: {e}")
        return False

def test_health_endpoint():
    """Test if the health endpoint responds"""
    print("Testing health endpoint...")
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get('http://localhost:5012/api/health', timeout=5)
            if response.status_code == 200:
                print("[OK] Health endpoint responding")
                return True
        except requests.exceptions.RequestException:
            if i < max_retries - 1:
                print(f"Waiting for app to start... ({i+1}/{max_retries})")
                time.sleep(5)
            else:
                print("[ERROR] Health endpoint not responding")
                return False
    return False

def cleanup():
    """Clean up Docker container"""
    print("Cleaning up...")
    subprocess.run(['docker', 'stop', 'hubspot-agent'], capture_output=True)
    subprocess.run(['docker', 'rm', 'hubspot-agent'], capture_output=True)
    print("[OK] Cleanup completed")

def main():
    """Run all Docker tests"""
    print("Docker Setup Test Suite")
    print("=" * 50)
    
    tests = [
        ("Docker Build", test_docker_build),
        ("Docker Run", test_docker_run),
        ("Health Endpoint", test_health_endpoint)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        else:
            print(f"[FAILED] {test_name} failed")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} passed")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("[SUCCESS] Docker setup is working correctly!")
    else:
        print("[WARNING] Some tests failed. Check Docker installation and configuration.")
    
    # Cleanup
    cleanup()

if __name__ == "__main__":
    main()
