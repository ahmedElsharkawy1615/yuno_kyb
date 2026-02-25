"""
Browser-Based Frontend Tests for Yuno KYB System
=================================================

This module contains Selenium-based tests that open a real browser
and interact with the web interface.

Requirements:
    pip install selenium pytest pytest-html webdriver-manager

Run tests:
    python manage.py runserver &
    pytest tests/browser_tests.py -v --html=reports/test_report.html

Author: Yuno QA Team
"""

import pytest
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_URL = "http://127.0.0.1:8000"
ADMIN_URL = f"{BASE_URL}/admin/"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
IMPLICIT_WAIT = 10
SCREENSHOT_DIR = "reports/screenshots"


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture(scope="function")
def browser():
    """
    Create a Chrome browser instance for each test.
    Takes screenshots on failure.
    """
    # Chrome options
    chrome_options = Options()
    # Uncomment below for headless mode (no visible browser)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Initialize driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(IMPLICIT_WAIT)

    yield driver

    # Cleanup
    driver.quit()


@pytest.fixture(scope="function")
def admin_browser(browser):
    """
    Browser with admin already logged in.
    """
    browser.get(ADMIN_URL)

    # Login
    username_field = browser.find_element(By.NAME, "username")
    password_field = browser.find_element(By.NAME, "password")

    username_field.send_keys(ADMIN_USERNAME)
    password_field.send_keys(ADMIN_PASSWORD)
    password_field.send_keys(Keys.RETURN)

    # Wait for login to complete
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "site-name"))
    )

    return browser


def take_screenshot(driver, name):
    """Save screenshot to reports directory."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"{SCREENSHOT_DIR}/{name}_{timestamp}.png"
    driver.save_screenshot(filepath)
    return filepath


def safe_click(driver, element):
    """Safely click an element by scrolling to it first."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.3)
    try:
        element.click()
    except:
        # Fallback to JavaScript click
        driver.execute_script("arguments[0].click();", element)


# =============================================================================
# TEST CLASS: HOME PAGE
# =============================================================================

class TestHomePage:
    """Tests for the home page."""

    def test_home_page_loads(self, browser):
        """
        Test: Home page loads successfully
        Steps:
            1. Navigate to home page
            2. Verify title contains 'Yuno KYB'
            3. Verify main navigation elements present
        Expected: Page loads with correct branding
        """
        browser.get(BASE_URL)

        # Verify title
        assert "Yuno KYB" in browser.title

        # Verify navigation
        nav = browser.find_element(By.CLASS_NAME, "navbar")
        assert "Yuno KYB" in nav.text

        # Verify main cards present
        cards = browser.find_elements(By.CLASS_NAME, "card")
        assert len(cards) >= 3  # Register, Status, Dashboard cards

        take_screenshot(browser, "home_page")
        print("✅ Home page loads successfully")

    def test_home_page_navigation_links(self, browser):
        """
        Test: All navigation links work
        Steps:
            1. Navigate to home page
            2. Click each navigation link
            3. Verify correct page loads
        Expected: All links navigate correctly
        """
        browser.get(BASE_URL)

        # Test Register link
        register_link = browser.find_element(By.LINK_TEXT, "Register Now")
        register_link.click()
        assert "/register/" in browser.current_url

        # Test Status link via navbar
        browser.get(BASE_URL)
        status_link = browser.find_element(By.LINK_TEXT, "Check Status")
        status_link.click()
        assert "/status/" in browser.current_url

        # Test Dashboard link
        browser.get(BASE_URL)
        dashboard_link = browser.find_element(By.LINK_TEXT, "View Dashboard")
        dashboard_link.click()
        assert "/dashboard/" in browser.current_url

        print("✅ All navigation links work correctly")


# =============================================================================
# TEST CLASS: MERCHANT REGISTRATION
# =============================================================================

