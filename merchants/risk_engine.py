"""
Risk scoring engine for merchant KYB.
"""
import logging

logger = logging.getLogger(__name__)

# Business category risk weights (base score contribution)
CATEGORY_WEIGHTS = {
    'ECOMMERCE': 10,
    'DIGITAL_SERVICES': 15,
    'GAMING': 40,
    'REMITTANCES': 80,
    'CRYPTO': 90,
    'LUXURY': 50,
}

# Country risk weights
COUNTRY_WEIGHTS = {
    'SG': 10,  # Singapore - Low risk
    'MY': 20,  # Malaysia - Low-Medium
    'TH': 25,  # Thailand - Medium
    'PH': 30,  # Philippines - Medium
    'VN': 40,  # Vietnam - Medium-High
    'ID': 50,  # Indonesia - High
}

# Risk level thresholds
RISK_THRESHOLDS = {
    'LOW': 30,
    'MEDIUM': 60,
    'HIGH': 100,
}


def calculate_risk_score(merchant):
    """
    Calculate risk score for a merchant.

    Returns:
        tuple: (score: int, factors: list, risk_level: str)
    """
    score = 0
    factors = []

    # Business category weight (40% of score)
    category_weight = CATEGORY_WEIGHTS.get(merchant.business_category, 50)
    category_contribution = category_weight * 0.4
    score += category_contribution

    if category_weight >= 80:
        factors.append(f"High-risk business category: {merchant.get_business_category_display()}")
    elif category_weight >= 40:
        factors.append(f"Medium-risk business category: {merchant.get_business_category_display()}")

    # Country risk (30% of score)
    country_weight = COUNTRY_WEIGHTS.get(merchant.country, 30)
    country_contribution = country_weight * 0.3
    score += country_contribution

    if country_weight >= 40:
        factors.append(f"Higher-risk jurisdiction: {merchant.get_country_display()}")

    # Beneficial ownership complexity (15% of score)
    owners = merchant.owners.all()
    small_shareholders = owners.filter(ownership_percentage__lt=25).count()

    if small_shareholders > 3:
        score += 15
        factors.append(f"Complex ownership structure: {small_shareholders} shareholders with <25% ownership")
    elif small_shareholders > 1:
        score += 8
        factors.append(f"Multiple minority shareholders: {small_shareholders}")

    # PEP exposure (15% of score)
    pep_owners = owners.filter(is_pep=True)
    if pep_owners.exists():
        pep_count = pep_owners.count()
        score += 15
        factors.append(f"PEP involvement: {pep_count} politically exposed person(s)")

    # Determine risk level
    score = min(int(score), 100)  # Cap at 100

    if score <= RISK_THRESHOLDS['LOW']:
        risk_level = 'LOW'
    elif score <= RISK_THRESHOLDS['MEDIUM']:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'HIGH'

    logger.info(f"Risk assessment for {merchant.business_name}: score={score}, level={risk_level}, factors={factors}")

    return score, factors, risk_level


def should_require_beneficial_owners(merchant):
    """
    Determine if merchant registration should require beneficial owner info.
    High-risk merchants always require beneficial ownership details.
    """
    category_weight = CATEGORY_WEIGHTS.get(merchant.business_category, 50)
    country_weight = COUNTRY_WEIGHTS.get(merchant.country, 30)

    # Require for high-risk categories or countries
    if category_weight >= 40 or country_weight >= 40:
        return True

    return False


def get_due_diligence_level(risk_level):
    """
    Get the required due diligence level based on risk.

    Returns:
        str: 'SIMPLIFIED', 'STANDARD', or 'ENHANCED'
    """
    if risk_level == 'LOW':
        return 'SIMPLIFIED'
    elif risk_level == 'MEDIUM':
        return 'STANDARD'
    return 'ENHANCED'


def can_auto_approve(merchant, screening_status):
    """
    Determine if a merchant can be auto-approved.

    Only LOW risk merchants with CLEAR screening can be auto-approved.
    """
    if screening_status != 'CLEAR':
        return False

    assessment = merchant.get_latest_risk_assessment()
    if not assessment:
        return False

    return assessment.get_risk_level() == 'LOW'
