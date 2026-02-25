#!/usr/bin/env python
"""
Browser Test Runner for Yuno KYB System
========================================

This script runs Selenium browser tests and generates an HTML report.

Usage:
    python run_browser_tests.py

Requirements:
    - Django server running on http://127.0.0.1:8000
    - Chrome browser installed
    - Dependencies: selenium, pytest, pytest-html, webdriver-manager

The script will:
    1. Check if the server is running
    2. Run all browser tests
    3. Generate HTML report in reports/test_report.html
    4. Open the report in browser
"""

import os
import sys
import subprocess
import time
import webbrowser
import requests

# Configuration
SERVER_URL = "http://127.0.0.1:8000"
REPORT_PATH = "reports/test_report.html"


def check_server():
    """Check if Django server is running."""
    print("🔍 Checking if server is running...")
    try:
        response = requests.get(SERVER_URL, timeout=5)
        if response.status_code == 200:
            print(f"✅ Server is running at {SERVER_URL}")
            return True
    except requests.exceptions.RequestException:
        pass

    print(f"❌ Server is not running at {SERVER_URL}")
    return False


def start_server():
    """Start Django development server in background."""
    print("🚀 Starting Django server...")

    # Activate virtualenv and run server
    if sys.platform == "win32":
        cmd = "venv\\Scripts\\activate && python manage.py runserver"
    else:
        cmd = "source venv/bin/activate && python manage.py runserver"

    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait for server to start
    for i in range(10):
        time.sleep(1)
        if check_server():
            return process

    print("❌ Failed to start server")
    return None


def run_tests():
    """Run pytest browser tests."""
    print("\n" + "=" * 60)
    print("🧪 RUNNING BROWSER TESTS")
    print("=" * 60 + "\n")

    # Create reports directory
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)

    # Run pytest
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/browser_tests.py",
        "-v",
        "--html=reports/test_report.html",
        "--self-contained-html",
        "--tb=short",
    ])

    return result.returncode


def open_report():
    """Open the HTML report in browser."""
    report_path = os.path.abspath(REPORT_PATH)
    if os.path.exists(report_path):
        print(f"\n📊 Opening report: {report_path}")
        webbrowser.open(f"file://{report_path}")
    else:
        print(f"\n❌ Report not found: {report_path}")


def main():
    """Main entry point."""
    print("\n" + "=" * 60)
    print("🔬 YUNO KYB BROWSER TEST RUNNER")
    print("=" * 60)

    # Check server
    server_process = None
    if not check_server():
        print("\n⚠️  Server not running. Please start it with:")
        print("    source venv/bin/activate && python manage.py runserver")
        print("\nOr press Enter to attempt auto-start...")
        input()

        server_process = start_server()
        if not server_process:
            print("Cannot proceed without server running.")
            sys.exit(1)

    # Run tests
    try:
        exit_code = run_tests()

        print("\n" + "=" * 60)
        if exit_code == 0:
            print("✅ ALL TESTS PASSED")
        else:
            print("❌ SOME TESTS FAILED")
        print("=" * 60)

        # Open report
        open_report()

        sys.exit(exit_code)

    finally:
        # Cleanup
        if server_process:
            print("\n🛑 Stopping server...")
            server_process.terminate()


if __name__ == "__main__":
    main()