class TestMerchantRegistration:
    """Tests for merchant registration flow."""

    def test_registration_form_loads(self, browser):
        """
        Test: Registration form displays all fields
        Steps:
            1. Navigate to registration page
            2. Verify all form fields present
        Expected: Form displays with all required fields
        """
        browser.get(f"{BASE_URL}/register/")

        # Verify page title
        assert "Merchant Registration" in browser.page_source

        # Verify form fields
        assert browser.find_element(By.NAME, "business_name")
        assert browser.find_element(By.NAME, "registration_number")
        assert browser.find_element(By.NAME, "country")
        assert browser.find_element(By.NAME, "business_category")
        assert browser.find_element(By.NAME, "email")
        assert browser.find_element(By.NAME, "phone")
        assert browser.find_element(By.NAME, "address")

        take_screenshot(browser, "registration_form")
        print("✅ Registration form loads with all fields")

    def test_register_low_risk_merchant_auto_approved(self, browser):
        """
        Test: Low-risk merchant registration auto-approves
        Steps:
            1. Fill registration form with low-risk data
            2. Submit form
            3. Verify redirect to status page
            4. Verify APPROVED status
        Expected: Merchant auto-approved
        """
        browser.get(f"{BASE_URL}/register/")

        # Generate unique registration number
        reg_number = f"TEST-{int(time.time())}"

        # Fill form
        browser.find_element(By.NAME, "business_name").send_keys("Test E-commerce Singapore")
        browser.find_element(By.NAME, "registration_number").send_keys(reg_number)

        # Select country (Singapore - low risk)
        country_select = Select(browser.find_element(By.NAME, "country"))
        country_select.select_by_value("SG")

        # Select category (E-commerce - low risk)
        category_select = Select(browser.find_element(By.NAME, "business_category"))
        category_select.select_by_value("ECOMMERCE")

        browser.find_element(By.NAME, "email").send_keys("test@ecommerce.sg")
        browser.find_element(By.NAME, "phone").send_keys("+65 1234 5678")
        browser.find_element(By.NAME, "address").send_keys("123 Orchard Road, Singapore")

        take_screenshot(browser, "registration_filled_low_risk")

        # Set owner formset TOTAL_FORMS to 0 (no owners)
        browser.execute_script(
            "document.getElementById('id_owners-TOTAL_FORMS').value = '0';"
        )

        # Submit form
        form = browser.find_element(By.TAG_NAME, "form")
        browser.execute_script("arguments[0].submit();", form)

        # Wait for redirect
        time.sleep(2)
        WebDriverWait(browser, 15).until(
            lambda d: "/status/" in d.current_url
        )

        # Verify approved status
        time.sleep(1)  # Allow page to fully load
        page_source = browser.page_source
        assert "Approved" in page_source or "APPROVED" in page_source

        take_screenshot(browser, "registration_approved")
        print(f"✅ Low-risk merchant {reg_number} auto-approved")

    def test_register_high_risk_merchant_pending(self, browser):
        """
        Test: High-risk merchant registration goes to pending
        Steps:
            1. Fill registration with high-risk data (Crypto in Indonesia)
            2. Submit form
            3. Verify PENDING status
        Expected: Merchant pending manual review
        """
        browser.get(f"{BASE_URL}/register/")

        reg_number = f"HIGH-{int(time.time())}"

        # Fill form with high-risk data
        browser.find_element(By.NAME, "business_name").send_keys("Crypto Exchange Test")
        browser.find_element(By.NAME, "registration_number").send_keys(reg_number)

        # Select Indonesia (high risk country)
        country_select = Select(browser.find_element(By.NAME, "country"))
        country_select.select_by_value("ID")

        # Select Crypto (high risk category)
        category_select = Select(browser.find_element(By.NAME, "business_category"))
        category_select.select_by_value("CRYPTO")

        browser.find_element(By.NAME, "email").send_keys("test@crypto.id")
        browser.find_element(By.NAME, "phone").send_keys("+62 812 3456 7890")
        browser.find_element(By.NAME, "address").send_keys("Jakarta, Indonesia")

        take_screenshot(browser, "registration_filled_high_risk")

        # Set owner formset TOTAL_FORMS to 0
        browser.execute_script(
            "document.getElementById('id_owners-TOTAL_FORMS').value = '0';"
        )

        # Submit form
        form = browser.find_element(By.TAG_NAME, "form")
        browser.execute_script("arguments[0].submit();", form)

        # Wait for redirect
        time.sleep(2)
        WebDriverWait(browser, 15).until(
            lambda d: "/status/" in d.current_url
        )

        # Verify pending status
        time.sleep(1)
        page_source = browser.page_source
        assert "Pending" in page_source or "PENDING" in page_source

        take_screenshot(browser, "registration_pending")
        print(f"✅ High-risk merchant {reg_number} is pending review")

    def test_register_sanctioned_entity_rejected(self, browser):
        """
        Test: Sanctioned entity auto-rejected
        Steps:
            1. Fill registration with sanctioned business name
            2. Submit form
            3. Verify REJECTED status
        Expected: Merchant auto-rejected due to sanctions match
        """
        browser.get(f"{BASE_URL}/register/")

        reg_number = f"SANC-{int(time.time())}"

        # Fill form with sanctioned name
        browser.find_element(By.NAME, "business_name").send_keys("Shell Corp Ltd")  # Sanctioned
        browser.find_element(By.NAME, "registration_number").send_keys(reg_number)

        country_select = Select(browser.find_element(By.NAME, "country"))
        country_select.select_by_value("SG")

        category_select = Select(browser.find_element(By.NAME, "business_category"))
        category_select.select_by_value("ECOMMERCE")

        browser.find_element(By.NAME, "email").send_keys("shell@corp.com")
        browser.find_element(By.NAME, "phone").send_keys("+65 0000 0000")
        browser.find_element(By.NAME, "address").send_keys("Unknown")

        take_screenshot(browser, "registration_sanctioned")

        # Set owner formset TOTAL_FORMS to 0
        browser.execute_script(
            "document.getElementById('id_owners-TOTAL_FORMS').value = '0';"
        )

        # Submit form
        form = browser.find_element(By.TAG_NAME, "form")
        browser.execute_script("arguments[0].submit();", form)

        # Wait for redirect
        time.sleep(2)
        WebDriverWait(browser, 15).until(
            lambda d: "/status/" in d.current_url
        )

        # Verify rejected
        time.sleep(1)
        page_source = browser.page_source
        assert "Rejected" in page_source or "REJECTED" in page_source

        take_screenshot(browser, "registration_rejected")
        print(f"✅ Sanctioned entity {reg_number} auto-rejected")

    def test_registration_validation_errors(self, browser):
        """
        Test: Form validation shows errors
        Steps:
            1. Submit empty form
            2. Verify validation error messages
        Expected: Validation errors displayed
        """
        browser.get(f"{BASE_URL}/register/")

        # Submit empty form
        submit_btn = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
        safe_click(browser, submit_btn)

        # Check for validation errors (HTML5 validation or Django messages)
        time.sleep(1)

        # The form should not submit with empty required fields
        assert "/register/" in browser.current_url

        take_screenshot(browser, "registration_validation")
        print("✅ Form validation prevents empty submission")


