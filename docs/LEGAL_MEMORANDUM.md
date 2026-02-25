# LEGAL MEMORANDUM

## PRIVILEGED AND CONFIDENTIAL
### ATTORNEY-CLIENT PRIVILEGED

---

**TO:** Chief Executive Officer and Executive Team, Yuno

**FROM:** Legal & Compliance Advisory

**DATE:** February 25, 2026

**RE:** KYB Compliance Assessment and Risk Mitigation Strategy Following Indonesian Payment Facilitator Incident

---

## EXECUTIVE SUMMARY

### Situation Overview

Following the recent Indonesian payment facilitator scandal involving illegal online gambling operations processed through legitimate payment infrastructure, Yuno faces heightened regulatory scrutiny across its Southeast Asian operations. This memorandum assesses Yuno's regulatory exposure as a payment orchestration platform and provides actionable risk mitigation recommendations.

### Key Findings

| Risk Area | Severity | Immediate Action Required |
|-----------|----------|---------------------------|
| Indonesia Regulatory Exposure | **CRITICAL** | Yes - 30 days |
| Philippines PSP Relationship | **HIGH** | Yes - 30 days |
| Singapore MAS Compliance | **MEDIUM** | Yes - 60 days |
| KYB Process Gaps | **HIGH** | Yes - 30 days |

### Priority Actions (Next 30-90 Days)

**Immediate (0-30 Days):**
1. Implement enhanced merchant screening for all new onboarding
2. Conduct retrospective review of existing Indonesia-connected merchants
3. Engage proactively with Philippine PSP partner to demonstrate compliance improvements

**Short-term (30-60 Days):**
4. Deploy automated sanctions screening system
5. Establish beneficial ownership verification protocols
6. Create risk-based merchant categorization framework

**Medium-term (60-90 Days):**
7. Complete MAS Payment Services Act compliance audit
8. Implement ongoing transaction monitoring capabilities
9. Establish quarterly compliance reporting to Board

### Key Takeaways for Board Presentation

1. **Yuno is NOT directly liable** for merchant misconduct, but faces significant **regulatory and reputational risk** as a payment chain participant
2. **Proactive compliance investment** is substantially less costly than reactive enforcement response
3. **KYB enhancement** is both a regulatory necessity and competitive differentiator
4. **Estimated compliance investment:** USD 150,000-250,000 (one-time) + USD 50,000/year (ongoing)
5. **Estimated risk exposure without action:** USD 1-5 million in potential fines, plus license revocation risk

---

## SECTION 1: REGULATORY RISK ASSESSMENT

### 1.1 Yuno's Position in the Payment Chain

Yuno operates as a **payment orchestration platform**, providing:
- Single API integration for merchants to access multiple payment providers
- Transaction routing and optimization
- Consolidated reporting and reconciliation

**Critical Legal Question:** Does Yuno's role as an orchestrator/aggregator create KYB obligations equivalent to those of licensed Payment Service Providers (PSPs)?

**Analysis:** While Yuno may not hold direct PSP licenses in all jurisdictions, the regulatory trend clearly indicates:

1. **Regulatory authorities increasingly view the entire payment chain** as responsible for merchant due diligence
2. **Contractual obligations** from PSP partners typically flow KYB requirements upstream
3. **Reputational contagion** affects all participants when merchant misconduct is discovered

### 1.2 Indonesia Analysis

#### Regulatory Framework

| Regulation | Authority | Relevance to Yuno |
|------------|-----------|-------------------|
| Bank Indonesia Regulation No. 22/23/PBI/2020 | Bank Indonesia | Payment system licensing and AML requirements |
| OJK Regulation No. 12/POJK.01/2017 | OJK | AML/CFT for financial services |
| Presidential Regulation No. 13/2018 | Government | Beneficial ownership transparency |

#### Current Risk Assessment: CRITICAL

**Specific Concerns:**

1. **Direct Regulatory Attention:** Indonesia is ground zero for the payment facilitator scandal. Bank Indonesia and OJK are actively investigating payment chain participants.

2. **Merchant Nexus:** If any of the merchants involved in the scandal processed payments through Yuno-connected PSPs, Yuno will face scrutiny regarding:
   - What due diligence was performed at onboarding?
   - Were there transaction patterns indicating gambling activity?
   - What ongoing monitoring was in place?

