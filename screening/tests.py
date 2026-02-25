"""
Tests for the screening app.
"""
from django.test import TestCase
from decimal import Decimal

from merchants.models import Merchant, BeneficialOwner
from .models import ScreeningResult
from .services import (
    screen_entity,
    screen_merchant,
    rescreen_merchant,
    calculate_similarity,
    MOCK_SANCTIONS_LIST,
    MOCK_PEP_LIST,
)


class SimilarityCalculationTestCase(TestCase):
    """Tests for string similarity calculation."""

    def test_exact_match_similarity(self):
        """Exact matches should have similarity of 1.0."""
        similarity = calculate_similarity("Shell Corp Ltd", "Shell Corp Ltd")
        self.assertEqual(similarity, 1.0)
        print("✓ Exact match similarity = 1.0")

    def test_case_insensitive_similarity(self):
        """Similarity should be case-insensitive."""
        similarity = calculate_similarity("SHELL CORP LTD", "shell corp ltd")
        self.assertEqual(similarity, 1.0)
        print("✓ Case-insensitive similarity works")

    def test_partial_match_similarity(self):
        """Partial matches should have intermediate similarity."""
        similarity = calculate_similarity("Shell Corp", "Shell Corp Ltd")
        self.assertGreater(similarity, 0.7)
        self.assertLess(similarity, 1.0)
        print(f"✓ Partial match similarity = {similarity:.2f}")

    def test_no_match_similarity(self):
        """Completely different strings should have low similarity."""
        similarity = calculate_similarity("Apple Inc", "Google LLC")
        self.assertLess(similarity, 0.5)
        print(f"✓ No match similarity = {similarity:.2f}")


class ScreenEntityTestCase(TestCase):
    """Tests for single entity screening."""

    def test_all_sanctions_entries_detected(self):
        """All entries in the mock sanctions list should be detected."""
        for entry in MOCK_SANCTIONS_LIST:
            status, match = screen_entity(entry["name"], "SANCTIONS")
            self.assertEqual(status, "MATCH", f"Failed to detect: {entry['name']}")

        print(f"✓ All {len(MOCK_SANCTIONS_LIST)} sanctions entries detected")

    def test_all_pep_entries_detected(self):
        """All entries in the mock PEP list should be detected."""
        for entry in MOCK_PEP_LIST:
            status, match = screen_entity(entry["name"], "PEP")
            self.assertEqual(status, "MATCH", f"Failed to detect: {entry['name']}")

        print(f"✓ All {len(MOCK_PEP_LIST)} PEP entries detected")

    def test_clean_names_pass_screening(self):
        """Clean business names should pass screening."""
        clean_names = [
            "Acme Corporation",
            "Blue Sky Technologies",
            "Global Solutions Inc",
            "Happy Customers Ltd",
            "Good Morning Bakery",
        ]

        for name in clean_names:
            status, _ = screen_entity(name, "SANCTIONS")
            self.assertEqual(status, "CLEAR", f"False positive for: {name}")

        print(f"✓ All {len(clean_names)} clean names passed screening")

    def test_substring_match_detected(self):
        """Names containing sanctioned entity as substring should be detected."""
        status, match = screen_entity("The Shell Corp Ltd Holdings", "SANCTIONS")
        self.assertEqual(status, "MATCH")
        print("✓ Substring match detected")

    def test_screening_returns_list_info(self):
        """Matched results should include which list was matched."""
        status, match = screen_entity("Shell Corp Ltd", "SANCTIONS")

        self.assertIn("list", match)
        self.assertEqual(match["list"], "OFAC SDN")
        print(f"✓ Match includes list info: {match['list']}")


