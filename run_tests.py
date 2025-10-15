#!/usr/bin/env python3
"""
Test Runner for HubSpot Logging API

This script starts the API server and runs the test suite against it.
"""

import os
import sys
import time
import threading
import subprocess
from pathlib import Path

def start_server():
    """Start the Flask API server in a separate thread"""
    print("[SERVER] Starting API server...")

    # Set environment variables
    env = os.environ.copy()
    env['FLASK_APP'] = 'app.main:app'
    env['FLASK_ENV'] = 'testing'

    # Start the server
    try:
        process = subprocess.Popen(
            [sys.executable, '-m', 'flask', 'run', '--host=127.0.0.1', '--port=5000'],
            env=env,
            cwd=Path.cwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait a bit for server to start
        time.sleep(3)

        if process.poll() is None:
            print("[OK] API server started successfully")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"[ERROR] Failed to start server: {stderr.decode()}")
            return None

    except Exception as e:
        print(f"[ERROR] Error starting server: {str(e)}")
        return None

def run_tests():
    """Run the test suite"""
    print("\n[TESTS] Running test suite...")

    try:
        # Run the complete flow test
        result = subprocess.run([
            sys.executable, 'tests/test_complete_flow.py'
        ], cwd=Path.cwd(), capture_output=True, text=True)

        print("Test output:")
        print(result.stdout)

        if result.stderr:
            print("Test errors:")
            print(result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"[ERROR] Error running tests: {str(e)}")
        return False

def main():
    """Main test runner"""
    print("[TOOLS] HubSpot Logging API Test Runner")
    print("=" * 50)

    # Start the server
    server_process = start_server()

    if not server_process:
        print("[ERROR] Cannot run tests without server")
        sys.exit(1)

    try:
        # Run tests
        tests_passed = run_tests()

        if tests_passed:
            print("\n[SUCCESS] All tests passed!")
            sys.exit(0)
        else:
            print("\n[ERROR] Some tests failed!")
            sys.exit(1)

    finally:
        # Clean up - stop the server
        print("\n[SHUTDOWN] Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("[OK] Server stopped")

if __name__ == "__main__":
    main()
