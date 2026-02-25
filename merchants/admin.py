"""
Admin configuration for merchant KYB.
"""
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.contrib import messages

from .models import Merchant, BeneficialOwner, Document, RiskAssessment
from screening.models import ScreeningResult


class BeneficialOwnerInline(admin.TabularInline):
    """Inline admin for beneficial owners."""
    model = BeneficialOwner
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('full_name', 'nationality', 'ownership_percentage', 'id_document_type', 'id_document_number', 'is_pep')


class DocumentInline(admin.TabularInline):
    """Inline admin for documents."""
    model = Document
    extra = 0
    readonly_fields = ('uploaded_at', 'verified_by', 'verification_date')
    fields = ('document_type', 'file', 'uploaded_at', 'verified', 'verified_by', 'verification_notes')


class ScreeningResultInline(admin.TabularInline):
    """Inline admin for screening results."""
    model = ScreeningResult
    extra = 0
    readonly_fields = ('screening_type', 'status', 'matched_list', 'match_details', 'screened_at')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class RiskAssessmentInline(admin.TabularInline):
    """Inline admin for risk assessments."""
    model = RiskAssessment
    extra = 0
    readonly_fields = ('risk_score', 'risk_factors', 'assessment_date', 'assessed_by', 'assessor_user')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    """Admin for merchants with approval workflow."""

    list_display = (
        'business_name',
        'registration_number',
        'country',
        'business_category',
        'risk_level_display',
        'status_display',
        'created_at',
    )

    list_filter = ('status', 'risk_level', 'country', 'business_category')
    search_fields = ('business_name', 'registration_number', 'email')
    readonly_fields = ('created_at', 'updated_at', 'reviewed_by', 'review_date')

    fieldsets = (
        ('Business Information', {
            'fields': ('business_name', 'registration_number', 'country', 'business_category')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Risk & Status', {
            'fields': ('risk_level', 'status')
        }),
        ('Review Information', {
            'fields': ('review_notes', 'reviewed_by', 'review_date'),
            'classes': ('collapse',)
        }),
        ('Audit Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [BeneficialOwnerInline, DocumentInline, ScreeningResultInline, RiskAssessmentInline]

    actions = ['approve_merchants', 'reject_merchants', 'mark_under_review']

    def risk_level_display(self, obj):
        """Display risk level with color coding."""
        colors = {
            'LOW': 'green',
            'MEDIUM': 'orange',
            'HIGH': 'red',
        }
        color = colors.get(obj.risk_level, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_risk_level_display()
        )
    risk_level_display.short_description = 'Risk Level'
    risk_level_display.admin_order_field = 'risk_level'

    def status_display(self, obj):
        """Display status with color coding."""
        colors = {
            'PENDING': 'orange',
            'APPROVED': 'green',
            'REJECTED': 'red',
            'UNDER_REVIEW': 'blue',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'

    def approve_merchants(self, request, queryset):
        """Bulk approve selected merchants."""
        count = 0
        for merchant in queryset:
            if merchant.status in ['PENDING', 'UNDER_REVIEW']:
                merchant.status = 'APPROVED'
                merchant.reviewed_by = request.user
                merchant.review_date = timezone.now()
                merchant.save()
                count += 1

        self.message_user(
            request,
            f'{count} merchant(s) approved successfully.',
            messages.SUCCESS
        )
    approve_merchants.short_description = 'Approve selected merchants'

    def reject_merchants(self, request, queryset):
        """Bulk reject selected merchants."""
        count = 0
        for merchant in queryset:
            if merchant.status in ['PENDING', 'UNDER_REVIEW']:
                merchant.status = 'REJECTED'
                merchant.reviewed_by = request.user
                merchant.review_date = timezone.now()
                merchant.save()
                count += 1

        self.message_user(
            request,
            f'{count} merchant(s) rejected.',
            messages.WARNING
        )
    reject_merchants.short_description = 'Reject selected merchants'

    def mark_under_review(self, request, queryset):
        """Mark selected merchants for review."""
        count = queryset.filter(status='PENDING').update(status='UNDER_REVIEW')
        self.message_user(
            request,
            f'{count} merchant(s) marked for review.',
            messages.INFO
        )
    mark_under_review.short_description = 'Mark for review'

    def save_model(self, request, obj, form, change):
        """Track who reviewed the merchant."""
        if change and 'status' in form.changed_data:
            obj.reviewed_by = request.user
            obj.review_date = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(BeneficialOwner)
class BeneficialOwnerAdmin(admin.ModelAdmin):
    """Admin for beneficial owners."""
    list_display = ('full_name', 'merchant', 'ownership_percentage', 'is_pep')
    list_filter = ('is_pep', 'nationality')
    search_fields = ('full_name', 'merchant__business_name')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin for documents."""
    list_display = ('merchant', 'document_type', 'uploaded_at', 'verified')
    list_filter = ('document_type', 'verified')
    search_fields = ('merchant__business_name',)
    readonly_fields = ('uploaded_at',)

    actions = ['verify_documents']

    def verify_documents(self, request, queryset):
        """Bulk verify documents."""
        count = queryset.filter(verified=False).update(
            verified=True,
            verified_by=request.user,
            verification_date=timezone.now()
        )
        self.message_user(request, f'{count} document(s) verified.')
    verify_documents.short_description = 'Verify selected documents'


@admin.register(RiskAssessment)
class RiskAssessmentAdmin(admin.ModelAdmin):
    """Admin for risk assessments."""
    list_display = ('merchant', 'risk_score', 'assessed_by', 'assessment_date')
    list_filter = ('assessed_by',)
    search_fields = ('merchant__business_name',)
    readonly_fields = ('assessment_date',)
