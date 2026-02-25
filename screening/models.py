"""
Models for sanctions screening.
"""
from django.db import models
from merchants.models import Merchant


class ScreeningResult(models.Model):
    """Results from sanctions/AML screening."""

    SCREENING_TYPE_CHOICES = [
        ('SANCTIONS', 'Sanctions Check'),
        ('PEP', 'PEP Check'),
        ('ADVERSE_MEDIA', 'Adverse Media'),
    ]

    STATUS_CHOICES = [
        ('CLEAR', 'Clear'),
        ('MATCH', 'Match Found'),
        ('POTENTIAL_MATCH', 'Potential Match'),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='screening_results')
    screening_type = models.CharField(max_length=20, choices=SCREENING_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    matched_list = models.CharField(max_length=100, blank=True)
    match_details = models.JSONField(default=dict)
    screened_at = models.DateTimeField(auto_now_add=True)
    screened_entity = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-screened_at']
        verbose_name = 'Screening Result'
        verbose_name_plural = 'Screening Results'

    def __str__(self):
        return f"{self.get_screening_type_display()} - {self.merchant.business_name}: {self.status}"


class SanctionsList(models.Model):
    """Reference table for sanctions lists."""

    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    last_updated = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Sanctions List'
        verbose_name_plural = 'Sanctions Lists'

    def __str__(self):
        return f"{self.name} ({self.source})"
