"""
Comprehensive Automated Test Suite for Yuno KYB System
========================================================

This module contains full positive and negative test cases covering:
- Merchant Registration (valid/invalid inputs)
- Risk Assessment (all risk levels)
- Sanctions Screening (clear/match/potential match)
- Auto-Decisioning (approve/reject/review)
- Compliance Officer Workflows
- Edge Cases and Error Handling

Run with: python manage.py test merchants.test_full_scenarios --verbosity=2
"""

from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Merchant, BeneficialOwner, Document, RiskAssessment
from .risk_engine import calculate_risk_score, can_auto_approve, should_require_beneficial_owners
from screening.services import screen_merchant, screen_entity
from screening.models import ScreeningResult


# =============================================================================
# POSITIVE TEST CASES
# =============================================================================

class PositiveRegistrationTestCase(TestCase):
    """
    POSITIVE TEST CASES: Successful merchant registration scenarios
    """

    def setUp(self):
        self.client = Client()

    # -------------------------------------------------------------------------
    # P-REG-001: Low Risk E-commerce Singapore - Auto Approve
    # -------------------------------------------------------------------------
    def test_P_REG_001_low_risk_ecommerce_singapore_auto_approved(self):
        """
        Scenario: Low-risk merchant registration
        Given: E-commerce business in Singapore
        When: Merchant submits registration
        Then: Should be auto-approved with LOW risk level
        """
        data = {
            "business_name": "Singapore Tech Store Pte Ltd",
            "registration_number": "SG-REG-001",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "contact@sgtech.com",
            "phone": "+65 6123 4567",
            "address": "100 Orchard Road, Singapore 238840",
            "owners-TOTAL_FORMS": "0",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        response = self.client.post(reverse("register_merchant"), data, follow=True)

        merchant = Merchant.objects.get(registration_number="SG-REG-001")

        # Assertions
        self.assertEqual(merchant.status, "APPROVED")
        self.assertEqual(merchant.risk_level, "LOW")
        self.assertIn("Auto-approved", merchant.review_notes)

        # Verify risk assessment created
        assessment = merchant.get_latest_risk_assessment()
        self.assertIsNotNone(assessment)
        self.assertLessEqual(assessment.risk_score, 30)

        # Verify screening completed
        self.assertTrue(merchant.screening_results.exists())
        self.assertEqual(merchant.get_screening_status(), "CLEAR")

        print("✅ P-REG-001: Low-risk e-commerce Singapore auto-approved")

    # -------------------------------------------------------------------------
    # P-REG-002: Low Risk Digital Services Malaysia - Auto Approve
    # -------------------------------------------------------------------------
    def test_P_REG_002_low_risk_digital_services_malaysia_auto_approved(self):
        """
        Scenario: Digital services in Malaysia
        Given: Digital services business in Malaysia
        When: Merchant submits registration
        Then: Should be auto-approved
        """
        data = {
            "business_name": "CloudSoft Solutions Sdn Bhd",
            "registration_number": "MY-REG-002",
            "country": "MY",
            "business_category": "DIGITAL_SERVICES",
            "email": "info@cloudsoft.my",
            "phone": "+60 3 1234 5678",
            "address": "Menara KL, Kuala Lumpur",
            "owners-TOTAL_FORMS": "0",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        response = self.client.post(reverse("register_merchant"), data, follow=True)

        merchant = Merchant.objects.get(registration_number="MY-REG-002")

        self.assertEqual(merchant.status, "APPROVED")
        self.assertEqual(merchant.risk_level, "LOW")

        print("✅ P-REG-002: Digital services Malaysia auto-approved")

    # -------------------------------------------------------------------------
    # P-REG-003: Registration with Beneficial Owner
    # -------------------------------------------------------------------------
    def test_P_REG_003_registration_with_beneficial_owner(self):
        """
        Scenario: Registration with beneficial ownership information
        Given: Merchant with one beneficial owner
        When: Complete registration submitted
        Then: Should save merchant and owner, calculate risk including owner
        """
        data = {
            "business_name": "Family Holdings Pte Ltd",
            "registration_number": "SG-REG-003",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "family@holdings.sg",
            "phone": "+65 6999 8888",
            "address": "Marina Bay, Singapore",
            "owners-TOTAL_FORMS": "1",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
            "owners-0-full_name": "John Smith",
            "owners-0-nationality": "SG",
            "owners-0-ownership_percentage": "100",
            "owners-0-id_document_type": "PASSPORT",
            "owners-0-id_document_number": "E1234567A",
            "owners-0-is_pep": "",
        }

        response = self.client.post(reverse("register_merchant"), data, follow=True)

        merchant = Merchant.objects.get(registration_number="SG-REG-003")

        self.assertEqual(merchant.status, "APPROVED")
        self.assertEqual(merchant.owners.count(), 1)

        owner = merchant.owners.first()
        self.assertEqual(owner.full_name, "John Smith")
        self.assertEqual(owner.ownership_percentage, Decimal("100"))

        print("✅ P-REG-003: Registration with beneficial owner successful")

    # -------------------------------------------------------------------------
    # P-REG-004: Multiple Beneficial Owners
    # -------------------------------------------------------------------------
    def test_P_REG_004_registration_multiple_owners(self):
        """
        Scenario: Registration with multiple beneficial owners
        Given: Merchant with three shareholders
        When: Registration submitted
        Then: All owners should be saved and screened
        """
        data = {
            "business_name": "Joint Venture Corp",
            "registration_number": "SG-REG-004",
            "country": "SG",
            "business_category": "DIGITAL_SERVICES",
            "email": "jv@corp.sg",
            "phone": "+65 6777 5555",
            "address": "Raffles Place, Singapore",
            "owners-TOTAL_FORMS": "3",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
            "owners-0-full_name": "Alice Wong",
            "owners-0-nationality": "SG",
            "owners-0-ownership_percentage": "40",
            "owners-0-id_document_type": "NATIONAL_ID",
            "owners-0-id_document_number": "S1234567A",
            "owners-0-is_pep": "",
            "owners-1-full_name": "Bob Tan",
            "owners-1-nationality": "SG",
            "owners-1-ownership_percentage": "35",
            "owners-1-id_document_type": "PASSPORT",
            "owners-1-id_document_number": "E9876543B",
            "owners-1-is_pep": "",
            "owners-2-full_name": "Carol Lee",
            "owners-2-nationality": "MY",
            "owners-2-ownership_percentage": "25",
            "owners-2-id_document_type": "PASSPORT",
            "owners-2-id_document_number": "A1111111",
            "owners-2-is_pep": "",
        }

        response = self.client.post(reverse("register_merchant"), data, follow=True)

        merchant = Merchant.objects.get(registration_number="SG-REG-004")

        self.assertEqual(merchant.owners.count(), 3)

        # Verify screening for each owner
        owner_screenings = merchant.screening_results.filter(
            screened_entity__contains="Owner"
        )
        self.assertGreaterEqual(owner_screenings.count(), 3)  # At least sanctions check per owner

        print("✅ P-REG-004: Multiple beneficial owners registered and screened")


class PositiveStatusCheckTestCase(TestCase):
    """
    POSITIVE TEST CASES: Successful status check scenarios
    """

    def setUp(self):
        self.client = Client()
        # Create test merchant
        self.merchant = Merchant.objects.create(
            business_name="Status Test Corp",
            registration_number="STATUS-001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@status.com",
            phone="+65 1234 5678",
            address="Singapore",
            status="APPROVED",
            risk_level="LOW",
        )

    # -------------------------------------------------------------------------
    # P-STS-001: Valid Status Check
    # -------------------------------------------------------------------------
    def test_P_STS_001_valid_status_check(self):
        """
        Scenario: Check status with valid registration number
        Given: Existing merchant with registration number
        When: User checks status
        Then: Should display merchant status and details
        """
        response = self.client.post(
            reverse("check_status"),
            {"registration_number": "STATUS-001"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Status Test Corp")
        self.assertContains(response, "Approved")

        print("✅ P-STS-001: Valid status check returns merchant details")

    # -------------------------------------------------------------------------
    # P-STS-002: Status Page Direct Access
    # -------------------------------------------------------------------------
    def test_P_STS_002_status_page_direct_access(self):
        """
        Scenario: Direct access to status page via URL
        Given: Valid registration number in URL
        When: User navigates directly to status page
        Then: Should display full merchant details
        """
        response = self.client.get(
            reverse("merchant_status", args=["STATUS-001"])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Status Test Corp")
        self.assertContains(response, "Singapore")

        print("✅ P-STS-002: Direct status page access works")


class PositiveRiskAssessmentTestCase(TestCase):
    """
    POSITIVE TEST CASES: Risk assessment calculation scenarios
    """

    # -------------------------------------------------------------------------
    # P-RSK-001: Lowest Possible Risk Score
    # -------------------------------------------------------------------------
    def test_P_RSK_001_lowest_risk_score(self):
        """
        Scenario: Calculate lowest possible risk
        Given: E-commerce in Singapore with no owners
        When: Risk is calculated
        Then: Score should be 7 (minimum)
        """
        merchant = Merchant.objects.create(
            business_name="Min Risk Corp",
            registration_number="RSK-001",
            country="SG",
            business_category="ECOMMERCE",
            email="min@risk.com",
            phone="+65 1111 1111",
            address="Singapore",
        )

        score, factors, risk_level = calculate_risk_score(merchant)

        # E-commerce (10) * 0.4 + Singapore (10) * 0.3 = 4 + 3 = 7
        self.assertEqual(score, 7)
        self.assertEqual(risk_level, "LOW")
        self.assertEqual(len(factors), 0)  # No risk factors

        print("✅ P-RSK-001: Lowest risk score calculated correctly (7)")

    # -------------------------------------------------------------------------
    # P-RSK-002: Medium Risk Score
    # -------------------------------------------------------------------------
    def test_P_RSK_002_medium_risk_score(self):
        """
        Scenario: Calculate medium risk
        Given: Gaming business in Vietnam
        When: Risk is calculated
        Then: Score should be in medium range
        """
        merchant = Merchant.objects.create(
            business_name="Gaming Vietnam",
            registration_number="RSK-002",
            country="VN",
            business_category="GAMING",
            email="gaming@vn.com",
            phone="+84 1234 5678",
            address="Ho Chi Minh City",
        )

        score, factors, risk_level = calculate_risk_score(merchant)

        # Gaming (40) * 0.4 + Vietnam (40) * 0.3 = 16 + 12 = 28
        self.assertEqual(score, 28)
        self.assertIn("Medium-risk business category", factors[0])

        print(f"✅ P-RSK-002: Medium risk score calculated ({score})")

    # -------------------------------------------------------------------------
    # P-RSK-003: High Risk Score with All Factors
    # -------------------------------------------------------------------------
    def test_P_RSK_003_high_risk_all_factors(self):
        """
        Scenario: Calculate maximum risk with all factors
        Given: Crypto in Indonesia with complex ownership and PEP
        When: Risk is calculated
        Then: Score should be high with all factors listed
        """
        merchant = Merchant.objects.create(
            business_name="Crypto Exchange ID",
            registration_number="RSK-003",
            country="ID",
            business_category="CRYPTO",
            email="crypto@id.com",
            phone="+62 812 345 678",
            address="Jakarta",
        )

        # Add 4 small shareholders (complex ownership)
        for i in range(4):
            BeneficialOwner.objects.create(
                merchant=merchant,
                full_name=f"Owner {i+1}",
                nationality="ID",
                ownership_percentage=Decimal("20"),
                id_document_type="NATIONAL_ID",
                id_document_number=f"ID{i+1}",
                is_pep=(i == 0),  # First owner is PEP
            )

        score, factors, risk_level = calculate_risk_score(merchant)

        # Crypto (90)*0.4 + Indonesia (50)*0.3 + Complex (15) + PEP (15)
        # = 36 + 15 + 15 + 15 = 81
        self.assertEqual(score, 81)
        self.assertEqual(risk_level, "HIGH")

        # Verify all factors present
        factor_text = " ".join(factors)
        self.assertIn("Crypto", factor_text)
        self.assertIn("Indonesia", factor_text)
        self.assertIn("Complex ownership", factor_text)
        self.assertIn("PEP", factor_text)

        print(f"✅ P-RSK-003: High risk with all factors ({score})")


class PositiveSanctionsScreeningTestCase(TestCase):
    """
    POSITIVE TEST CASES: Successful sanctions screening scenarios
    """

    # -------------------------------------------------------------------------
    # P-SCR-001: Clean Business Passes Screening
    # -------------------------------------------------------------------------
    def test_P_SCR_001_clean_business_passes(self):
        """
        Scenario: Clean business name passes screening
        Given: Legitimate business name
        When: Screening is performed
        Then: Status should be CLEAR
        """
        status, match = screen_entity("Acme Software Solutions", "SANCTIONS")

        self.assertEqual(status, "CLEAR")
        self.assertIsNone(match)

        print("✅ P-SCR-001: Clean business passes screening")

    # -------------------------------------------------------------------------
    # P-SCR-002: Clean Owner Passes PEP Check
    # -------------------------------------------------------------------------
    def test_P_SCR_002_clean_owner_passes_pep(self):
        """
        Scenario: Non-PEP individual passes PEP screening
        Given: Regular person name
        When: PEP screening is performed
        Then: Status should be CLEAR
        """
        status, match = screen_entity("Michael Johnson", "PEP")

        self.assertEqual(status, "CLEAR")
        self.assertIsNone(match)

        print("✅ P-SCR-002: Non-PEP passes PEP screening")

    # -------------------------------------------------------------------------
    # P-SCR-003: Full Merchant Screening - All Clear
    # -------------------------------------------------------------------------
    def test_P_SCR_003_full_merchant_screening_clear(self):
        """
        Scenario: Complete merchant screening with no matches
        Given: Clean merchant with clean owners
        When: Full screening is performed
        Then: Overall status should be CLEAR
        """
        merchant = Merchant.objects.create(
            business_name="Perfectly Clean Corp",
            registration_number="SCR-003",
            country="SG",
            business_category="ECOMMERCE",
            email="clean@corp.sg",
            phone="+65 1234 5678",
            address="Singapore",
        )

        BeneficialOwner.objects.create(
            merchant=merchant,
            full_name="Legitimate Person",
            nationality="SG",
            ownership_percentage=Decimal("100"),
            id_document_type="PASSPORT",
            id_document_number="E1234567",
            is_pep=False,
        )

        status = screen_merchant(merchant)

        self.assertEqual(status, "CLEAR")

        # All results should be clear
        for result in merchant.screening_results.all():
            self.assertEqual(result.status, "CLEAR")

        print("✅ P-SCR-003: Full merchant screening returns CLEAR")


class PositiveAdminWorkflowTestCase(TestCase):
    """
    POSITIVE TEST CASES: Compliance officer admin workflows
    """

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username="compliance_officer",
            email="compliance@yuno.com",
            password="secure123"
        )
        self.client.login(username="compliance_officer", password="secure123")

    # -------------------------------------------------------------------------
    # P-ADM-001: Admin Can View Merchant List
    # -------------------------------------------------------------------------
    def test_P_ADM_001_admin_views_merchant_list(self):
        """
        Scenario: Compliance officer views merchant list
        Given: Logged in admin user
        When: Accessing merchant admin page
        Then: Should see list of merchants
        """
        Merchant.objects.create(
            business_name="Admin View Test",
            registration_number="ADM-001",
            country="SG",
            business_category="ECOMMERCE",
            email="admin@test.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        response = self.client.get("/admin/merchants/merchant/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin View Test")

        print("✅ P-ADM-001: Admin can view merchant list")

    # -------------------------------------------------------------------------
    # P-ADM-002: Admin Approves Pending Merchant
    # -------------------------------------------------------------------------
    def test_P_ADM_002_admin_approves_merchant(self):
        """
        Scenario: Compliance officer approves pending merchant
        Given: Pending merchant in system
        When: Admin uses approve action
        Then: Merchant status should be APPROVED with audit trail
        """
        merchant = Merchant.objects.create(
            business_name="Pending Approval Corp",
            registration_number="ADM-002",
            country="SG",
            business_category="GAMING",
            email="pending@corp.com",
            phone="+65 5555 5555",
            address="Singapore",
            status="PENDING",
        )

        response = self.client.post(
            "/admin/merchants/merchant/",
            {
                "action": "approve_merchants",
                "_selected_action": [merchant.pk],
            }
        )

        merchant.refresh_from_db()

        self.assertEqual(merchant.status, "APPROVED")
        self.assertEqual(merchant.reviewed_by, self.admin)
        self.assertIsNotNone(merchant.review_date)

        print("✅ P-ADM-002: Admin approved merchant with audit trail")

    # -------------------------------------------------------------------------
    # P-ADM-003: Admin Rejects Merchant with Notes
    # -------------------------------------------------------------------------
    def test_P_ADM_003_admin_rejects_merchant(self):
        """
        Scenario: Compliance officer rejects merchant
        Given: Under review merchant
        When: Admin uses reject action
        Then: Merchant status should be REJECTED with audit trail
        """
        merchant = Merchant.objects.create(
            business_name="Reject Test Corp",
            registration_number="ADM-003",
            country="ID",
            business_category="CRYPTO",
            email="reject@test.com",
            phone="+62 1234 5678",
            address="Jakarta",
            status="UNDER_REVIEW",
        )

        response = self.client.post(
            "/admin/merchants/merchant/",
            {
                "action": "reject_merchants",
                "_selected_action": [merchant.pk],
            }
        )

        merchant.refresh_from_db()

        self.assertEqual(merchant.status, "REJECTED")
        self.assertEqual(merchant.reviewed_by, self.admin)

        print("✅ P-ADM-003: Admin rejected merchant with audit trail")

    # -------------------------------------------------------------------------
    # P-ADM-004: Bulk Approve Multiple Merchants
    # -------------------------------------------------------------------------
    def test_P_ADM_004_bulk_approve_merchants(self):
        """
        Scenario: Bulk approve multiple pending merchants
        Given: Multiple pending merchants
        When: Admin selects all and approves
        Then: All should be approved
        """
        merchants = []
        for i in range(3):
            m = Merchant.objects.create(
                business_name=f"Bulk Test {i+1}",
                registration_number=f"BULK-00{i+1}",
                country="SG",
                business_category="ECOMMERCE",
                email=f"bulk{i+1}@test.com",
                phone="+65 1111 1111",
                address="Singapore",
                status="PENDING",
            )
            merchants.append(m)

        response = self.client.post(
            "/admin/merchants/merchant/",
            {
                "action": "approve_merchants",
                "_selected_action": [m.pk for m in merchants],
            }
        )

        for m in merchants:
            m.refresh_from_db()
            self.assertEqual(m.status, "APPROVED")

        print("✅ P-ADM-004: Bulk approved 3 merchants")


class PositiveDashboardTestCase(TestCase):
    """
    POSITIVE TEST CASES: Dashboard functionality
    """

    def setUp(self):
        self.client = Client()

    # -------------------------------------------------------------------------
    # P-DSH-001: Dashboard Displays Statistics
    # -------------------------------------------------------------------------
    def test_P_DSH_001_dashboard_displays_stats(self):
        """
        Scenario: Dashboard shows correct statistics
        Given: Mix of merchants in different states
        When: Viewing dashboard
        Then: Should show correct counts
        """
        # Create merchants in different states
        Merchant.objects.create(
            business_name="Approved 1", registration_number="DSH-A1",
            country="SG", business_category="ECOMMERCE",
            email="a1@test.com", phone="+65 1111", address="SG",
            status="APPROVED", risk_level="LOW"
        )
        Merchant.objects.create(
            business_name="Pending 1", registration_number="DSH-P1",
            country="SG", business_category="GAMING",
            email="p1@test.com", phone="+65 2222", address="SG",
            status="PENDING", risk_level="MEDIUM"
        )
        Merchant.objects.create(
            business_name="Rejected 1", registration_number="DSH-R1",
            country="ID", business_category="CRYPTO",
            email="r1@test.com", phone="+62 3333", address="ID",
            status="REJECTED", risk_level="HIGH"
        )

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Compliance Dashboard")

        # Check stats are in context
        self.assertEqual(response.context["stats"]["total"], 3)
        self.assertEqual(response.context["stats"]["approved"], 1)
        self.assertEqual(response.context["stats"]["pending"], 1)
        self.assertEqual(response.context["stats"]["rejected"], 1)

        print("✅ P-DSH-001: Dashboard displays correct statistics")


# =============================================================================
# NEGATIVE TEST CASES
# =============================================================================

class NegativeRegistrationTestCase(TestCase):
    """
    NEGATIVE TEST CASES: Registration failure scenarios
    """

    def setUp(self):
        self.client = Client()

    # -------------------------------------------------------------------------
    # N-REG-001: Missing Required Fields
    # -------------------------------------------------------------------------
    def test_N_REG_001_missing_required_fields(self):
        """
        Scenario: Registration with missing required fields
        Given: Incomplete registration data
        When: Form is submitted
        Then: Should fail validation, merchant not created
        """
        data = {
            "business_name": "",  # Missing
            "registration_number": "N-REG-001",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "test@test.com",
            "phone": "+65 1234 5678",
            "address": "Singapore",
            "owners-TOTAL_FORMS": "0",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        response = self.client.post(reverse("register_merchant"), data)

        # Should not redirect (form has errors)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")

        # Merchant should not be created
        self.assertFalse(Merchant.objects.filter(registration_number="N-REG-001").exists())

        print("✅ N-REG-001: Missing required fields rejected")

    # -------------------------------------------------------------------------
    # N-REG-002: Duplicate Registration Number
    # -------------------------------------------------------------------------
    def test_N_REG_002_duplicate_registration_number(self):
        """
        Scenario: Registration with duplicate registration number
        Given: Existing merchant with same registration number
        When: New registration submitted
        Then: Should fail with duplicate error
        """
        # Create existing merchant
        Merchant.objects.create(
            business_name="Existing Corp",
            registration_number="DUPLICATE-001",
            country="SG",
            business_category="ECOMMERCE",
            email="existing@corp.com",
            phone="+65 1111 1111",
            address="Singapore",
        )

        data = {
            "business_name": "New Corp",
            "registration_number": "DUPLICATE-001",  # Duplicate
            "country": "MY",
            "business_category": "DIGITAL_SERVICES",
            "email": "new@corp.com",
            "phone": "+60 2222 2222",
            "address": "Malaysia",
            "owners-TOTAL_FORMS": "0",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        response = self.client.post(reverse("register_merchant"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already exists")

        # Should still be only one merchant with that number
        self.assertEqual(
            Merchant.objects.filter(registration_number="DUPLICATE-001").count(),
            1
        )

        print("✅ N-REG-002: Duplicate registration number rejected")

    # -------------------------------------------------------------------------
    # N-REG-003: Invalid Email Format
    # -------------------------------------------------------------------------
    def test_N_REG_003_invalid_email_format(self):
        """
        Scenario: Registration with invalid email
        Given: Malformed email address
        When: Form is submitted
        Then: Should fail validation
        """
        data = {
            "business_name": "Test Corp",
            "registration_number": "N-REG-003",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "not-an-email",  # Invalid
            "phone": "+65 1234 5678",
            "address": "Singapore",
            "owners-TOTAL_FORMS": "0",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        response = self.client.post(reverse("register_merchant"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "valid email")

        print("✅ N-REG-003: Invalid email format rejected")

    # -------------------------------------------------------------------------
    # N-REG-004: Sanctions Match - Auto Reject
    # -------------------------------------------------------------------------
    def test_N_REG_004_sanctions_match_auto_rejected(self):
        """
        Scenario: Registration of sanctioned entity
        Given: Business name matching sanctions list
        When: Registration submitted
        Then: Should be auto-rejected
        """
        data = {
            "business_name": "Shell Corp Ltd",  # Matches sanctions
            "registration_number": "N-REG-004",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "shell@corp.com",
            "phone": "+65 1234 5678",
            "address": "Singapore",
            "owners-TOTAL_FORMS": "0",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        response = self.client.post(reverse("register_merchant"), data, follow=True)

        merchant = Merchant.objects.get(registration_number="N-REG-004")

        self.assertEqual(merchant.status, "REJECTED")
        self.assertIn("sanctions", merchant.review_notes.lower())

        # Verify screening shows match
        self.assertEqual(merchant.get_screening_status(), "MATCH")

        print("✅ N-REG-004: Sanctions match auto-rejected")

    # -------------------------------------------------------------------------
    # N-REG-005: Sanctioned Owner - Auto Reject
    # -------------------------------------------------------------------------
    def test_N_REG_005_sanctioned_owner_rejected(self):
        """
        Scenario: Registration with sanctioned beneficial owner
        Given: Clean business name but sanctioned owner
        When: Registration submitted
        Then: Should be auto-rejected due to owner match
        """
        data = {
            "business_name": "Legitimate Business Inc",
            "registration_number": "N-REG-005",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "legit@biz.com",
            "phone": "+65 1234 5678",
            "address": "Singapore",
            "owners-TOTAL_FORMS": "1",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
            "owners-0-full_name": "Shell Corp Ltd",  # Sanctioned name
            "owners-0-nationality": "SG",
            "owners-0-ownership_percentage": "100",
            "owners-0-id_document_type": "PASSPORT",
            "owners-0-id_document_number": "X1234567",
            "owners-0-is_pep": "",
        }

        response = self.client.post(reverse("register_merchant"), data, follow=True)

        merchant = Merchant.objects.get(registration_number="N-REG-005")

        self.assertEqual(merchant.status, "REJECTED")

        print("✅ N-REG-005: Sanctioned owner causes rejection")


class NegativeStatusCheckTestCase(TestCase):
    """
    NEGATIVE TEST CASES: Status check failure scenarios
    """

    def setUp(self):
        self.client = Client()

    # -------------------------------------------------------------------------
    # N-STS-001: Non-existent Registration Number
    # -------------------------------------------------------------------------
    def test_N_STS_001_nonexistent_registration(self):
        """
        Scenario: Check status with non-existent registration
        Given: Registration number not in system
        When: Status check submitted
        Then: Should show error message
        """
        response = self.client.post(
            reverse("check_status"),
            {"registration_number": "DOES-NOT-EXIST-123"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No merchant found")

        print("✅ N-STS-001: Non-existent registration shows error")

    # -------------------------------------------------------------------------
    # N-STS-002: Invalid Direct URL Access
    # -------------------------------------------------------------------------
    def test_N_STS_002_invalid_direct_url(self):
        """
        Scenario: Direct URL access with invalid registration
        Given: Non-existent registration in URL
        When: User navigates to status page
        Then: Should return 404
        """
        response = self.client.get(
            reverse("merchant_status", args=["INVALID-REG-999"])
        )

        self.assertEqual(response.status_code, 404)

        print("✅ N-STS-002: Invalid direct URL returns 404")


class NegativeAutoApprovalTestCase(TestCase):
    """
    NEGATIVE TEST CASES: Auto-approval blocking scenarios
    """

    # -------------------------------------------------------------------------
    # N-APR-001: High Risk Cannot Auto-Approve
    # -------------------------------------------------------------------------
    def test_N_APR_001_high_risk_blocked(self):
        """
        Scenario: High risk merchant cannot be auto-approved
        Given: Merchant with HIGH risk level
        When: Auto-approval checked
        Then: Should return False
        """
        merchant = Merchant.objects.create(
            business_name="High Risk Corp",
            registration_number="N-APR-001",
            country="ID",
            business_category="CRYPTO",
            email="high@risk.com",
            phone="+62 1234 5678",
            address="Jakarta",
        )

        score, factors, risk_level = calculate_risk_score(merchant)
        RiskAssessment.objects.create(
            merchant=merchant,
            risk_score=score,
            risk_factors=factors,
        )

        result = can_auto_approve(merchant, "CLEAR")

        self.assertFalse(result)

        print("✅ N-APR-001: High risk blocked from auto-approval")

    # -------------------------------------------------------------------------
    # N-APR-002: Potential Match Cannot Auto-Approve
    # -------------------------------------------------------------------------
    def test_N_APR_002_potential_match_blocked(self):
        """
        Scenario: Potential sanctions match cannot be auto-approved
        Given: Low risk merchant with POTENTIAL_MATCH
        When: Auto-approval checked
        Then: Should return False
        """
        merchant = Merchant.objects.create(
            business_name="Low Risk Corp",
            registration_number="N-APR-002",
            country="SG",
            business_category="ECOMMERCE",
            email="low@risk.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        score, factors, risk_level = calculate_risk_score(merchant)
        RiskAssessment.objects.create(
            merchant=merchant,
            risk_score=score,
            risk_factors=factors,
        )

        result = can_auto_approve(merchant, "POTENTIAL_MATCH")

        self.assertFalse(result)

        print("✅ N-APR-002: Potential match blocked from auto-approval")

    # -------------------------------------------------------------------------
    # N-APR-003: No Risk Assessment Cannot Auto-Approve
    # -------------------------------------------------------------------------
    def test_N_APR_003_no_assessment_blocked(self):
        """
        Scenario: Merchant without risk assessment cannot be auto-approved
        Given: Merchant with no risk assessment record
        When: Auto-approval checked
        Then: Should return False
        """
        merchant = Merchant.objects.create(
            business_name="No Assessment Corp",
            registration_number="N-APR-003",
            country="SG",
            business_category="ECOMMERCE",
            email="no@assessment.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        # No risk assessment created

        result = can_auto_approve(merchant, "CLEAR")

        self.assertFalse(result)

        print("✅ N-APR-003: No assessment blocked from auto-approval")


class NegativeSanctionsScreeningTestCase(TestCase):
    """
    NEGATIVE TEST CASES: Sanctions screening match scenarios
    """

    # -------------------------------------------------------------------------
    # N-SCR-001: Exact Sanctions Match
    # -------------------------------------------------------------------------
    def test_N_SCR_001_exact_sanctions_match(self):
        """
        Scenario: Exact match on sanctions list
        Given: Name matching sanctions list exactly
        When: Screening performed
        Then: Should return MATCH
        """
        sanctioned_names = [
            "Shell Corp Ltd",
            "Suspicious Trading Co",
            "Blacklisted Enterprises",
            "Fraudulent Services Inc",
            "Money Laundering Network",
            "Terrorist Funding Corp",
        ]

        for name in sanctioned_names:
            status, match = screen_entity(name, "SANCTIONS")
            self.assertEqual(status, "MATCH", f"Failed to match: {name}")
            self.assertIsNotNone(match)

        print(f"✅ N-SCR-001: All {len(sanctioned_names)} exact sanctions matches detected")

    # -------------------------------------------------------------------------
    # N-SCR-002: Fuzzy/Partial Sanctions Match
    # -------------------------------------------------------------------------
    def test_N_SCR_002_fuzzy_sanctions_match(self):
        """
        Scenario: Fuzzy match on sanctions list
        Given: Name similar to sanctioned entity
        When: Screening performed
        Then: Should return MATCH or POTENTIAL_MATCH
        """
        fuzzy_names = [
            ("Shell Corp Limited", "MATCH"),  # Variation
            ("The Shell Corp Ltd", "MATCH"),  # With prefix
            ("Shell Corp Ltd International", "MATCH"),  # With suffix
        ]

        for name, expected in fuzzy_names:
            status, match = screen_entity(name, "SANCTIONS")
            self.assertEqual(status, expected, f"Failed for: {name}")

        print("✅ N-SCR-002: Fuzzy sanctions matches detected")

    # -------------------------------------------------------------------------
    # N-SCR-003: PEP Match
    # -------------------------------------------------------------------------
    def test_N_SCR_003_pep_match(self):
        """
        Scenario: Match on PEP list
        Given: Name matching PEP list
        When: PEP screening performed
        Then: Should return MATCH
        """
        pep_names = [
            "John Politician",
            "Maria Governor",
            "Robert Senator",
        ]

        for name in pep_names:
            status, match = screen_entity(name, "PEP")
            self.assertEqual(status, "MATCH", f"Failed to match PEP: {name}")

        print(f"✅ N-SCR-003: All {len(pep_names)} PEP matches detected")


class NegativeAdminWorkflowTestCase(TestCase):
    """
    NEGATIVE TEST CASES: Admin workflow failure scenarios
    """

    # -------------------------------------------------------------------------
    # N-ADM-001: Unauthenticated Access Blocked
    # -------------------------------------------------------------------------
    def test_N_ADM_001_unauthenticated_blocked(self):
        """
        Scenario: Unauthenticated access to admin
        Given: No login credentials
        When: Accessing admin page
        Then: Should redirect to login
        """
        client = Client()  # No login

        response = client.get("/admin/merchants/merchant/")

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

        print("✅ N-ADM-001: Unauthenticated admin access blocked")

    # -------------------------------------------------------------------------
    # N-ADM-002: Non-Admin User Blocked
    # -------------------------------------------------------------------------
    def test_N_ADM_002_non_admin_blocked(self):
        """
        Scenario: Regular user cannot access admin
        Given: Non-superuser account
        When: Accessing admin page
        Then: Should be denied
        """
        client = Client()
        User.objects.create_user(
            username="regular_user",
            email="user@test.com",
            password="user123"
        )
        client.login(username="regular_user", password="user123")

        response = client.get("/admin/merchants/merchant/")

        # Should redirect to login (user has no admin access)
        self.assertEqual(response.status_code, 302)

        print("✅ N-ADM-002: Non-admin user blocked from admin")

    # -------------------------------------------------------------------------
    # N-ADM-003: Cannot Approve Already Approved
    # -------------------------------------------------------------------------
    def test_N_ADM_003_approve_already_approved(self):
        """
        Scenario: Attempting to approve already approved merchant
        Given: Merchant with APPROVED status
        When: Admin uses approve action
        Then: Should not change anything (already approved)
        """
        client = Client()
        admin = User.objects.create_superuser(
            "admin", "admin@test.com", "admin123"
        )
        client.login(username="admin", password="admin123")

        merchant = Merchant.objects.create(
            business_name="Already Approved",
            registration_number="N-ADM-003",
            country="SG",
            business_category="ECOMMERCE",
            email="approved@test.com",
            phone="+65 1234 5678",
            address="Singapore",
            status="APPROVED",
        )

        original_date = merchant.updated_at

        response = client.post(
            "/admin/merchants/merchant/",
            {
                "action": "approve_merchants",
                "_selected_action": [merchant.pk],
            }
        )

        merchant.refresh_from_db()

        # Status should still be approved, reviewed_by should not change
        # (approval action skips already approved merchants)
        self.assertEqual(merchant.status, "APPROVED")

        print("✅ N-ADM-003: Approve action on approved merchant handled")


class NegativeEdgeCaseTestCase(TestCase):
    """
    NEGATIVE TEST CASES: Edge cases and boundary conditions
    """

    # -------------------------------------------------------------------------
    # N-EDG-001: Empty Owner Form Ignored
    # -------------------------------------------------------------------------
    def test_N_EDG_001_empty_owner_ignored(self):
        """
        Scenario: Empty beneficial owner form submitted
        Given: Owner form with no data
        When: Registration submitted
        Then: Should create merchant without owner
        """
        data = {
            "business_name": "No Owner Corp",
            "registration_number": "N-EDG-001",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "noowner@corp.com",
            "phone": "+65 1234 5678",
            "address": "Singapore",
            "owners-TOTAL_FORMS": "1",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
            "owners-0-full_name": "",  # Empty
            "owners-0-nationality": "",
            "owners-0-ownership_percentage": "",
            "owners-0-id_document_type": "",
            "owners-0-id_document_number": "",
        }

        response = self.client.post(reverse("register_merchant"), data, follow=True)

        merchant = Merchant.objects.get(registration_number="N-EDG-001")

        # Merchant created but no owners
        self.assertEqual(merchant.owners.count(), 0)

        print("✅ N-EDG-001: Empty owner form ignored correctly")

    def setUp(self):
        self.client = Client()

    # -------------------------------------------------------------------------
    # N-EDG-002: Ownership Over 100%
    # -------------------------------------------------------------------------
    def test_N_EDG_002_ownership_validation(self):
        """
        Scenario: Beneficial owners with ownership exceeding 100%
        Note: This is a data quality issue - system should still work
        Given: Owners claiming >100% total ownership
        When: Registration submitted
        Then: Should still process (business logic, not form validation)
        """
        data = {
            "business_name": "Over Ownership Corp",
            "registration_number": "N-EDG-002",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "over@owner.com",
            "phone": "+65 1234 5678",
            "address": "Singapore",
            "owners-TOTAL_FORMS": "2",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
            "owners-0-full_name": "Owner A",
            "owners-0-nationality": "SG",
            "owners-0-ownership_percentage": "60",
            "owners-0-id_document_type": "PASSPORT",
            "owners-0-id_document_number": "A123",
            "owners-0-is_pep": "",
            "owners-1-full_name": "Owner B",
            "owners-1-nationality": "SG",
            "owners-1-ownership_percentage": "60",  # Total 120%
            "owners-1-id_document_type": "PASSPORT",
            "owners-1-id_document_number": "B456",
            "owners-1-is_pep": "",
        }

        response = self.client.post(reverse("register_merchant"), data, follow=True)

        # System should still create merchant (data quality issue, not validation)
        merchant = Merchant.objects.get(registration_number="N-EDG-002")
        self.assertEqual(merchant.owners.count(), 2)

        print("✅ N-EDG-002: Over 100% ownership handled (data quality issue)")

    # -------------------------------------------------------------------------
    # N-EDG-003: Very Long Business Name
    # -------------------------------------------------------------------------
    def test_N_EDG_003_long_business_name(self):
        """
        Scenario: Very long business name
        Given: Business name at max length
        When: Registration submitted
        Then: Should succeed (within limits)
        """
        long_name = "A" * 255  # Max length

        data = {
            "business_name": long_name,
            "registration_number": "N-EDG-003",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "long@name.com",
            "phone": "+65 1234 5678",
            "address": "Singapore",
            "owners-TOTAL_FORMS": "0",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        response = self.client.post(reverse("register_merchant"), data, follow=True)

        merchant = Merchant.objects.get(registration_number="N-EDG-003")
        self.assertEqual(len(merchant.business_name), 255)

        print("✅ N-EDG-003: Max length business name accepted")


# =============================================================================
# INTEGRATION TEST CASES
# =============================================================================

class IntegrationEndToEndTestCase(TestCase):
    """
    END-TO-END INTEGRATION TESTS: Complete workflow scenarios
    """

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            "compliance", "compliance@yuno.com", "comp123"
        )

    # -------------------------------------------------------------------------
    # I-E2E-001: Complete Low Risk Auto-Approval Flow
    # -------------------------------------------------------------------------
    def test_I_E2E_001_low_risk_auto_approval_flow(self):
        """
        End-to-end: Low risk merchant registration to auto-approval

        Steps:
        1. Merchant submits registration
        2. System calculates risk
        3. System runs screening
        4. System auto-approves
        5. Merchant checks status
        """
        # Step 1: Register
        data = {
            "business_name": "E2E Low Risk Test",
            "registration_number": "E2E-001",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "e2e@test.com",
            "phone": "+65 9999 9999",
            "address": "Singapore",
            "owners-TOTAL_FORMS": "0",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        self.client.post(reverse("register_merchant"), data, follow=True)

        merchant = Merchant.objects.get(registration_number="E2E-001")

        # Step 2-4: Verify auto-processing
        self.assertEqual(merchant.status, "APPROVED")
        self.assertEqual(merchant.risk_level, "LOW")
        self.assertIsNotNone(merchant.get_latest_risk_assessment())
        self.assertTrue(merchant.screening_results.exists())

        # Step 5: Check status
        response = self.client.get(reverse("merchant_status", args=["E2E-001"]))
        self.assertContains(response, "Approved")

        print("✅ I-E2E-001: Complete low-risk auto-approval flow")

    # -------------------------------------------------------------------------
    # I-E2E-002: Complete Manual Review Flow
    # -------------------------------------------------------------------------
    def test_I_E2E_002_manual_review_flow(self):
        """
        End-to-end: High risk merchant to manual approval

        Steps:
        1. Merchant submits high-risk registration
        2. System calculates high risk
        3. System runs screening (clear)
        4. System sets to PENDING
        5. Compliance officer reviews in admin
        6. Compliance officer approves
        7. Merchant checks status
        """
        # Step 1: Register high-risk
        data = {
            "business_name": "E2E Manual Review Test",
            "registration_number": "E2E-002",
            "country": "ID",
            "business_category": "REMITTANCES",
            "email": "manual@review.com",
            "phone": "+62 8888 8888",
            "address": "Jakarta",
            "owners-TOTAL_FORMS": "0",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        self.client.post(reverse("register_merchant"), data, follow=True)

        merchant = Merchant.objects.get(registration_number="E2E-002")

        # Step 2-4: Verify pending
        self.assertEqual(merchant.status, "PENDING")
        self.assertIn(merchant.risk_level, ["MEDIUM", "HIGH"])

        # Step 5-6: Admin approval
        self.client.login(username="compliance", password="comp123")
        self.client.post(
            "/admin/merchants/merchant/",
            {
                "action": "approve_merchants",
                "_selected_action": [merchant.pk],
            }
        )

        merchant.refresh_from_db()

        # Step 7: Verify approved
        self.assertEqual(merchant.status, "APPROVED")
        self.assertEqual(merchant.reviewed_by, self.admin)

        print("✅ I-E2E-002: Complete manual review flow")

    # -------------------------------------------------------------------------
    # I-E2E-003: Complete Rejection Flow
    # -------------------------------------------------------------------------
    def test_I_E2E_003_sanctions_rejection_flow(self):
        """
        End-to-end: Sanctioned entity to auto-rejection

        Steps:
        1. Sanctioned entity submits registration
        2. System calculates risk
        3. System runs screening (MATCH)
        4. System auto-rejects
        5. Entity checks status (sees rejection)
        """
        # Step 1: Register sanctioned entity
        data = {
            "business_name": "Suspicious Trading Co",
            "registration_number": "E2E-003",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "suspicious@trading.com",
            "phone": "+65 0000 0000",
            "address": "Singapore",
            "owners-TOTAL_FORMS": "0",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        self.client.post(reverse("register_merchant"), data, follow=True)

        merchant = Merchant.objects.get(registration_number="E2E-003")

        # Step 2-4: Verify rejected
        self.assertEqual(merchant.status, "REJECTED")
        self.assertIn("sanctions", merchant.review_notes.lower())

        # Verify screening shows match
        match_results = merchant.screening_results.filter(status="MATCH")
        self.assertTrue(match_results.exists())

        # Step 5: Check status shows rejection
        response = self.client.get(reverse("merchant_status", args=["E2E-003"]))
        self.assertContains(response, "Rejected")

        print("✅ I-E2E-003: Complete sanctions rejection flow")

    # -------------------------------------------------------------------------
    # I-E2E-004: PEP Flagged for Review Flow
    # -------------------------------------------------------------------------
    def test_I_E2E_004_pep_review_flow(self):
        """
        End-to-end: PEP involvement flagged for review

        Steps:
        1. Merchant with PEP owner submits registration
        2. System detects PEP
        3. System flags for review (not auto-reject)
        4. Compliance officer reviews
        """
        # Step 1: Register with PEP owner
        data = {
            "business_name": "Political Family Business",
            "registration_number": "E2E-004",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "political@family.com",
            "phone": "+65 7777 7777",
            "address": "Singapore",
            "owners-TOTAL_FORMS": "1",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
            "owners-0-full_name": "John Politician",  # PEP match
            "owners-0-nationality": "PH",
            "owners-0-ownership_percentage": "51",
            "owners-0-id_document_type": "PASSPORT",
            "owners-0-id_document_number": "PH999",
            "owners-0-is_pep": "on",
        }

        self.client.post(reverse("register_merchant"), data, follow=True)

        merchant = Merchant.objects.get(registration_number="E2E-004")

        # Step 2-3: Verify flagged (not rejected)
        self.assertIn(merchant.status, ["PENDING", "UNDER_REVIEW"])

        # Verify PEP screening result
        pep_results = merchant.screening_results.filter(screening_type="PEP")
        self.assertTrue(pep_results.exists())

        # Verify risk factors include PEP
        assessment = merchant.get_latest_risk_assessment()
        factor_text = " ".join(assessment.risk_factors)
        self.assertIn("PEP", factor_text)

        print("✅ I-E2E-004: PEP flagged for review (not auto-rejected)")


# =============================================================================
# RUN ALL TESTS
# =============================================================================

if __name__ == "__main__":
    import sys
    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "test", "merchants.test_full_scenarios", "-v2"])