class ScreenMerchantTestCase(TestCase):
    """Tests for full merchant screening."""

    def test_clean_merchant_returns_clear(self):
        """Merchant with no matches should return CLEAR."""
        merchant = Merchant.objects.create(
            business_name="Legitimate Business Inc",
            registration_number="CLEAN001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@legitimate.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        status = screen_merchant(merchant)

        self.assertEqual(status, "CLEAR")
        self.assertTrue(merchant.screening_results.filter(status="CLEAR").exists())
        print("✓ Clean merchant screening returns CLEAR")

    def test_sanctioned_merchant_returns_match(self):
        """Merchant matching sanctions list should return MATCH."""
        merchant = Merchant.objects.create(
            business_name="Shell Corp Ltd",
            registration_number="SANC001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@shell.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        status = screen_merchant(merchant)

        self.assertEqual(status, "MATCH")
        self.assertTrue(merchant.screening_results.filter(status="MATCH").exists())
        print("✓ Sanctioned merchant screening returns MATCH")

    def test_beneficial_owners_screened(self):
        """Beneficial owners should also be screened."""
        merchant = Merchant.objects.create(
            business_name="Clean Company",
            registration_number="OWNER001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@clean.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        # Add clean owner
        BeneficialOwner.objects.create(
            merchant=merchant,
            full_name="Jane Doe",
            nationality="SG",
            ownership_percentage=Decimal("100.00"),
            id_document_type="PASSPORT",
            id_document_number="E1234567",
            is_pep=False,
        )

        screen_merchant(merchant)

        # Should have screening results for both business and owner
        owner_results = merchant.screening_results.filter(
            screened_entity__contains="Owner"
        )
        self.assertTrue(owner_results.exists())
        print(f"✓ Beneficial owner screened: {owner_results.count()} result(s)")

    def test_sanctioned_owner_triggers_match(self):
        """Sanctioned beneficial owner should trigger MATCH status."""
        merchant = Merchant.objects.create(
            business_name="Front Company Inc",
            registration_number="FRONT001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@front.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        # Add owner matching sanctions list
        BeneficialOwner.objects.create(
            merchant=merchant,
            full_name="Shell Corp Ltd",  # This matches sanctions list
            nationality="SG",
            ownership_percentage=Decimal("100.00"),
            id_document_type="PASSPORT",
            id_document_number="E1234567",
            is_pep=False,
        )

        status = screen_merchant(merchant)

        self.assertEqual(status, "MATCH")
        print("✓ Sanctioned owner triggers MATCH")

    def test_pep_owner_triggers_potential_match(self):
        """PEP owner should trigger POTENTIAL_MATCH for review."""
        merchant = Merchant.objects.create(
            business_name="Political Holdings",
            registration_number="PEP001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@political.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        # Add owner matching PEP list
        BeneficialOwner.objects.create(
            merchant=merchant,
            full_name="John Politician",
            nationality="PH",
            ownership_percentage=Decimal("51.00"),
            id_document_type="PASSPORT",
            id_document_number="PH1234567",
            is_pep=True,
        )

        status = screen_merchant(merchant)

        # PEP match should flag for review but not auto-reject
        self.assertIn(status, ["POTENTIAL_MATCH", "MATCH"])
        print(f"✓ PEP owner triggers: {status}")

    def test_screening_creates_multiple_results(self):
        """Screening should create results for each check performed."""
        merchant = Merchant.objects.create(
            business_name="Multi Check Corp",
            registration_number="MULTI001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@multi.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        # Add two owners
        for i in range(2):
            BeneficialOwner.objects.create(
                merchant=merchant,
                full_name=f"Owner {i+1}",
                nationality="SG",
                ownership_percentage=Decimal("50.00"),
                id_document_type="PASSPORT",
                id_document_number=f"E{i+1}",
                is_pep=False,
            )

        screen_merchant(merchant)

        # Should have: 1 business sanctions + 2 owner sanctions + 2 owner PEP = 5 results
        result_count = merchant.screening_results.count()
        self.assertEqual(result_count, 5)
        print(f"✓ Multiple screening results created: {result_count}")


class RescreenMerchantTestCase(TestCase):
    """Tests for merchant rescreening functionality."""

    def test_rescreen_clears_old_results(self):
        """Rescreening should clear previous results."""
        merchant = Merchant.objects.create(
            business_name="Rescreen Test",
            registration_number="RESCAN001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@rescreen.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        # Initial screening
        screen_merchant(merchant)
        initial_count = merchant.screening_results.count()
        initial_ids = list(merchant.screening_results.values_list("id", flat=True))

        # Rescreen
        rescreen_merchant(merchant)

        # Should have new results
        new_count = merchant.screening_results.count()
        new_ids = list(merchant.screening_results.values_list("id", flat=True))

        self.assertEqual(initial_count, new_count)
        self.assertFalse(set(initial_ids) & set(new_ids))  # No overlap
        print("✓ Rescreening clears old results and creates new ones")


class ScreeningResultModelTestCase(TestCase):
    """Tests for ScreeningResult model."""

    def test_screening_result_str(self):
        """ScreeningResult should have readable string representation."""
        merchant = Merchant.objects.create(
            business_name="String Test Corp",
            registration_number="STR001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@string.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        result = ScreeningResult.objects.create(
            merchant=merchant,
            screening_type="SANCTIONS",
            status="CLEAR",
            screened_entity="String Test Corp",
        )

        self.assertIn("Sanctions", str(result))
        self.assertIn("String Test Corp", str(result))
        print(f"✓ ScreeningResult str: {result}")

    def test_screening_result_ordering(self):
        """ScreeningResults should be ordered by screened_at descending."""
        merchant = Merchant.objects.create(
            business_name="Order Test Corp",
            registration_number="ORD001",
            country="SG",
            business_category="ECOMMERCE",
            email="test@order.com",
            phone="+65 1234 5678",
            address="Singapore",
        )

        # Create results
        for i in range(3):
            ScreeningResult.objects.create(
                merchant=merchant,
                screening_type="SANCTIONS",
                status="CLEAR",
                screened_entity=f"Entity {i+1}",
            )

        results = list(merchant.screening_results.all())

        # Most recent should be first
        for i in range(len(results) - 1):
            self.assertGreaterEqual(
                results[i].screened_at,
                results[i+1].screened_at
            )

        print("✓ ScreeningResults ordered correctly")