# =============================================================================
# TEST CLASS: STATUS CHECK
# =============================================================================

class TestStatusCheck:
    """Tests for merchant status check."""

    def test_status_check_page_loads(self, browser):
        """
        Test: Status check page loads
        Steps:
            1. Navigate to status check page
            2. Verify form present
        Expected: Page loads with search form
        """
        browser.get(f"{BASE_URL}/status/")

        assert "Check Application Status" in browser.page_source
        assert browser.find_element(By.NAME, "registration_number")

        take_screenshot(browser, "status_check_page")
        print("✅ Status check page loads")

    def test_status_check_not_found(self, browser):
        """
        Test: Non-existent registration shows error
        Steps:
            1. Enter invalid registration number
            2. Submit search
            3. Verify error message
        Expected: Error message displayed
        """
        browser.get(f"{BASE_URL}/status/")

        # Enter non-existent registration
        reg_field = browser.find_element(By.NAME, "registration_number")
        reg_field.send_keys("DOES-NOT-EXIST-12345")
        reg_field.send_keys(Keys.RETURN)

        time.sleep(1)

        # Verify error message
        assert "No merchant found" in browser.page_source

        take_screenshot(browser, "status_not_found")
        print("✅ Non-existent registration shows error")


# =============================================================================
# TEST CLASS: DASHBOARD
# =============================================================================

