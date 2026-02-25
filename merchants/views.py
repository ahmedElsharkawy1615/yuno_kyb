"""
Views for merchant KYB onboarding.
"""
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

from .models import Merchant, RiskAssessment
from .forms import (
    MerchantRegistrationForm,
    BeneficialOwnerFormSet,
    MerchantStatusCheckForm,
)
from .risk_engine import calculate_risk_score, can_auto_approve
from screening.services import screen_merchant

logger = logging.getLogger(__name__)


def home(request):
    """Home page with navigation options."""
    return render(request, 'merchants/home.html')


def register_merchant(request):
    """Handle merchant registration."""
    if request.method == 'POST':
        form = MerchantRegistrationForm(request.POST)
        owner_formset = BeneficialOwnerFormSet(request.POST, prefix='owners')

        if form.is_valid() and owner_formset.is_valid():
            with transaction.atomic():
                # Save merchant
                merchant = form.save(commit=False)
                merchant.status = 'PENDING'
                merchant.save()

                # Save beneficial owners
                owner_formset.instance = merchant
                owner_formset.save()

                # Calculate risk score
                score, factors, risk_level = calculate_risk_score(merchant)

                # Create risk assessment
                RiskAssessment.objects.create(
                    merchant=merchant,
                    risk_score=score,
                    risk_factors=factors,
                    assessed_by='SYSTEM',
                )

                # Update merchant risk level
                merchant.risk_level = risk_level
                merchant.save()

                # Run sanctions screening
                screening_status = screen_merchant(merchant)

                # Determine status based on screening and risk
                if screening_status == 'MATCH':
                    merchant.status = 'REJECTED'
                    merchant.review_notes = 'Auto-rejected due to sanctions match.'
                    logger.warning(f"Merchant {merchant.business_name} auto-rejected: sanctions match")
                elif screening_status == 'POTENTIAL_MATCH':
                    merchant.status = 'UNDER_REVIEW'
                    logger.info(f"Merchant {merchant.business_name} queued for review: potential sanctions match")
                elif can_auto_approve(merchant, screening_status):
                    merchant.status = 'APPROVED'
                    merchant.review_notes = 'Auto-approved: Low risk, clear screening.'
                    logger.info(f"Merchant {merchant.business_name} auto-approved: low risk")
                else:
                    merchant.status = 'PENDING'
                    logger.info(f"Merchant {merchant.business_name} pending review: {risk_level} risk")

                merchant.save()

                messages.success(
                    request,
                    f'Registration submitted successfully. Your reference number is: {merchant.registration_number}'
                )
                return redirect('merchant_status', registration_number=merchant.registration_number)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MerchantRegistrationForm()
        owner_formset = BeneficialOwnerFormSet(prefix='owners')

    return render(request, 'merchants/register.html', {
        'form': form,
        'owner_formset': owner_formset,
    })


def check_status(request):
    """Check merchant status by registration number."""
    merchant = None

    if request.method == 'POST':
        form = MerchantStatusCheckForm(request.POST)
        if form.is_valid():
            registration_number = form.cleaned_data['registration_number']
            try:
                merchant = Merchant.objects.get(registration_number=registration_number)
            except Merchant.DoesNotExist:
                messages.error(request, 'No merchant found with that registration number.')
    else:
        form = MerchantStatusCheckForm()

    return render(request, 'merchants/check_status.html', {
        'form': form,
        'merchant': merchant,
    })


def merchant_status(request, registration_number):
    """Display merchant status page."""
    merchant = get_object_or_404(Merchant, registration_number=registration_number)
    risk_assessment = merchant.get_latest_risk_assessment()
    screening_results = merchant.screening_results.all()

    return render(request, 'merchants/status.html', {
        'merchant': merchant,
        'risk_assessment': risk_assessment,
        'screening_results': screening_results,
    })


def dashboard(request):
    """Compliance dashboard with statistics."""
    merchants = Merchant.objects.all()

    stats = {
        'total': merchants.count(),
        'pending': merchants.filter(status='PENDING').count(),
        'under_review': merchants.filter(status='UNDER_REVIEW').count(),
        'approved': merchants.filter(status='APPROVED').count(),
        'rejected': merchants.filter(status='REJECTED').count(),
        'high_risk': merchants.filter(risk_level='HIGH').count(),
        'medium_risk': merchants.filter(risk_level='MEDIUM').count(),
        'low_risk': merchants.filter(risk_level='LOW').count(),
    }

    # Recent pending merchants
    pending_merchants = merchants.filter(
        status__in=['PENDING', 'UNDER_REVIEW']
    ).order_by('-created_at')[:10]

    # Recent activity
    recent_merchants = merchants.order_by('-updated_at')[:5]

    return render(request, 'merchants/dashboard.html', {
        'stats': stats,
        'pending_merchants': pending_merchants,
        'recent_merchants': recent_merchants,
    })