3. **License Implications:** While Yuno may operate through licensed PSP partners, regulatory action against those partners (license suspension/revocation) would directly impact Yuno's operations.

#### Key Regulatory Requirements

**Bank Indonesia PBI 22/23/PBI/2020 requires:**
- Customer identification and verification
- Beneficial ownership identification for legal entities
- Ongoing due diligence and transaction monitoring
- Suspicious transaction reporting

**Application to Payment Orchestrators:**
- BI has signaled intent to extend oversight to "technology service providers" in the payment ecosystem
- Draft regulations under consideration would require registration of payment facilitators and aggregators
- **Recommendation:** Prepare for direct regulatory obligations within 12-18 months

#### Recommended Actions for Indonesia

| Priority | Action | Timeline | Responsible |
|----------|--------|----------|-------------|
| 1 | Conduct retrospective review of all Indonesia-connected merchants | 14 days | Compliance |
| 2 | Implement enhanced screening for Indonesia market | 21 days | Product/Engineering |
| 3 | Engage external counsel for BI/OJK regulatory consultation | 30 days | Legal |
| 4 | Prepare incident response plan for potential regulatory inquiry | 30 days | Legal/Compliance |

---

### 1.3 Philippines Analysis

#### Regulatory Framework

| Regulation | Authority | Relevance to Yuno |
|------------|-----------|-------------------|
| Republic Act No. 9160 (AMLA) as amended | AMLC | AML obligations for covered persons |
| BSP Circular No. 706 | BSP | E-money and payment system regulations |
| BSP Circular No. 1022 | BSP | Enhanced due diligence requirements |

#### Current Risk Assessment: HIGH

**Specific Concerns:**

1. **PSP Partner Relationship at Risk:** A key Philippine PSP partner is already reviewing its relationship with Yuno. Loss of this partnership would significantly impact Philippine market operations.

2. **BSP Heightened Scrutiny:** Following regional incidents, BSP has increased examination of payment service providers and their technology partners.

3. **Covered Person Status:** Under AMLA, entities facilitating fund transfers may be classified as "covered persons" with direct AML obligations.

#### Key Regulatory Requirements

**BSP Circular 706 requires payment system operators to:**
- Implement risk-based customer acceptance policies
- Conduct customer due diligence (CDD) and enhanced due diligence (EDD) where appropriate
- Maintain records for at least 5 years
- Report covered and suspicious transactions

**AMLA Requirements:**
- Customer identification program
- Record-keeping requirements
- Suspicious transaction reporting
- Compliance officer designation

#### Recommended Actions for Philippines

| Priority | Action | Timeline | Responsible |
|----------|--------|----------|-------------|
| 1 | Schedule call with PSP partner compliance team | 7 days | Business Development |
| 2 | Prepare compliance enhancement presentation for PSP | 14 days | Compliance |
| 3 | Review all Philippine merchant accounts for risk indicators | 21 days | Compliance |
| 4 | Engage Philippine legal counsel for BSP consultation | 30 days | Legal |

---

### 1.4 Singapore Analysis

#### Regulatory Framework

| Regulation | Authority | Relevance to Yuno |
|------------|-----------|-------------------|
| Payment Services Act 2019 | MAS | Licensing and conduct requirements |
| MAS Notice PSN01 | MAS | AML/CFT requirements for payment services |
| MAS Notice PSN02 | MAS | Technology risk management |

#### Current Risk Assessment: MEDIUM

**Specific Concerns:**

1. **Licensing Requirements:** The Payment Services Act 2019 has clear licensing categories. Yuno's activities may require a license as a "payment service provider" under one or more categories.

2. **AML/CFT Notice PSN01:** If licensed or operating in Singapore, Yuno would be subject to comprehensive AML/CFT requirements including:
   - Customer due diligence
   - Enhanced measures for high-risk situations
   - Correspondent banking due diligence (applicable to payment service relationships)

3. **Regulatory Precedent:** Singapore's strict enforcement creates precedent that other ASEAN regulators follow.

#### Key Regulatory Requirements

**Payment Services Act 2019 - Relevant License Types:**
- **Major Payment Institution (MPI):** Required if transaction volume exceeds thresholds
- **Standard Payment Institution (SPI):** For lower-volume operations