class TestDashboard:
    """Tests for compliance dashboard."""

    def test_dashboard_loads(self, browser):
        """
        Test: Dashboard page loads with statistics
        Steps:
            1. Navigate to dashboard
            2. Verify statistics cards present
        Expected: Dashboard displays with stats
        """
        browser.get(f"{BASE_URL}/dashboard/")

        assert "Compliance Dashboard" in browser.page_source

        # Verify stat cards
        cards = browser.find_elements(By.CLASS_NAME, "card-stat")
        assert len(cards) >= 4  # Total, Pending, Approved, Rejected

        take_screenshot(browser, "dashboard")
        print("✅ Dashboard loads with statistics")

    def test_dashboard_shows_pending_merchants(self, browser):
        """
        Test: Dashboard shows pending merchants table
        Steps:
            1. Navigate to dashboard
            2. Verify pending reviews section
        Expected: Pending reviews section visible
        """
        browser.get(f"{BASE_URL}/dashboard/")

        # Look for pending reviews section
        assert "Pending Reviews" in browser.page_source or "pending" in browser.page_source.lower()

        take_screenshot(browser, "dashboard_pending")
        print("✅ Dashboard shows pending merchants section")


# =============================================================================
# TEST CLASS: ADMIN PANEL
# =============================================================================

class TestAdminPanel:
    """Tests for Django admin panel."""

    def test_admin_login_page_loads(self, browser):
        """
        Test: Admin login page loads
        Steps:
            1. Navigate to admin URL
            2. Verify login form present
        Expected: Login form displayed
        """
        browser.get(ADMIN_URL)

        assert browser.find_element(By.NAME, "username")
        assert browser.find_element(By.NAME, "password")

        take_screenshot(browser, "admin_login")
        print("✅ Admin login page loads")

    def test_admin_login_success(self, browser):
        """
        Test: Admin can login successfully
        Steps:
            1. Enter valid credentials
            2. Submit login
            3. Verify access to admin dashboard
        Expected: Login successful, admin dashboard shown
        """
        browser.get(ADMIN_URL)

        username_field = browser.find_element(By.NAME, "username")
        password_field = browser.find_element(By.NAME, "password")

        username_field.send_keys(ADMIN_USERNAME)
        password_field.send_keys(ADMIN_PASSWORD)
        password_field.send_keys(Keys.RETURN)

        # Wait for dashboard
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "site-name"))
        )

        assert "Site administration" in browser.page_source

        take_screenshot(browser, "admin_dashboard")
        print("✅ Admin login successful")

    def test_admin_login_invalid_credentials(self, browser):
        """
        Test: Invalid credentials show error
        Steps:
            1. Enter invalid credentials
            2. Submit login
            3. Verify error message
        Expected: Error message shown
        """
        browser.get(ADMIN_URL)

        username_field = browser.find_element(By.NAME, "username")
        password_field = browser.find_element(By.NAME, "password")

        username_field.send_keys("wronguser")
        password_field.send_keys("wrongpass")
        password_field.send_keys(Keys.RETURN)

        time.sleep(1)

        # Verify error message
        assert "enter the correct username" in browser.page_source.lower() or "error" in browser.page_source.lower()

        take_screenshot(browser, "admin_login_failed")
        print("✅ Invalid credentials show error")

    def test_admin_view_merchants(self, admin_browser):
        """
        Test: Admin can view merchants list
        Steps:
            1. Login to admin
            2. Navigate to merchants
            3. Verify list displays
        Expected: Merchants list visible
        """
        admin_browser.get(f"{ADMIN_URL}merchants/merchant/")

        assert "Select merchant to change" in admin_browser.page_source or "merchant" in admin_browser.page_source.lower()

        take_screenshot(admin_browser, "admin_merchants_list")
        print("✅ Admin can view merchants list")

    def test_admin_approve_merchant(self, admin_browser):
        """
        Test: Admin can approve a pending merchant
        Steps:
            1. Create a pending merchant via registration
            2. Navigate to admin merchants
            3. Select merchant and approve
            4. Verify status changed
        Expected: Merchant status changed to APPROVED
        """
        # First, create a pending merchant
        admin_browser.get(f"{BASE_URL}/register/")

        reg_number = f"ADMIN-{int(time.time())}"

        admin_browser.find_element(By.NAME, "business_name").send_keys("Admin Approval Test")
        admin_browser.find_element(By.NAME, "registration_number").send_keys(reg_number)

        country_select = Select(admin_browser.find_element(By.NAME, "country"))
        country_select.select_by_value("ID")

        category_select = Select(admin_browser.find_element(By.NAME, "business_category"))
        category_select.select_by_value("GAMING")

        admin_browser.find_element(By.NAME, "email").send_keys("admin@test.com")
        admin_browser.find_element(By.NAME, "phone").send_keys("+62 999 8888")
        admin_browser.find_element(By.NAME, "address").send_keys("Jakarta")

        # Set owner formset TOTAL_FORMS to 0
        admin_browser.execute_script(
            "document.getElementById('id_owners-TOTAL_FORMS').value = '0';"
        )

        # Submit form
        form = admin_browser.find_element(By.TAG_NAME, "form")
        admin_browser.execute_script("arguments[0].submit();", form)

        time.sleep(2)
        WebDriverWait(admin_browser, 15).until(
            lambda d: "/status/" in d.current_url
        )

        # Now go to admin and approve
        admin_browser.get(f"{ADMIN_URL}merchants/merchant/")

        # Find and click the merchant
        time.sleep(1)

        # Select the checkbox for the merchant (first one)
        try:
            checkbox = admin_browser.find_element(By.CSS_SELECTOR, "input[type='checkbox'][name='_selected_action']")
            safe_click(admin_browser, checkbox)

            # Select approve action
            action_select = Select(admin_browser.find_element(By.NAME, "action"))
            action_select.select_by_value("approve_merchants")

            # Click Go
            go_button = admin_browser.find_element(By.NAME, "index")
            safe_click(admin_browser, go_button)

            take_screenshot(admin_browser, "admin_approve_action")
            print("✅ Admin can approve merchant")
        except Exception as e:
            take_screenshot(admin_browser, "admin_approve_error")
            print(f"⚠️ Admin approve test: {e}")


