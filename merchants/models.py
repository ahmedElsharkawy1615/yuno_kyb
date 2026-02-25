"""
Merchant models for KYB onboarding.
"""
from django.db import models
from django.contrib.auth.models import User


class Merchant(models.Model):
    """Main merchant entity for KYB onboarding."""

    CATEGORY_CHOICES = [
        ('ECOMMERCE', 'E-commerce (General)'),
        ('DIGITAL_SERVICES', 'Digital Services'),
        ('GAMING', 'Gaming'),
        ('REMITTANCES', 'Remittances/Money Transfer'),
        ('CRYPTO', 'Crypto-adjacent'),
        ('LUXURY', 'High-value Luxury'),
    ]

    RISK_LEVEL_CHOICES = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('UNDER_REVIEW', 'Under Review'),
    ]

    COUNTRY_CHOICES = [
        ('SG', 'Singapore'),
        ('PH', 'Philippines'),
        ('ID', 'Indonesia'),
        ('MY', 'Malaysia'),
        ('TH', 'Thailand'),
        ('VN', 'Vietnam'),
    ]

    # Basic Info
    business_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    business_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    # Contact
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    # Risk & Status
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_merchants')
    review_notes = models.TextField(blank=True)
    review_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Merchant'
        verbose_name_plural = 'Merchants'

    def __str__(self):
        return f"{self.business_name} ({self.registration_number})"

    def get_latest_risk_assessment(self):
        """Get the most recent risk assessment."""
        return self.risk_assessments.order_by('-assessment_date').first()

    def get_screening_status(self):
        """Get overall screening status."""
        results = self.screening_results.all()
        if results.filter(status='MATCH').exists():
            return 'MATCH'
        if results.filter(status='POTENTIAL_MATCH').exists():
            return 'POTENTIAL_MATCH'
        if results.exists():
            return 'CLEAR'
        return 'NOT_SCREENED'


class BeneficialOwner(models.Model):
    """Beneficial owners of a merchant."""

    ID_DOCUMENT_CHOICES = [
        ('PASSPORT', 'Passport'),
        ('NATIONAL_ID', 'National ID'),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='owners')
    full_name = models.CharField(max_length=255)
    nationality = models.CharField(max_length=2)
    ownership_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    id_document_type = models.CharField(max_length=20, choices=ID_DOCUMENT_CHOICES)
    id_document_number = models.CharField(max_length=100)
    is_pep = models.BooleanField(default=False, verbose_name='Politically Exposed Person')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ownership_percentage']
        verbose_name = 'Beneficial Owner'
        verbose_name_plural = 'Beneficial Owners'

    def __str__(self):
        return f"{self.full_name} ({self.ownership_percentage}%)"


class Document(models.Model):
    """Documents uploaded by merchants."""

    DOCUMENT_TYPE_CHOICES = [
        ('BUSINESS_LICENSE', 'Business License'),
        ('REGISTRATION_CERT', 'Registration Certificate'),
        ('ID_PROOF', 'ID Proof'),
        ('ADDRESS_PROOF', 'Address Proof'),
        ('FINANCIAL_STATEMENT', 'Financial Statement'),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    verification_date = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.merchant.business_name}"


class RiskAssessment(models.Model):
    """Risk assessment records for merchants."""

    ASSESSOR_CHOICES = [
        ('SYSTEM', 'Automated System'),
        ('MANUAL', 'Manual Review'),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='risk_assessments')
    risk_score = models.IntegerField()
    risk_factors = models.JSONField(default=list)
    assessment_date = models.DateTimeField(auto_now_add=True)
    assessed_by = models.CharField(max_length=50, choices=ASSESSOR_CHOICES, default='SYSTEM')
    assessor_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-assessment_date']
        verbose_name = 'Risk Assessment'
        verbose_name_plural = 'Risk Assessments'

    def __str__(self):
        return f"Risk Assessment for {self.merchant.business_name}: {self.risk_score}"

    def get_risk_level(self):
        """Convert score to risk level."""
        if self.risk_score <= 30:
            return 'LOW'
        elif self.risk_score <= 60:
            return 'MEDIUM'
        return 'HIGH'