**MAS Notice PSN01 Requirements:**
- Risk assessment and risk-based approach
- Customer due diligence (CDD)
- Enhanced due diligence for higher-risk customers
- Ongoing monitoring
- Suspicious transaction reporting
- Record keeping (5 years minimum)

#### Recommended Actions for Singapore

| Priority | Action | Timeline | Responsible |
|----------|--------|----------|-------------|
| 1 | Conduct licensing assessment with Singapore counsel | 30 days | Legal |
| 2 | Map current practices against PSN01 requirements | 45 days | Compliance |
| 3 | Implement compliant merchant onboarding process | 60 days | Product/Engineering |
| 4 | Establish MAS notification/reporting protocols | 60 days | Compliance |

---

## SECTION 2: RISK MITIGATION STRATEGY

### 2.1 Enhanced Merchant Screening Framework

#### Tier-Based Due Diligence Model

| Merchant Risk Tier | Criteria | Due Diligence Level | Approval Process |
|--------------------|----------|---------------------|------------------|
| **Tier 1 - Low Risk** | Standard e-commerce, Singapore-based, <$100K monthly volume | Simplified DD | Automated approval |
| **Tier 2 - Medium Risk** | Gaming, remittance, higher-risk jurisdictions | Standard DD | Compliance review |
| **Tier 3 - High Risk** | Crypto-adjacent, complex ownership, PEP involvement | Enhanced DD | Senior compliance + Legal approval |
| **Tier 4 - Prohibited** | Sanctions match, unlicensed financial services, illegal activity | Rejection | Auto-reject |

#### Minimum Due Diligence Requirements

**All Merchants (Simplified DD):**
- [ ] Business registration verification
- [ ] Business address confirmation
- [ ] Contact information validation
- [ ] Sanctions screening (business name)
- [ ] Basic website/business model review

**Medium Risk (Standard DD):**
- [ ] All Simplified DD requirements
- [ ] Beneficial ownership identification (>25% ownership)
- [ ] Sanctions screening (all beneficial owners)
- [ ] Business license/permit verification
- [ ] Financial statements or bank reference
- [ ] PEP screening for beneficial owners

**High Risk (Enhanced DD):**
- [ ] All Standard DD requirements
- [ ] Source of funds documentation
- [ ] Detailed business model review
- [ ] On-site visit or video verification
- [ ] Third-party due diligence report
- [ ] Senior management approval
- [ ] Ongoing enhanced monitoring

### 2.2 Sanctions Screening Implementation

#### Screening Requirements

| Screen Type | Timing | Lists | Action on Match |
|-------------|--------|-------|-----------------|
| **Initial Screening** | Onboarding | OFAC, UN, EU, Local | Block if match; Review if potential |
| **Ongoing Screening** | Daily batch | OFAC, UN, EU, Local | Alert for review; Suspend if confirmed |
| **Transaction Screening** | Real-time | OFAC, UN | Block transaction; Flag account |

#### Recommended Sanctions Lists

1. **OFAC SDN List** (US Office of Foreign Assets Control)
2. **UN Security Council Consolidated List**
3. **EU Consolidated Sanctions List**
4. **MAS Lists of Designated Individuals and Entities** (Singapore)
5. **AMLC Targeted Financial Sanctions List** (Philippines)
6. **PPATK Lists** (Indonesia)

### 2.3 Beneficial Ownership Requirements

#### Identification Thresholds

| Jurisdiction | Threshold | Documentation Required |
|--------------|-----------|------------------------|
| Singapore | 25% ownership or control | ACRA Bizfile, ID documents |
| Philippines | 20% ownership | SEC registration, ID documents |
| Indonesia | 25% ownership | Company deed, ID documents |
| **Yuno Standard** | **20% ownership** | **Passport/National ID, Proof of address** |

#### Complex Ownership Structures

For merchants with:
- Multiple layers of corporate ownership
- Nominee shareholders
- Trust structures
- Cross-border ownership

**Require:**
1. Full ownership chart to ultimate beneficial owners
2. Explanation of structure purpose
3. Enhanced ongoing monitoring
4. Annual ownership confirmation

### 2.4 PEP (Politically Exposed Person) Screening

#### PEP Definition

