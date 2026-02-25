"""
Automated tests for the Yuno KYB Merchant Onboarding System.
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Merchant, BeneficialOwner, RiskAssessment
from .risk_engine import (
    calculate_risk_score,
    should_require_beneficial_owners,
    can_auto_approve,
    CATEGORY_WEIGHTS,
    COUNTRY_WEIGHTS,
)
from screening.services import screen_merchant, screen_entity


class RiskEngineTestCase(TestCase):
    """Tests for the risk scoring engine."""

    def test_low_risk_score_ecommerce_singapore(self):
        """E-commerce in Singapore should have LOW risk score."""
        merchant = Merchant.objects.create(
            business_name="Tech Solutions Pte Ltd",
            registration_number="SG12345",
            country="SG",
            business_category="ECOMMERCE",
            email="test@example.com",
            phone="+65 1234 5678",
            address="Singapore",
        )
        score, factors, risk_level = calculate_risk_score(merchant)

        self.assertLessEqual(score, 30)
        self.assertEqual(risk_level, "LOW")
        print(f"✓ Low risk test: score={score}, level={risk_level}")

    def test_high_risk_score_crypto_indonesia(self):
        """Crypto business in Indonesia should have elevated risk score."""
        merchant = Merchant.objects.create(
            business_name="Crypto Exchange ID",
            registration_number="ID98765",
            country="ID",
            business_category="CRYPTO",
            email="test@example.com",
            phone="+62 812 3456",
            address="Jakarta, Indonesia",
        )
        score, factors, risk_level = calculate_risk_score(merchant)

        # Crypto (90*0.4=36) + Indonesia (50*0.3=15) = 51 = MEDIUM
        self.assertGreater(score, 30)
        self.assertIn(risk_level, ["MEDIUM", "HIGH"])
        self.assertTrue(any("High-risk business category" in f for f in factors))
        print(f"✓ High risk test: score={score}, level={risk_level}")

    def test_medium_risk_score_gaming_philippines(self):
        """Gaming business in Philippines should have elevated risk score."""
        merchant = Merchant.objects.create(
            business_name="Gaming Corp",
            registration_number="PH11111",
            country="PH",
            business_category="GAMING",
            email="test@example.com",
            phone="+63 912 345",
            address="Manila, Philippines",
        )
        score, factors, risk_level = calculate_risk_score(merchant)

        # Gaming (40*0.4=16) + Philippines (30*0.3=9) = 25
        # Still flags as medium-risk category
        self.assertGreater(score, 20)
        self.assertTrue(any("Medium-risk business category" in f for f in factors))
        print(f"✓ Gaming risk test: score={score}, level={risk_level}")

    def test_pep_increases_risk_score(self):
        """PEP involvement should increase risk score by 15 points."""
        merchant = Merchant.objects.create(
            business_name="Family Business",
            registration_number="SG22222",
            country="SG",
            business_category="ECOMMERCE",
            email="test@example.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        # Score without PEP
        score_without_pep, _, _ = calculate_risk_score(merchant)

        # Add PEP owner
        BeneficialOwner.objects.create(
            merchant=merchant,
            full_name="John Politician",
            nationality="SG",
            ownership_percentage=Decimal("51.00"),
            id_document_type="PASSPORT",
            id_document_number="E1234567",
            is_pep=True,
        )

        # Score with PEP
        score_with_pep, factors, _ = calculate_risk_score(merchant)

        self.assertEqual(score_with_pep - score_without_pep, 15)
        self.assertTrue(any("PEP" in f for f in factors))
        print(f"✓ PEP test: score increased from {score_without_pep} to {score_with_pep}")

    def test_complex_ownership_increases_risk(self):
        """Complex ownership (>3 small shareholders) should increase risk."""
        merchant = Merchant.objects.create(
            business_name="Complex Holdings",
            registration_number="SG33333",
            country="SG",
            business_category="ECOMMERCE",
            email="test@example.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        # Add 4 small shareholders (<25% each)
        for i in range(4):
            BeneficialOwner.objects.create(
                merchant=merchant,
                full_name=f"Owner {i+1}",
                nationality="SG",
                ownership_percentage=Decimal("20.00"),
                id_document_type="PASSPORT",
                id_document_number=f"P{i+1}",
                is_pep=False,
            )

        score, factors, _ = calculate_risk_score(merchant)

        self.assertTrue(any("Complex ownership" in f for f in factors))
        print(f"✓ Complex ownership test: score={score}, factors={factors}")

    def test_should_require_beneficial_owners_high_risk(self):
        """High-risk categories should require beneficial owner info."""
        merchant = Merchant.objects.create(
            business_name="Crypto Biz",
            registration_number="SG44444",
            country="SG",
            business_category="CRYPTO",
            email="test@example.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        self.assertTrue(should_require_beneficial_owners(merchant))
        print("✓ High-risk category requires beneficial owners")

    def test_should_not_require_beneficial_owners_low_risk(self):
        """Low-risk e-commerce in Singapore should not require beneficial owners."""
        merchant = Merchant.objects.create(
            business_name="Simple Shop",
            registration_number="SG55555",
            country="SG",
            business_category="ECOMMERCE",
            email="test@example.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        self.assertFalse(should_require_beneficial_owners(merchant))
        print("✓ Low-risk category does not require beneficial owners")


class SanctionsScreeningTestCase(TestCase):
    """Tests for sanctions screening service."""

    def test_sanctions_match_exact(self):
        """Exact sanctions match should return MATCH status."""
        status, match = screen_entity("Shell Corp Ltd", "SANCTIONS")

        self.assertEqual(status, "MATCH")
        self.assertIsNotNone(match)
        self.assertEqual(match["list"], "OFAC SDN")
        print(f"✓ Exact sanctions match: {match}")

    def test_sanctions_match_partial(self):
        """Partial name match should still trigger MATCH."""
        status, match = screen_entity("Suspicious Trading Co International", "SANCTIONS")

        self.assertEqual(status, "MATCH")
        print(f"✓ Partial sanctions match: {match}")

    def test_sanctions_clear(self):
        """Clean business name should return CLEAR status."""
        status, match = screen_entity("Legitimate Business Inc", "SANCTIONS")

        self.assertEqual(status, "CLEAR")
        self.assertIsNone(match)
        print("✓ Clean business passed sanctions check")

    def test_sanctions_fuzzy_match(self):
        """Similar name should return POTENTIAL_MATCH or MATCH."""
        status, match = screen_entity("Shel Corp Limited", "SANCTIONS")

        self.assertIn(status, ["MATCH", "POTENTIAL_MATCH"])
        print(f"✓ Fuzzy match test: status={status}")

    def test_pep_match(self):
        """PEP name match should be detected."""
        status, match = screen_entity("John Politician", "PEP")

        self.assertEqual(status, "MATCH")
        self.assertIsNotNone(match)
        print(f"✓ PEP match: {match}")

    def test_merchant_screening_creates_results(self):
        """Screening a merchant should create ScreeningResult records."""
        merchant = Merchant.objects.create(
            business_name="Test Company",
            registration_number="TEST001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@example.com",
            phone="+65 1234",
            address="Singapore",
        )

        screen_merchant(merchant)

        self.assertTrue(merchant.screening_results.exists())
        print(f"✓ Screening created {merchant.screening_results.count()} result(s)")


class MerchantAutoApprovalTestCase(TestCase):
    """Tests for auto-approval logic."""

    def test_low_risk_clear_screening_auto_approves(self):
        """LOW risk merchant with CLEAR screening should be auto-approved."""
        merchant = Merchant.objects.create(
            business_name="Clean Tech Pte Ltd",
            registration_number="SG66666",
            country="SG",
            business_category="ECOMMERCE",
            email="test@example.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        # Create risk assessment
        score, factors, risk_level = calculate_risk_score(merchant)
        RiskAssessment.objects.create(
            merchant=merchant,
            risk_score=score,
            risk_factors=factors,
        )
        merchant.risk_level = risk_level
        merchant.save()

        # Test auto-approval eligibility
        result = can_auto_approve(merchant, "CLEAR")

        self.assertTrue(result)
        print("✓ Low-risk clean merchant eligible for auto-approval")

    def test_elevated_risk_cannot_auto_approve(self):
        """Elevated risk (MEDIUM/HIGH) merchant should NOT be auto-approved."""
        merchant = Merchant.objects.create(
            business_name="Crypto Biz",
            registration_number="ID77777",
            country="ID",
            business_category="CRYPTO",
            email="test@example.com",
            phone="+62 812 345",
            address="Indonesia",
        )

        score, factors, risk_level = calculate_risk_score(merchant)
        RiskAssessment.objects.create(
            merchant=merchant,
            risk_score=score,
            risk_factors=factors,
        )
        merchant.risk_level = risk_level
        merchant.save()

        result = can_auto_approve(merchant, "CLEAR")

        self.assertFalse(result)
        self.assertIn(risk_level, ["MEDIUM", "HIGH"])
        print(f"✓ {risk_level}-risk merchant NOT eligible for auto-approval")

    def test_sanctions_match_cannot_auto_approve(self):
        """Merchant with sanctions MATCH should NOT be auto-approved."""
        merchant = Merchant.objects.create(
            business_name="Good Company",
            registration_number="SG88888",
            country="SG",
            business_category="ECOMMERCE",
            email="test@example.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        score, factors, risk_level = calculate_risk_score(merchant)
        RiskAssessment.objects.create(
            merchant=merchant,
            risk_score=score,
            risk_factors=factors,
        )

        result = can_auto_approve(merchant, "MATCH")

        self.assertFalse(result)
        print("✓ Sanctions match prevents auto-approval")


class MerchantRegistrationViewTestCase(TestCase):
    """Tests for merchant registration views."""

    def setUp(self):
        self.client = Client()

    def test_registration_page_loads(self):
        """Registration page should load successfully."""
        response = self.client.get(reverse("register_merchant"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Merchant Registration")
        print("✓ Registration page loads successfully")

    def test_low_risk_registration_auto_approves(self):
        """Submitting low-risk registration should result in APPROVED status."""
        data = {
            "business_name": "Auto Approve Test Ltd",
            "registration_number": "SG99999",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "test@autoapprove.com",
            "phone": "+65 9999 9999",
            "address": "123 Test Street, Singapore",
            "owners-TOTAL_FORMS": "1",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        response = self.client.post(reverse("register_merchant"), data)

        merchant = Merchant.objects.get(registration_number="SG99999")
        self.assertEqual(merchant.status, "APPROVED")
        self.assertEqual(merchant.risk_level, "LOW")
        print(f"✓ Low-risk registration auto-approved: {merchant.status}")

    def test_elevated_risk_registration_pending(self):
        """Submitting elevated-risk registration should result in PENDING status."""
        data = {
            "business_name": "Crypto Test Exchange",
            "registration_number": "ID88888",
            "country": "ID",
            "business_category": "CRYPTO",
            "email": "test@cryptotest.com",
            "phone": "+62 888 8888",
            "address": "Jakarta, Indonesia",
            "owners-TOTAL_FORMS": "1",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        response = self.client.post(reverse("register_merchant"), data)

        merchant = Merchant.objects.get(registration_number="ID88888")
        self.assertEqual(merchant.status, "PENDING")
        self.assertIn(merchant.risk_level, ["MEDIUM", "HIGH"])
        print(f"✓ Elevated-risk registration pending: {merchant.status}, risk={merchant.risk_level}")

    def test_sanctions_match_auto_rejects(self):
        """Registering a sanctioned entity should result in REJECTED status."""
        data = {
            "business_name": "Shell Corp Ltd",
            "registration_number": "XX00001",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "test@shell.com",
            "phone": "+65 0000 0001",
            "address": "Somewhere",
            "owners-TOTAL_FORMS": "1",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        response = self.client.post(reverse("register_merchant"), data)

        merchant = Merchant.objects.get(registration_number="XX00001")
        self.assertEqual(merchant.status, "REJECTED")
        self.assertIn("sanctions", merchant.review_notes.lower())
        print(f"✓ Sanctioned entity auto-rejected: {merchant.review_notes}")

    def test_status_check_page_loads(self):
        """Status check page should load successfully."""
        response = self.client.get(reverse("check_status"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Check Application Status")
        print("✓ Status check page loads successfully")

    def test_status_check_finds_merchant(self):
        """Status check should find and display merchant info."""
        merchant = Merchant.objects.create(
            business_name="Find Me Corp",
            registration_number="FIND123",
            country="SG",
            business_category="ECOMMERCE",
            email="test@findme.com",
            phone="+65 1234 5678",
            address="Singapore",
            status="APPROVED",
        )

        response = self.client.post(
            reverse("check_status"),
            {"registration_number": "FIND123"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Find Me Corp")
        self.assertContains(response, "Approved")
        print("✓ Status check finds merchant successfully")

    def test_dashboard_loads(self):
        """Dashboard should load with statistics."""
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Compliance Dashboard")
        print("✓ Dashboard loads successfully")


class ComplianceOfficerWorkflowTestCase(TestCase):
    """Tests for compliance officer admin workflows."""

    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username="testadmin",
            email="admin@test.com",
            password="testpass123"
        )
        self.client.login(username="testadmin", password="testpass123")

    def test_admin_can_view_merchants(self):
        """Admin should be able to view merchant list."""
        Merchant.objects.create(
            business_name="Admin Test Corp",
            registration_number="ADMIN001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@admin.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        response = self.client.get("/admin/merchants/merchant/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Test Corp")
        print("✓ Admin can view merchant list")

    def test_admin_can_approve_merchant(self):
        """Admin should be able to approve a merchant."""
        merchant = Merchant.objects.create(
            business_name="Approve Me Corp",
            registration_number="APPROVE001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@approve.com",
            phone="+65 1234 5678",
            address="Singapore",
            status="PENDING",
        )

        # Use admin action to approve
        response = self.client.post(
            "/admin/merchants/merchant/",
            {
                "action": "approve_merchants",
                "_selected_action": [merchant.pk],
            }
        )

        merchant.refresh_from_db()
        self.assertEqual(merchant.status, "APPROVED")
        self.assertEqual(merchant.reviewed_by, self.admin_user)
        print(f"✓ Admin approved merchant, reviewed_by={merchant.reviewed_by}")

    def test_admin_can_reject_merchant(self):
        """Admin should be able to reject a merchant."""
        merchant = Merchant.objects.create(
            business_name="Reject Me Corp",
            registration_number="REJECT001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@reject.com",
            phone="+65 1234 5678",
            address="Singapore",
            status="PENDING",
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
        self.assertEqual(merchant.reviewed_by, self.admin_user)
        print(f"✓ Admin rejected merchant, reviewed_by={merchant.reviewed_by}")

    def test_audit_trail_recorded(self):
        """Status changes should record reviewer and timestamp."""
        merchant = Merchant.objects.create(
            business_name="Audit Trail Corp",
            registration_number="AUDIT001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@audit.com",
            phone="+65 1234 5678",
            address="Singapore",
            status="PENDING",
        )

        self.assertIsNone(merchant.reviewed_by)
        self.assertIsNone(merchant.review_date)

        # Approve via admin
        self.client.post(
            "/admin/merchants/merchant/",
            {
                "action": "approve_merchants",
                "_selected_action": [merchant.pk],
            }
        )

        merchant.refresh_from_db()
        self.assertIsNotNone(merchant.reviewed_by)
        self.assertIsNotNone(merchant.review_date)
        print(f"✓ Audit trail: reviewed_by={merchant.reviewed_by}, date={merchant.review_date}")


class IntegrationTestCase(TestCase):
    """End-to-end integration tests."""

    def setUp(self):
        self.client = Client()

    def test_full_low_risk_flow(self):
        """Test complete flow for low-risk merchant: register → auto-approve → check status."""
        # Step 1: Register
        data = {
            "business_name": "Integration Test Low Risk",
            "registration_number": "INT001",
            "country": "SG",
            "business_category": "DIGITAL_SERVICES",
            "email": "integration@test.com",
            "phone": "+65 1111 1111",
            "address": "123 Integration St, Singapore",
            "owners-TOTAL_FORMS": "1",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        response = self.client.post(reverse("register_merchant"), data, follow=True)

        # Step 2: Verify auto-approved
        merchant = Merchant.objects.get(registration_number="INT001")
        self.assertEqual(merchant.status, "APPROVED")

        # Step 3: Verify risk assessment created
        self.assertTrue(merchant.risk_assessments.exists())
        assessment = merchant.get_latest_risk_assessment()
        self.assertLessEqual(assessment.risk_score, 30)

        # Step 4: Verify screening results created
        self.assertTrue(merchant.screening_results.exists())

        # Step 5: Check status page
        response = self.client.get(reverse("merchant_status", args=["INT001"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Approved")

        print("✓ Full low-risk flow completed successfully")

    def test_full_elevated_risk_flow(self):
        """Test complete flow for elevated-risk merchant with manual review."""
        # Step 1: Register elevated-risk merchant
        data = {
            "business_name": "Integration Test High Risk",
            "registration_number": "INT002",
            "country": "ID",
            "business_category": "REMITTANCES",
            "email": "highrisk@test.com",
            "phone": "+62 2222 2222",
            "address": "Jakarta, Indonesia",
            "owners-TOTAL_FORMS": "1",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        self.client.post(reverse("register_merchant"), data)

        # Step 2: Verify pending status
        merchant = Merchant.objects.get(registration_number="INT002")
        self.assertEqual(merchant.status, "PENDING")
        self.assertIn(merchant.risk_level, ["MEDIUM", "HIGH"])

        # Step 3: Verify risk assessment with elevated score
        assessment = merchant.get_latest_risk_assessment()
        self.assertGreater(assessment.risk_score, 30)

        # Step 4: Admin approves
        admin = User.objects.create_superuser("intadmin", "int@admin.com", "pass123")
        self.client.login(username="intadmin", password="pass123")

        self.client.post(
            "/admin/merchants/merchant/",
            {
                "action": "approve_merchants",
                "_selected_action": [merchant.pk],
            }
        )

        # Step 5: Verify approved with audit trail
        merchant.refresh_from_db()
        self.assertEqual(merchant.status, "APPROVED")
        self.assertEqual(merchant.reviewed_by, admin)

        print("✓ Full elevated-risk flow completed successfully")

    def test_full_sanctions_rejection_flow(self):
        """Test complete flow for sanctioned entity: register → auto-reject."""
        data = {
            "business_name": "Suspicious Trading Co",
            "registration_number": "INT003",
            "country": "SG",
            "business_category": "ECOMMERCE",
            "email": "sanctions@test.com",
            "phone": "+65 3333 3333",
            "address": "Singapore",
            "owners-TOTAL_FORMS": "1",
            "owners-INITIAL_FORMS": "0",
            "owners-MIN_NUM_FORMS": "0",
            "owners-MAX_NUM_FORMS": "1000",
        }

        self.client.post(reverse("register_merchant"), data)

        merchant = Merchant.objects.get(registration_number="INT003")

        # Verify auto-rejected
        self.assertEqual(merchant.status, "REJECTED")

        # Verify screening shows match
        sanctions_results = merchant.screening_results.filter(
            screening_type="SANCTIONS",
            status="MATCH"
        )
        self.assertTrue(sanctions_results.exists())

        # Verify status page shows rejection
        response = self.client.get(reverse("merchant_status", args=["INT003"]))
        self.assertContains(response, "Rejected")

        print("✓ Full sanctions rejection flow completed successfully")
