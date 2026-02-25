# Yuno KYB - Know Your Business Onboarding System

A comprehensive **Know Your Business (KYB)** compliance system designed to screen and onboard merchants before they can process payments through Yuno's payment orchestration platform.

---

## Table of Contents

- [The Problem](#the-problem)
- [The Solution](#the-solution)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Risk Scoring Engine](#risk-scoring-engine)
- [Sanctions Screening](#sanctions-screening)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [API Reference](#api-reference)
- [Admin Panel](#admin-panel)
- [Project Structure](#project-structure)

---

## The Problem

### Background

Yuno is a payment orchestration platform that enables merchants to connect with multiple payment providers through a single integration. As Yuno expands into **Southeast Asian markets** (Singapore, Philippines, Indonesia), it faces critical compliance challenges.

### Regulatory Compliance Gaps

Payment service providers in these jurisdictions are subject to strict Anti-Money Laundering (AML) and Counter-Terrorism Financing (CTF) regulations:

| Jurisdiction | Regulatory Body | Key Requirements |
|--------------|-----------------|------------------|
| **Singapore** | MAS (Monetary Authority of Singapore) | Payment Services Act 2019, AML/CFT Notice PSN01 |
| **Philippines** | BSP (Bangko Sentral ng Pilipinas) | AMLA, BSP Circular 706 |
| **Indonesia** | OJK (Otoritas Jasa Keuangan) | POJK regulations, AML requirements |

### Key Compliance Requirements

1. **Merchant Due Diligence** - Verify business legitimacy before onboarding
2. **Beneficial Ownership** - Identify ultimate beneficial owners (UBOs) with >25% ownership
3. **Sanctions Screening** - Check against OFAC, UN, EU, and local sanctions lists
4. **PEP Screening** - Identify Politically Exposed Persons
5. **Risk Assessment** - Categorize merchants by risk level
6. **Ongoing Monitoring** - Periodic re-screening and transaction monitoring
7. **Audit Trail** - Maintain records for regulatory examinations

### Business Risks Without KYB

- **Regulatory Fines**: Up to SGD 1 million per violation in Singapore
- **License Revocation**: Risk of losing payment service provider license
- **Reputational Damage**: Association with money laundering or terrorist financing
- **Legal Liability**: Personal liability for compliance officers and directors

---

## The Solution

### Yuno KYB System

A web-based KYB onboarding platform that automates merchant screening and compliance workflows:

```
┌─────────────────────────────────────────────────────────────────┐
│                     MERCHANT REGISTRATION                        │
│  Business Info → Beneficial Owners → Document Upload             │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RISK ASSESSMENT                             │
│  Category Risk + Country Risk + Ownership Complexity + PEP       │
│                          │                                       │
│              ┌───────────┼───────────┐                          │
│              ▼           ▼           ▼                          │
│           LOW         MEDIUM       HIGH                          │
│         (0-30)       (31-60)     (61-100)                       │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SANCTIONS SCREENING                            │
│  Business Name + Beneficial Owners vs OFAC/UN/EU Lists          │
│                          │                                       │
│              ┌───────────┼───────────┐                          │
│              ▼           ▼           ▼                          │
│           CLEAR     POTENTIAL      MATCH                         │
│                       MATCH                                      │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DECISION ENGINE                               │
│                                                                  │
│  LOW Risk + CLEAR Screen  ──────────►  AUTO-APPROVE             │
│  MEDIUM/HIGH Risk + CLEAR ──────────►  MANUAL REVIEW            │
│  Any Risk + POTENTIAL     ──────────►  MANUAL REVIEW            │
│  Any Risk + MATCH         ──────────►  AUTO-REJECT              │
└─────────────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Risk-Based Approach** - Proportional due diligence based on risk level
2. **Automation First** - Auto-approve low-risk, auto-reject sanctioned entities
3. **Audit Everything** - Complete trail of all decisions and actions
4. **Compliance Officer Friendly** - Intuitive admin interface for manual reviews

---

## Key Features

### For Merchants

- **Self-Service Registration** - Web form for business information submission
- **Real-Time Status** - Check application status anytime
- **Clear Requirements** - Guidance on required documents and information

### For Compliance Officers

- **Risk Dashboard** - Overview of pending reviews and statistics
- **Bulk Actions** - Approve or reject multiple merchants
- **Detailed Records** - View risk factors, screening results, documents
- **Audit Trail** - Track who reviewed what and when

### Automated Capabilities

- **Risk Scoring** - Algorithm-based risk assessment
- **Sanctions Screening** - Name matching against sanctions lists
- **PEP Detection** - Identify politically exposed persons
- **Auto-Decisioning** - Approve/reject based on configurable rules

---

## System Architecture

### Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.11+ / Django 5.x | Web framework, ORM, Admin |
| **Database** | SQLite (dev) / PostgreSQL (prod) | Data persistence |
| **Frontend** | Django Templates + Bootstrap 5 | User interface |
| **Admin** | Django Admin | Compliance officer interface |

### Data Models

```
┌─────────────────┐       ┌──────────────────┐
│    Merchant     │       │  BeneficialOwner │
├─────────────────┤       ├──────────────────┤
│ business_name   │──┐    │ full_name        │
│ registration_no │  │    │ nationality      │
│ country         │  │    │ ownership_%      │
│ category        │  └───►│ id_document      │
│ risk_level      │       │ is_pep           │
│ status          │       └──────────────────┘
└────────┬────────┘
         │
         │         ┌──────────────────┐
         ├────────►│  RiskAssessment  │
         │         ├──────────────────┤
         │         │ risk_score       │
         │         │ risk_factors[]   │
         │         │ assessed_by      │
         │         └──────────────────┘
         │
         │         ┌──────────────────┐
         └────────►│ ScreeningResult  │
                   ├──────────────────┤
                   │ screening_type   │
                   │ status           │
                   │ matched_list     │
                   │ match_details    │
                   └──────────────────┘
```

---

## Risk Scoring Engine

### How Risk is Calculated

The risk score (0-100) is composed of multiple weighted factors:

```python
Total Score = Category Risk (40%) + Country Risk (30%) + Ownership (15%) + PEP (15%)
```

### Business Category Risk Weights

| Category | Weight | Reason |
|----------|--------|--------|
| E-commerce (General) | 10 | Standard retail, low risk |
| Digital Services | 15 | Software, SaaS, low risk |
| Gaming | 40 | Virtual goods, moderate risk |
| High-value Luxury | 50 | Potential laundering vehicle |
| Remittances/Money Transfer | 80 | High AML risk |
| Crypto-adjacent | 90 | Highest regulatory scrutiny |

### Country Risk Weights

| Country | Weight | Rationale |
|---------|--------|-----------|
| Singapore | 10 | Strong AML framework, FATF compliant |
| Malaysia | 20 | Developing AML framework |
| Thailand | 25 | Moderate risk jurisdiction |
| Philippines | 30 | Higher remittance activity |
| Vietnam | 40 | Emerging regulatory framework |
| Indonesia | 50 | Complex regulatory environment |

### Additional Risk Factors

| Factor | Points | Trigger |
|--------|--------|---------|
| Complex Ownership | +15 | More than 3 shareholders with <25% ownership |
| Multiple Minority Shareholders | +8 | 2-3 shareholders with <25% ownership |
| PEP Involvement | +15 | Any beneficial owner is a PEP |

### Risk Level Thresholds

| Level | Score Range | Due Diligence | Auto-Approve |
|-------|-------------|---------------|--------------|
| **LOW** | 0-30 | Simplified | Yes (if screening clear) |
| **MEDIUM** | 31-60 | Standard | No - Manual review |
| **HIGH** | 61-100 | Enhanced | No - Manual review |

### Example Calculations

**Example 1: Low Risk**
```
TechShop Singapore (E-commerce in Singapore)
- Category: E-commerce (10) × 0.4 = 4
- Country: Singapore (10) × 0.3 = 3
- Total: 7 → LOW RISK → Auto-approved
```

**Example 2: High Risk**
```
CryptoExchange Indonesia (Crypto in Indonesia)
- Category: Crypto (90) × 0.4 = 36
- Country: Indonesia (50) × 0.3 = 15
- Total: 51 → MEDIUM RISK → Manual review required
```

**Example 3: Maximum Risk**
```
Crypto + Indonesia + Complex Ownership + PEP
- Category: 36 + Country: 15 + Ownership: 15 + PEP: 15
- Total: 81 → HIGH RISK → Enhanced due diligence
```

---

## Sanctions Screening

### Screening Process

1. **Business Name Check** - Screen merchant name against sanctions lists
2. **Beneficial Owner Check** - Screen each owner against sanctions and PEP lists
3. **Fuzzy Matching** - Catch variations and misspellings

### Matching Algorithm

```python
# Exact match - immediate MATCH
if sanctioned_name in entity_name:
    return "MATCH"

# Fuzzy match using sequence similarity
similarity = SequenceMatcher(entity_name, sanctioned_name).ratio()

if similarity >= 0.8:   # 80%+ match
    return "MATCH"
elif similarity >= 0.6: # 60-79% match
    return "POTENTIAL_MATCH"
else:
    return "CLEAR"
```

### Screening Status Actions

| Status | Action | Reason |
|--------|--------|--------|
| **CLEAR** | Continue processing | No matches found |
| **POTENTIAL_MATCH** | Queue for manual review | Possible match, needs human verification |
| **MATCH** | Auto-reject | Definite match on sanctions list |

### Mock Sanctions Lists (Demo)

The system includes mock sanctions data for testing:

**OFAC SDN List:**
- Shell Corp Ltd
- Fraudulent Services Inc

**UN Sanctions:**
- Suspicious Trading Co
- Terrorist Funding Corp

**PEP List:**
- John Politician (Former Minister, Philippines)
- Maria Governor (Regional Governor, Indonesia)
- Robert Senator (Senator, Singapore)

---

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git (optional)

### Setup Steps

```bash
# 1. Navigate to project directory
cd /Users/ahmed/Desktop/AIChallange/yuno_kyb

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run database migrations
python manage.py migrate

# 6. Create admin superuser
python manage.py createsuperuser
# Username: admin
# Email: admin@yuno.com
# Password: admin123

# 7. Start development server
python manage.py runserver
```

### Quick Start (If Already Set Up)

```bash
cd /Users/ahmed/Desktop/AIChallange/yuno_kyb
source venv/bin/activate
python manage.py runserver
```

---

## Usage

### Web URLs

| URL | Purpose |
|-----|---------|
| http://127.0.0.1:8000/ | Home page |
| http://127.0.0.1:8000/register/ | Merchant registration form |
| http://127.0.0.1:8000/status/ | Check application status |
| http://127.0.0.1:8000/dashboard/ | Compliance dashboard |
| http://127.0.0.1:8000/admin/ | Admin panel (login required) |

### Merchant Registration Flow

1. **Visit** `/register/`
2. **Fill Business Information:**
   - Business name
   - Registration number (unique identifier)
   - Country of operation
   - Business category
   - Contact details
3. **Add Beneficial Owners** (optional for low-risk, required for high-risk)
4. **Submit** - System automatically:
   - Calculates risk score
   - Runs sanctions screening
   - Makes approval decision

### Checking Application Status

1. **Visit** `/status/`
2. **Enter** registration number
3. **View** current status, risk assessment, screening results

### Compliance Officer Workflow

1. **Login** to `/admin/` with superuser credentials
2. **View** pending merchants at `Merchants` section
3. **Review** individual merchant details:
   - Risk factors
   - Screening results
   - Beneficial owners
   - Documents
4. **Approve/Reject** using action buttons
5. **Add notes** for audit trail

---

## Testing

### Run All Tests

```bash
source venv/bin/activate
python manage.py test
```

### Run Tests with Verbose Output

```bash
python manage.py test --verbosity=2
```

### Run Specific Test Categories

```bash
# Risk engine tests
python manage.py test merchants.tests.RiskEngineTestCase

# Screening tests
python manage.py test screening.tests

# Integration tests
python manage.py test merchants.tests.IntegrationTestCase

# Admin workflow tests
python manage.py test merchants.tests.ComplianceOfficerWorkflowTestCase
```

### Test Coverage Summary

| Category | Tests | Coverage |
|----------|-------|----------|
| Risk Engine | 7 | Score calculation, thresholds, factors |
| Sanctions Screening | 6 | Exact match, fuzzy match, PEP detection |
| Auto-Approval Logic | 3 | Approval rules validation |
| Registration Views | 7 | Form submission, validation |
| Compliance Workflow | 4 | Admin approve/reject actions |
| Integration Tests | 3 | End-to-end scenarios |
| Screening Service | 11 | Entity/merchant screening |
| Model Tests | 7 | Data model behavior |
| **Total** | **48** | **All passing** |

### Manual Test Scenarios

**Test 1: Auto-Approve (Low Risk)**
```
Business: TechShop Singapore
Country: Singapore
Category: E-commerce
Expected: APPROVED (auto)
```

**Test 2: Manual Review (High Risk)**
```
Business: CryptoExchange
Country: Indonesia
Category: Crypto-adjacent
Expected: PENDING (manual review required)
```

**Test 3: Auto-Reject (Sanctions Match)**
```
Business: Shell Corp Ltd
Country: Any
Category: Any
Expected: REJECTED (sanctions match)
```

---

## API Reference

### Models

#### Merchant
```python
{
    "business_name": "string",
    "registration_number": "string (unique)",
    "country": "SG|PH|ID|MY|TH|VN",
    "business_category": "ECOMMERCE|DIGITAL_SERVICES|GAMING|REMITTANCES|CRYPTO|LUXURY",
    "email": "email",
    "phone": "string",
    "address": "text",
    "risk_level": "LOW|MEDIUM|HIGH",
    "status": "PENDING|APPROVED|REJECTED|UNDER_REVIEW",
    "review_notes": "text",
    "reviewed_by": "User (FK)",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

#### BeneficialOwner
```python
{
    "merchant": "Merchant (FK)",
    "full_name": "string",
    "nationality": "string (ISO country code)",
    "ownership_percentage": "decimal",
    "id_document_type": "PASSPORT|NATIONAL_ID",
    "id_document_number": "string",
    "is_pep": "boolean"
}
```

#### RiskAssessment
```python
{
    "merchant": "Merchant (FK)",
    "risk_score": "integer (0-100)",
    "risk_factors": "JSON array",
    "assessment_date": "datetime",
    "assessed_by": "SYSTEM|MANUAL"
}
```

#### ScreeningResult
```python
{
    "merchant": "Merchant (FK)",
    "screening_type": "SANCTIONS|PEP|ADVERSE_MEDIA",
    "status": "CLEAR|MATCH|POTENTIAL_MATCH",
    "matched_list": "string",
    "match_details": "JSON",
    "screened_entity": "string",
    "screened_at": "datetime"
}
```

---

## Admin Panel

### Login

- **URL:** http://127.0.0.1:8000/admin/
- **Username:** admin
- **Password:** admin123

### Features

| Feature | Description |
|---------|-------------|
| **Merchant List** | View all merchants with filters |
| **Risk Filtering** | Filter by LOW/MEDIUM/HIGH risk |
| **Status Filtering** | Filter by PENDING/APPROVED/REJECTED |
| **Bulk Actions** | Approve/reject multiple merchants |
| **Inline Editing** | View/edit beneficial owners, documents |
| **Audit Trail** | See who reviewed and when |

### Color Coding

- 🟢 **Green** - Approved / Low Risk / Clear
- 🟡 **Orange** - Pending / Medium Risk / Potential Match
- 🔴 **Red** - Rejected / High Risk / Match
- 🔵 **Blue** - Under Review

---

## Project Structure

```
yuno_kyb/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation
├── db.sqlite3               # SQLite database (dev)
├── audit.log                # Audit trail logs
│
├── yuno_kyb/                # Project configuration
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI application
│
├── merchants/               # Merchant app
│   ├── __init__.py
│   ├── models.py            # Merchant, BeneficialOwner, Document, RiskAssessment
│   ├── views.py             # Registration, status, dashboard views
│   ├── forms.py             # Registration forms
│   ├── admin.py             # Admin configuration
│   ├── urls.py              # App URL patterns
│   ├── risk_engine.py       # Risk scoring logic
│   ├── tests.py             # Unit tests
│   └── templates/merchants/ # HTML templates
│       ├── home.html
│       ├── register.html
│       ├── check_status.html
│       ├── status.html
│       └── dashboard.html
│
├── screening/               # Screening app
│   ├── __init__.py
│   ├── models.py            # ScreeningResult, SanctionsList
│   ├── services.py          # Screening logic
│   ├── admin.py             # Admin configuration
│   └── tests.py             # Unit tests
│
├── templates/               # Global templates
│   └── base.html            # Base template with Bootstrap
│
└── media/                   # Uploaded files
    └── documents/           # Merchant documents
```

---

## Security Considerations

### Current Implementation

- CSRF protection on all forms
- Session-based authentication for admin
- Input validation on all fields
- SQL injection prevention via Django ORM

### Production Recommendations

1. **Change SECRET_KEY** - Generate a new secret key
2. **Set DEBUG=False** - Disable debug mode
3. **Use PostgreSQL** - Replace SQLite
4. **HTTPS Only** - Enable SSL/TLS
5. **Rate Limiting** - Add request throttling
6. **Document Encryption** - Encrypt uploaded files at rest
7. **API Authentication** - Add API key or OAuth for integrations
8. **Regular Backups** - Automate database backups
9. **Log Monitoring** - Set up alerts for suspicious activity

---

## Future Enhancements

### Phase 2 Features

- [ ] Real-time sanctions list integration (World-Check, Dow Jones)
- [ ] Document OCR and verification
- [ ] Email notifications for status updates
- [ ] REST API for external integrations
- [ ] Periodic re-screening scheduler
- [ ] Transaction monitoring integration
- [ ] Multi-language support (Bahasa, Thai, Vietnamese)

### Phase 3 Features

- [ ] Machine learning risk scoring
- [ ] Adverse media screening
- [ ] Corporate registry API integration
- [ ] Mobile-responsive redesign
- [ ] SSO integration (SAML/OIDC)

---

## License

This project is developed for Yuno's compliance requirements. Internal use only.

---

## Support

For questions or issues:
- **Technical:** engineering@yuno.com
- **Compliance:** compliance@yuno.com

---

*Built with Django 5.x | Python 3.11+ | Bootstrap 5*