A Politically Exposed Person includes:
- Heads of state, government ministers, senior politicians
- Senior judicial officials
- Senior military officials
- Senior executives of state-owned enterprises
- **Family members** of the above
- **Close associates** of the above

#### PEP Handling Procedures

| PEP Status | Action Required |
|------------|-----------------|
| **PEP Identified** | Enhanced due diligence required |
| **PEP - Low Risk** | Senior compliance approval; Annual review |
| **PEP - High Risk** | Legal + Compliance + CEO approval; Quarterly review |
| **PEP - Sanctioned Jurisdiction** | Rejection unless exceptional circumstances |

### 2.5 Ongoing Monitoring Framework

#### Transaction Monitoring

| Indicator | Threshold | Action |
|-----------|-----------|--------|
| Volume spike | >200% of normal | Alert for review |
| High-risk country transactions | Any | Enhanced review |
| Round number transactions | Pattern detected | Alert for review |
| Rapid fund movement | In/out within 24hrs | Alert for review |
| Weekend/night activity | Unusual pattern | Alert for review |

#### Periodic Reviews

| Merchant Risk Level | Review Frequency | Review Scope |
|---------------------|------------------|--------------|
| Low Risk | Annual | Ownership confirmation, Sanctions re-screen |
| Medium Risk | Semi-annual | Full CDD refresh |
| High Risk | Quarterly | Full EDD refresh, Transaction review |

---

## SECTION 3: IMPLEMENTATION ROADMAP

### Phase 1: Immediate Actions (Days 1-30)

| Week | Deliverable | Owner |
|------|-------------|-------|
| 1 | Form compliance task force | CEO |
| 1 | Engage external counsel (Indonesia, Philippines) | Legal |
| 2 | Complete retrospective merchant review (Indonesia exposure) | Compliance |
| 2 | Implement basic sanctions screening | Engineering |
| 3 | Deploy enhanced onboarding questionnaire | Product |
| 3 | Schedule PSP partner compliance call | Business Dev |
| 4 | Complete risk assessment of existing portfolio | Compliance |
| 4 | Establish compliance reporting to Board | Compliance |

### Phase 2: Foundation Building (Days 31-60)

| Week | Deliverable | Owner |
|------|-------------|-------|
| 5-6 | Deploy automated KYB system | Engineering |
| 5-6 | Implement beneficial ownership collection | Product |
| 7 | Complete Singapore licensing assessment | Legal |
| 7 | Train operations team on new procedures | Compliance |
| 8 | Implement risk-based merchant tiering | Compliance |
| 8 | Establish ongoing monitoring protocols | Compliance |

### Phase 3: Enhancement (Days 61-90)

| Week | Deliverable | Owner |
|------|-------------|-------|
| 9-10 | Integrate PEP screening database | Engineering |
| 9-10 | Deploy transaction monitoring rules | Engineering |
| 11 | Complete PSN01 gap analysis (Singapore) | Compliance |
| 11 | Establish regulatory relationship protocols | Legal |
| 12 | Conduct compliance program audit | External |
| 12 | Board presentation on compliance program | CEO/Compliance |

---

## SECTION 4: RESOURCE REQUIREMENTS

### Budget Estimate

| Category | One-time Cost (USD) | Annual Cost (USD) |
|----------|---------------------|-------------------|
| **Technology** | | |
| KYB/Screening System | 50,000 - 80,000 | 20,000 - 30,000 |
| Transaction Monitoring | 30,000 - 50,000 | 15,000 - 25,000 |
| **Personnel** | | |
| Compliance Officer (hire) | 15,000 (recruiting) | 80,000 - 120,000 |
| Training | 10,000 | 5,000 |
| **External Services** | | |
| Legal Counsel | 40,000 - 60,000 | 20,000 - 30,000 |
| Sanctions Data Provider | - | 15,000 - 25,000 |
| External Audit | 15,000 - 20,000 | 15,000 - 20,000 |
| **Total** | **160,000 - 235,000** | **170,000 - 255,000** |

### Staffing Requirements

| Role | Current | Required | Gap |
|------|---------|----------|-----|
| Chief Compliance Officer | 0 | 1 | **Hire** |
| Compliance Analyst | 0 | 2 | **Hire** |
| Legal Counsel (in-house) | 1 | 1 | Adequate |
| Engineering (compliance features) | 0 | 1 | **Allocate** |

---