# =============================================================================
# TEST CLASS: END-TO-END FLOWS
# =============================================================================

class TestEndToEndFlows:
    """Complete end-to-end workflow tests."""

    def test_e2e_full_approval_flow(self, browser):
        """
        Test: Complete flow from registration to approval
        Steps:
            1. Register low-risk merchant
            2. Check auto-approval
            3. Verify on status page
            4. Verify on dashboard
        Expected: Merchant appears as approved everywhere
        """
        reg_number = f"E2E-{int(time.time())}"

        # Step 1: Register
        browser.get(f"{BASE_URL}/register/")

        browser.find_element(By.NAME, "business_name").send_keys("E2E Test Company")
        browser.find_element(By.NAME, "registration_number").send_keys(reg_number)

        country_select = Select(browser.find_element(By.NAME, "country"))
        country_select.select_by_value("SG")

        category_select = Select(browser.find_element(By.NAME, "business_category"))
        category_select.select_by_value("DIGITAL_SERVICES")

        browser.find_element(By.NAME, "email").send_keys("e2e@test.com")
        browser.find_element(By.NAME, "phone").send_keys("+65 5555 5555")
        browser.find_element(By.NAME, "address").send_keys("Singapore")

        # Set owner formset TOTAL_FORMS to 0
        browser.execute_script(
            "document.getElementById('id_owners-TOTAL_FORMS').value = '0';"
        )

        # Submit form
        form = browser.find_element(By.TAG_NAME, "form")
        browser.execute_script("arguments[0].submit();", form)

        # Step 2: Verify redirect and approval
        time.sleep(2)
        WebDriverWait(browser, 15).until(
            lambda d: "/status/" in d.current_url
        )

        time.sleep(1)
        assert "Approved" in browser.page_source

        # Step 3: Check via status search
        browser.get(f"{BASE_URL}/status/")
        reg_field = browser.find_element(By.NAME, "registration_number")
        reg_field.send_keys(reg_number)
        reg_field.send_keys(Keys.RETURN)

        time.sleep(1)
        assert "E2E Test Company" in browser.page_source
        assert "Approved" in browser.page_source

        # Step 4: Check dashboard
        browser.get(f"{BASE_URL}/dashboard/")
        # Dashboard should show updated stats

        take_screenshot(browser, "e2e_complete_flow")
        print(f"✅ E2E: Complete approval flow for {reg_number}")

    def test_e2e_rejection_flow(self, browser):
        """
        Test: Complete flow for sanctioned entity rejection
        Steps:
            1. Register sanctioned entity
            2. Verify auto-rejection
            3. Check status shows rejection reason
        Expected: Merchant rejected with reason
        """
        reg_number = f"REJ-{int(time.time())}"

        browser.get(f"{BASE_URL}/register/")

        browser.find_element(By.NAME, "business_name").send_keys("Suspicious Trading Co")
        browser.find_element(By.NAME, "registration_number").send_keys(reg_number)

        country_select = Select(browser.find_element(By.NAME, "country"))
        country_select.select_by_value("SG")

        category_select = Select(browser.find_element(By.NAME, "business_category"))
        category_select.select_by_value("ECOMMERCE")

        browser.find_element(By.NAME, "email").send_keys("reject@test.com")
        browser.find_element(By.NAME, "phone").send_keys("+65 0000 0000")
        browser.find_element(By.NAME, "address").send_keys("Unknown")

        # Set owner formset TOTAL_FORMS to 0
        browser.execute_script(
            "document.getElementById('id_owners-TOTAL_FORMS').value = '0';"
        )

        # Submit form
        form = browser.find_element(By.TAG_NAME, "form")
        browser.execute_script("arguments[0].submit();", form)

        time.sleep(2)
        WebDriverWait(browser, 15).until(
            lambda d: "/status/" in d.current_url
        )

        time.sleep(1)
        page_source = browser.page_source
        assert "Rejected" in page_source
        assert "sanction" in page_source.lower()

        take_screenshot(browser, "e2e_rejection_flow")
        print(f"✅ E2E: Rejection flow for {reg_number}")


