# Yuno KYB Testing Documentation

Comprehensive testing suite for the Yuno KYB (Know Your Business) Onboarding System.

---

## Table of Contents

- [Overview](#overview)
- [Test Architecture](#test-architecture)
- [Quick Start](#quick-start)
- [Unit Tests](#unit-tests)
- [Browser Tests](#browser-tests)
- [Test Reports](#test-reports)
- [Test Data](#test-data)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

---

## Overview

The Yuno KYB testing suite includes:

| Test Type | Framework | Count | Purpose |
|-----------|-----------|-------|---------|
| **Unit Tests** | Django TestCase | 88 | Backend logic validation |
| **Browser Tests** | Selenium + Pytest | 19 | Frontend UI automation |
| **Total** | - | **107** | Full system coverage |

### Test Coverage Areas

- ✅ Risk Assessment Engine
- ✅ Sanctions Screening Service
- ✅ Auto-Approval Logic
- ✅ Merchant Registration Flow
- ✅ Compliance Officer Workflows
- ✅ Admin Panel Functionality
- ✅ Status Check Features
- ✅ Dashboard Statistics
- ✅ Form Validation
- ✅ End-to-End Workflows

---

## Test Architecture

```
tests/
├── README.md                    # This documentation
├── __init__.py
├── browser_tests.py             # Selenium browser automation tests
│
merchants/
├── tests.py                     # Core unit tests (48 tests)
├── test_full_scenarios.py       # Comprehensive scenario tests (40 tests)
│
screening/
├── tests.py                     # Screening service tests (17 tests included in core)
│
reports/
├── test_report.html             # Browser test HTML report
├── screenshots/                 # Test failure screenshots
```

---

## Quick Start

### Prerequisites

```bash
# Activate virtual environment
cd /Users/ahmed/Desktop/AIChallange/yuno_kyb
source venv/bin/activate

# Install test dependencies
pip install selenium pytest pytest-html webdriver-manager requests
```

### Run All Tests

```bash
# Run all unit tests (88 tests)
python manage.py test

# Run browser tests (19 tests) - requires server running
python manage.py runserver &
pytest tests/browser_tests.py -v --html=reports/test_report.html
```

---

## Unit Tests

### Running Unit Tests

```bash
# Run all unit tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run specific app tests
python manage.py test merchants
python manage.py test screening

# Run specific test file
python manage.py test merchants.tests
python manage.py test merchants.test_full_scenarios

# Run specific test class
python manage.py test merchants.tests.RiskEngineTestCase
python manage.py test merchants.test_full_scenarios.PositiveRegistrationTestCase

# Run specific test method
python manage.py test merchants.tests.RiskEngineTestCase.test_low_risk_score_ecommerce_singapore
```

### Unit Test Categories

#### Core Tests (`merchants/tests.py`)

| Class | Tests | Description |
|-------|-------|-------------|
| `RiskEngineTestCase` | 7 | Risk score calculation |
| `SanctionsScreeningTestCase` | 6 | Sanctions matching |
| `MerchantAutoApprovalTestCase` | 3 | Auto-approval rules |
| `MerchantRegistrationViewTestCase` | 7 | Registration views |
| `ComplianceOfficerWorkflowTestCase` | 4 | Admin workflows |
| `IntegrationTestCase` | 3 | End-to-end flows |

#### Scenario Tests (`merchants/test_full_scenarios.py`)

| Category | Prefix | Tests | Description |
|----------|--------|-------|-------------|
| **Positive Registration** | P-REG | 4 | Successful registrations |
| **Positive Status** | P-STS | 2 | Status check success |
| **Positive Risk** | P-RSK | 3 | Risk calculations |
| **Positive Screening** | P-SCR | 3 | Clear screening |
| **Positive Admin** | P-ADM | 4 | Admin actions |
| **Positive Dashboard** | P-DSH | 1 | Dashboard display |
| **Negative Registration** | N-REG | 5 | Registration failures |
| **Negative Status** | N-STS | 2 | Status check failures |
| **Negative Approval** | N-APR | 3 | Approval blocks |
| **Negative Screening** | N-SCR | 3 | Screening matches |
| **Negative Admin** | N-ADM | 3 | Admin restrictions |
| **Negative Edge Cases** | N-EDG | 3 | Boundary conditions |
| **Integration E2E** | I-E2E | 4 | Full workflows |

#### Screening Tests (`screening/tests.py`)

| Class | Tests | Description |
|-------|-------|-------------|
| `SimilarityCalculationTestCase` | 4 | String matching |
| `ScreenEntityTestCase` | 6 | Entity screening |
| `ScreenMerchantTestCase` | 6 | Merchant screening |
| `RescreenMerchantTestCase` | 1 | Re-screening |
| `ScreeningResultModelTestCase` | 2 | Model behavior |

---

## Browser Tests

### Prerequisites

1. **Chrome Browser** - Latest version installed
2. **Django Server Running** - On `http://127.0.0.1:8000`
3. **Admin User Created** - Username: `admin`, Password: `admin123`

### Running Browser Tests

```bash
# Start Django server (in background)
python manage.py runserver &

# Run all browser tests with HTML report
pytest tests/browser_tests.py -v --html=reports/test_report.html --self-contained-html

# Run specific test class
pytest tests/browser_tests.py::TestMerchantRegistration -v

# Run specific test
pytest tests/browser_tests.py::TestMerchantRegistration::test_register_low_risk_merchant_auto_approved -v

# Run with visible browser (default)
pytest tests/browser_tests.py -v

# Run in headless mode (no browser window)
# Edit browser_tests.py and uncomment: chrome_options.add_argument("--headless")
```

### Browser Test Classes

| Class | Tests | Description |
|-------|-------|-------------|
| `TestHomePage` | 2 | Home page load, navigation |
| `TestMerchantRegistration` | 5 | Registration form, submissions |
| `TestStatusCheck` | 2 | Status lookup |
| `TestDashboard` | 2 | Dashboard display |
| `TestAdminPanel` | 5 | Admin login, approve/reject |
| `TestEndToEndFlows` | 2 | Complete workflows |
| `TestBeneficialOwners` | 1 | Owner registration |

### Browser Test Details

#### TestHomePage
| Test | Steps | Expected |
|------|-------|----------|
| `test_home_page_loads` | Navigate to home | Title contains "Yuno KYB" |
| `test_home_page_navigation_links` | Click all nav links | Correct pages load |

#### TestMerchantRegistration
| Test | Steps | Expected |
|------|-------|----------|
| `test_registration_form_loads` | Open registration page | All form fields present |
| `test_register_low_risk_merchant_auto_approved` | Submit low-risk data | Status = APPROVED |
| `test_register_high_risk_merchant_pending` | Submit high-risk data | Status = PENDING |
| `test_register_sanctioned_entity_rejected` | Submit sanctioned name | Status = REJECTED |
| `test_registration_validation_errors` | Submit empty form | Validation errors shown |

#### TestStatusCheck
| Test | Steps | Expected |
|------|-------|----------|
| `test_status_check_page_loads` | Open status page | Form displayed |
| `test_status_check_not_found` | Search invalid number | Error message shown |

#### TestDashboard
| Test | Steps | Expected |
|------|-------|----------|
| `test_dashboard_loads` | Open dashboard | Statistics cards visible |
| `test_dashboard_shows_pending_merchants` | View pending section | Pending list shown |

#### TestAdminPanel
| Test | Steps | Expected |
|------|-------|----------|
| `test_admin_login_page_loads` | Open admin URL | Login form shown |
| `test_admin_login_success` | Login with valid creds | Dashboard shown |
| `test_admin_login_invalid_credentials` | Login with bad creds | Error message |
| `test_admin_view_merchants` | Navigate to merchants | List displayed |
| `test_admin_approve_merchant` | Select and approve | Status changed |

#### TestEndToEndFlows
| Test | Steps | Expected |
|------|-------|----------|
| `test_e2e_full_approval_flow` | Register → Check Status | Complete flow works |
| `test_e2e_rejection_flow` | Register sanctioned → Check | Rejection shown |

#### TestBeneficialOwners
| Test | Steps | Expected |
|------|-------|----------|
| `test_add_beneficial_owner` | Fill owner form | Owner saved with merchant |

---

## Test Reports

### HTML Report

Browser tests generate an HTML report with:
- Test results summary
- Pass/Fail statistics
- Execution time
- Error details for failures

**Location:** `reports/test_report.html`

### Screenshots

Automatic screenshots are captured during browser tests:
- On test completion (success)
- On test failure (for debugging)

**Location:** `reports/screenshots/`

### Viewing Reports

```bash
# Open HTML report in browser
open reports/test_report.html

# View screenshots
open reports/screenshots/
```

---

## Test Data

### Mock Sanctions List

Used for testing sanctions screening:

| Name | List | Type |
|------|------|------|
| Shell Corp Ltd | OFAC SDN | SANCTIONS |
| Suspicious Trading Co | UN Sanctions | SANCTIONS |
| Blacklisted Enterprises | EU Sanctions | SANCTIONS |
| Fraudulent Services Inc | OFAC SDN | SANCTIONS |
| Money Laundering Network | FATF Blacklist | SANCTIONS |
| Terrorist Funding Corp | UN Sanctions | SANCTIONS |

### Mock PEP List

| Name | Position | Country |
|------|----------|---------|
| John Politician | Former Minister | PH |
| Maria Governor | Regional Governor | ID |
| Robert Senator | Senator | SG |

### Test Merchant Data

#### Low Risk (Auto-Approve)
```python
{
    "business_name": "Tech Shop Pte Ltd",
    "country": "SG",           # Singapore
    "business_category": "ECOMMERCE",
    "expected_status": "APPROVED",
    "expected_risk": "LOW"
}
```

#### High Risk (Manual Review)
```python
{
    "business_name": "Crypto Exchange",
    "country": "ID",           # Indonesia
    "business_category": "CRYPTO",
    "expected_status": "PENDING",
    "expected_risk": "MEDIUM/HIGH"
}
```

#### Sanctioned (Auto-Reject)
```python
{
    "business_name": "Shell Corp Ltd",
    "country": "ANY",
    "business_category": "ANY",
    "expected_status": "REJECTED",
    "reason": "Sanctions match"
}
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Yuno KYB Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        pip install selenium pytest pytest-html webdriver-manager

    - name: Run unit tests
      run: |
        source venv/bin/activate
        python manage.py test --verbosity=2

    - name: Run browser tests
      run: |
        source venv/bin/activate
        python manage.py runserver &
        sleep 5
        pytest tests/browser_tests.py -v --html=reports/test_report.html

    - name: Upload test report
      uses: actions/upload-artifact@v3
      with:
        name: test-report
        path: reports/
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running tests..."
source venv/bin/activate
python manage.py test --verbosity=1

if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi

echo "All tests passed!"
```

---

## Troubleshooting

### Common Issues

#### 1. Browser Tests Fail to Start

**Error:** `WebDriverException: ChromeDriver not found`

**Solution:**
```bash
pip install --upgrade webdriver-manager
```

#### 2. Server Not Running

**Error:** `ConnectionRefusedError: Connection refused`

**Solution:**
```bash
# Start the server first
python manage.py runserver &
sleep 3
pytest tests/browser_tests.py -v
```

#### 3. Form Submission Fails

**Error:** `TimeoutException: Element not clickable`

**Solution:** The test uses JavaScript form submission to bypass click issues. Ensure the form has all required fields.

#### 4. Admin Login Fails

**Error:** `AssertionError: Admin login failed`

**Solution:**
```bash
# Create/reset admin user
python manage.py createsuperuser --username admin --email admin@yuno.com
# Enter password: admin123
```

#### 5. Database Errors

**Error:** `OperationalError: no such table`

**Solution:**
```bash
python manage.py migrate
```

### Debug Mode

Run browser tests with visible browser and slower execution:

```python
# In tests/browser_tests.py, modify the browser fixture:
chrome_options.add_argument("--start-maximized")
# Comment out: chrome_options.add_argument("--headless")

# Add delays for debugging
import time
time.sleep(5)  # Pause to see what's happening
```

### Viewing Test Database

Unit tests use an in-memory SQLite database that is destroyed after tests. To inspect data:

```python
# In your test, add:
from django.conf import settings
print(f"Database: {settings.DATABASES['default']['NAME']}")
```

---

## Test Naming Conventions

### Unit Tests

- `test_<action>_<condition>_<expected>`
- Example: `test_low_risk_merchant_auto_approved`

### Scenario Tests

- `test_<ID>_<description>`
- Positive: `test_P_REG_001_low_risk_ecommerce_singapore_auto_approved`
- Negative: `test_N_REG_001_missing_required_fields`
- Integration: `test_I_E2E_001_low_risk_auto_approval_flow`

### Browser Tests

- `test_<feature>_<action>`
- Example: `test_register_low_risk_merchant_auto_approved`

---

## Adding New Tests

### Unit Test Template

```python
def test_new_feature_works(self):
    """
    Test: Description of what is being tested
    Given: Initial conditions
    When: Action taken
    Then: Expected outcome
    """
    # Arrange
    merchant = Merchant.objects.create(...)

    # Act
    result = some_function(merchant)

    # Assert
    self.assertEqual(result, expected_value)
    print("✅ Test description")
```

### Browser Test Template

```python
def test_new_ui_feature(self, browser):
    """
    Test: UI feature description
    Steps:
        1. Navigate to page
        2. Perform action
        3. Verify result
    Expected: Outcome description
    """
    browser.get(f"{BASE_URL}/page/")

    element = browser.find_element(By.ID, "element-id")
    element.click()

    assert "expected text" in browser.page_source

    take_screenshot(browser, "test_name")
    print("✅ Test passed")
```

---

## Contact

For testing questions or issues:
- **QA Team:** qa@yuno.com
- **Engineering:** engineering@yuno.com

---

*Last Updated: February 2026*
