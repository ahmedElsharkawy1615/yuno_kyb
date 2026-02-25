"""
Sanctions screening services.
"""
import logging
from difflib import SequenceMatcher

from .models import ScreeningResult

logger = logging.getLogger(__name__)

# Mock sanctions list for demonstration
MOCK_SANCTIONS_LIST = [
    {"name": "Shell Corp Ltd", "list": "OFAC SDN", "type": "SANCTIONS"},
    {"name": "Suspicious Trading Co", "list": "UN Sanctions", "type": "SANCTIONS"},
    {"name": "Blacklisted Enterprises", "list": "EU Sanctions", "type": "SANCTIONS"},
    {"name": "Fraudulent Services Inc", "list": "OFAC SDN", "type": "SANCTIONS"},
    {"name": "Money Laundering Network", "list": "FATF Blacklist", "type": "SANCTIONS"},
    {"name": "Terrorist Funding Corp", "list": "UN Sanctions", "type": "SANCTIONS"},
]

# Mock PEP list
MOCK_PEP_LIST = [
    {"name": "John Politician", "position": "Former Minister", "country": "PH"},
    {"name": "Maria Governor", "position": "Regional Governor", "country": "ID"},
    {"name": "Robert Senator", "position": "Senator", "country": "SG"},
]

# Similarity threshold for fuzzy matching
SIMILARITY_THRESHOLD = 0.8
POTENTIAL_MATCH_THRESHOLD = 0.6


def calculate_similarity(name1, name2):
    """Calculate string similarity between two names."""
    return SequenceMatcher(None, name1.lower(), name2.lower()).ratio()


def screen_entity(name, screening_type='SANCTIONS'):
    """
    Screen a name against sanctions/PEP lists.

    Args:
        name: Name to screen
        screening_type: 'SANCTIONS' or 'PEP'

    Returns:
        tuple: (status, match_details)
    """
    name_lower = name.lower().strip()

    if screening_type == 'SANCTIONS':
        check_list = MOCK_SANCTIONS_LIST
    else:
        check_list = MOCK_PEP_LIST

    best_match = None
    best_similarity = 0

    for entry in check_list:
        entry_name = entry["name"].lower()

        # Exact match
        if entry_name in name_lower or name_lower in entry_name:
            logger.warning(f"Sanctions MATCH found: {name} matches {entry['name']}")
            return "MATCH", entry

        # Fuzzy match
        similarity = calculate_similarity(name_lower, entry_name)
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = entry

    # Check thresholds
    if best_similarity >= SIMILARITY_THRESHOLD:
        logger.warning(f"Sanctions MATCH found (fuzzy): {name} matches {best_match['name']} ({best_similarity:.2f})")
        return "MATCH", best_match
    elif best_similarity >= POTENTIAL_MATCH_THRESHOLD:
        logger.info(f"Potential sanctions match: {name} similar to {best_match['name']} ({best_similarity:.2f})")
        return "POTENTIAL_MATCH", best_match

    return "CLEAR", None


def screen_merchant(merchant):
    """
    Run full screening on a merchant.

    Returns:
        str: Overall screening status ('CLEAR', 'MATCH', 'POTENTIAL_MATCH')
    """
    overall_status = 'CLEAR'

    # Screen business name
    status, match = screen_entity(merchant.business_name, 'SANCTIONS')
    ScreeningResult.objects.create(
        merchant=merchant,
        screening_type='SANCTIONS',
        status=status,
        matched_list=match.get('list', '') if match else '',
        match_details=match or {},
        screened_entity=merchant.business_name,
    )

    if status == 'MATCH':
        overall_status = 'MATCH'
    elif status == 'POTENTIAL_MATCH' and overall_status != 'MATCH':
        overall_status = 'POTENTIAL_MATCH'

    # Screen beneficial owners
    for owner in merchant.owners.all():
        # Sanctions check
        status, match = screen_entity(owner.full_name, 'SANCTIONS')
        ScreeningResult.objects.create(
            merchant=merchant,
            screening_type='SANCTIONS',
            status=status,
            matched_list=match.get('list', '') if match else '',
            match_details=match or {},
            screened_entity=f"Owner: {owner.full_name}",
        )

        if status == 'MATCH':
            overall_status = 'MATCH'
        elif status == 'POTENTIAL_MATCH' and overall_status != 'MATCH':
            overall_status = 'POTENTIAL_MATCH'

        # PEP check
        status, match = screen_entity(owner.full_name, 'PEP')
        ScreeningResult.objects.create(
            merchant=merchant,
            screening_type='PEP',
            status=status,
            matched_list=match.get('position', '') if match else '',
            match_details=match or {},
            screened_entity=f"Owner: {owner.full_name}",
        )

        # PEP match doesn't auto-reject but flags for review
        if status in ['MATCH', 'POTENTIAL_MATCH'] and overall_status == 'CLEAR':
            overall_status = 'POTENTIAL_MATCH'

    logger.info(f"Screening complete for {merchant.business_name}: {overall_status}")
    return overall_status


def rescreen_merchant(merchant):
    """
    Re-run screening for an existing merchant.
    Useful for periodic rescreening requirements.
    """
    # Clear old results
    merchant.screening_results.all().delete()

    # Run new screening
    return screen_merchant(merchant)