## SECTION 5: LEGAL RISK SUMMARY

### Potential Regulatory Penalties

| Jurisdiction | Violation Type | Potential Penalty |
|--------------|----------------|-------------------|
| **Singapore** | PSA violation | Up to SGD 1,000,000 per offense |
| **Singapore** | AML violation | Up to SGD 500,000 per offense |
| **Philippines** | AMLA violation | PHP 500,000 - 5,000,000 + imprisonment |
| **Indonesia** | AML violation | IDR 1 - 100 billion |

### Reputational Risk Factors

1. **Media Coverage:** Payment processor involvement in gambling scandal is highly newsworthy
2. **PSP Partner Confidence:** Partners may terminate relationships preemptively
3. **Merchant Confidence:** Legitimate merchants may seek alternative providers
4. **Investor Confidence:** Compliance failures impact valuation and funding

### Litigation Risk

| Scenario | Likelihood | Potential Exposure |
|----------|------------|-------------------|
| Regulatory enforcement action | Medium | $500K - $5M |
| PSP contract termination claims | Low-Medium | $100K - $500K |
| Class action (if public company) | Low | $1M+ |
| Criminal referral (executives) | Very Low | Personal liability |

---

## SECTION 6: RECOMMENDATIONS

### Immediate Priorities

1. **APPOINT** a Chief Compliance Officer with regional AML expertise within 30 days

2. **IMPLEMENT** enhanced merchant screening immediately for all new onboarding

3. **CONDUCT** retrospective review of existing merchant portfolio for Indonesia exposure

4. **ENGAGE** proactively with Philippine PSP partner to demonstrate compliance commitment

5. **RETAIN** external counsel in Indonesia and Philippines for regulatory guidance

### Strategic Recommendations

6. **INVEST** in automated KYB/AML infrastructure as competitive differentiator

7. **ESTABLISH** Board-level compliance oversight with quarterly reporting

8. **DEVELOP** regulatory relationships proactively before enforcement actions

9. **CONSIDER** voluntary regulatory engagement to demonstrate good faith

10. **DOCUMENT** all compliance enhancements for potential regulatory defense

---

## CONCLUSION

The Indonesian payment facilitator scandal has created a critical inflection point for Yuno. While Yuno's role as a payment orchestrator may provide some regulatory distance from direct merchant misconduct, this protection is narrowing rapidly as regulators expand oversight across the payment chain.

**The cost of proactive compliance investment (approximately USD 200,000 one-time + USD 200,000 annually) is substantially less than the potential cost of regulatory enforcement, reputational damage, or loss of PSP partnerships.**

Moreover, robust KYB/AML capabilities represent a competitive advantage. As regulatory requirements tighten, merchants will increasingly select payment providers who can demonstrate compliance excellence.

**We strongly recommend immediate implementation of the actions outlined in this memorandum.**

---

## APPENDICES

### Appendix A: Regulatory Contact Information

| Jurisdiction | Authority | Contact |
|--------------|-----------|---------|
| Singapore | MAS FinTech Office | fintech@mas.gov.sg |
| Philippines | BSP Financial Consumer Protection | consumeraffairs@bsp.gov.ph |
| Indonesia | Bank Indonesia | bicara@bi.go.id |

### Appendix B: Recommended External Counsel

| Jurisdiction | Recommended Firms | Specialization |
|--------------|-------------------|----------------|
| Singapore | Allen & Gledhill, WongPartnership | Payments, MAS regulatory |
| Philippines | SyCip Salazar Hernandez & Gatmaitan | BSP regulatory, AML |
| Indonesia | ABNR, Hadiputranto Hadinoto & Partners | BI/OJK regulatory |

### Appendix C: Reference Documents

1. Payment Services Act 2019 (Singapore)
2. MAS Notice PSN01 on Prevention of Money Laundering and Countering the Financing of Terrorism
3. BSP Circular No. 706 - Rules and Regulations on Electronic Money
4. Bank Indonesia Regulation No. 22/23/PBI/2020
5. Republic Act No. 9160 (AMLA) as amended

---

*This memorandum is intended for internal use only and constitutes privileged attorney-client communication. Distribution outside of Yuno executive leadership requires prior approval.*

**Prepared by:** Legal & Compliance Advisory Team

**Review Date:** 90 days from issuance