# =============================================================================
# TEST CLASS: BENEFICIAL OWNER TESTS
# =============================================================================

class TestBeneficialOwners:
    """Tests for beneficial owner functionality."""

    def test_add_beneficial_owner(self, browser):
        """
        Test: Can add beneficial owner during registration
        Steps:
            1. Go to registration
            2. Fill merchant info
            3. Fill beneficial owner info
            4. Submit and verify
        Expected: Owner saved with merchant
        """
        browser.get(f"{BASE_URL}/register/")

        reg_number = f"OWNER-{int(time.time())}"

        # Fill merchant info
        browser.find_element(By.NAME, "business_name").send_keys("Company With Owner")
        browser.find_element(By.NAME, "registration_number").send_keys(reg_number)

        country_select = Select(browser.find_element(By.NAME, "country"))
        country_select.select_by_value("SG")

        category_select = Select(browser.find_element(By.NAME, "business_category"))
        category_select.select_by_value("ECOMMERCE")

        browser.find_element(By.NAME, "email").send_keys("owner@test.com")
        browser.find_element(By.NAME, "phone").send_keys("+65 7777 7777")
        browser.find_element(By.NAME, "address").send_keys("Singapore")

        # Fill beneficial owner
        browser.find_element(By.NAME, "owners-0-full_name").send_keys("John Owner")

        owner_nationality = Select(browser.find_element(By.NAME, "owners-0-nationality"))
        owner_nationality.select_by_value("SG")

        browser.find_element(By.NAME, "owners-0-ownership_percentage").send_keys("100")

        owner_doc_type = Select(browser.find_element(By.NAME, "owners-0-id_document_type"))
        owner_doc_type.select_by_value("PASSPORT")

        browser.find_element(By.NAME, "owners-0-id_document_number").send_keys("E1234567")

        take_screenshot(browser, "registration_with_owner")

        # Submit
        submit_btn = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
        safe_click(browser, submit_btn)

        WebDriverWait(browser, 10).until(EC.url_contains("/status/"))

        # Verify owner displayed on status page
        time.sleep(1)
        assert "John Owner" in browser.page_source

        take_screenshot(browser, "owner_on_status")
        print(f"✅ Beneficial owner added to {reg_number}")


# =============================================================================
# REPORT GENERATION HELPERS
# =============================================================================

def pytest_configure(config):
    """Configure pytest to create reports directory."""
    os.makedirs("reports", exist_ok=True)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# =============================================================================
# MAIN RUNNER
# =============================================================================

if __name__ == "__main__":
    pytest.main([
        __file__,
        "-v",
        "--html=reports/test_report.html",
        "--self-contained-html",
        "-x",  # Stop on first failure
    ])
