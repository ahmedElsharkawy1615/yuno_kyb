# LEGAL MEMORANDUM

**PRIVILEGED AND CONFIDENTIAL**
**ATTORNEY-CLIENT COMMUNICATION**

---

**TO:** Maria Santos, Chief Executive Officer
       Executive Leadership Team
       Board of Directors

**FROM:** Office of General Counsel

**DATE:** February 25, 2026

**RE:** KYB Compliance Assessment and Risk Mitigation Strategy Following Indonesian Payment Facilitator Enforcement Action

---

## EXECUTIVE SUMMARY

### Situation Overview

Following the Indonesian regulatory enforcement action against a payment facilitator for inadequate merchant screening, Yuno faces immediate pressure from three stakeholder groups: (1) institutional investors requesting compliance briefings, (2) enterprise clients invoking audit clauses, and (3) a Philippine PSP partner reviewing its relationship with Yuno. This memorandum provides a realistic assessment of Yuno's regulatory exposure and actionable recommendations for the next 30-90 days.

### Key Findings

| Risk Category | Assessment | Priority |
|---------------|------------|----------|
| **Indonesia** | HIGH - Direct regulatory attention; evolving "payment chain" doctrine | Immediate |
| **Philippines** | HIGH - Active PSP relationship at risk; BSP regulatory scrutiny | Immediate |
| **Singapore** | MEDIUM-HIGH - Clear PSA 2019 framework; MAS enforcement precedent | Short-term |

### Critical Takeaways for Board Presentation

1. **Contractual protections are insufficient.** While Yuno's PSP contracts state that partners bear "sole responsibility" for compliance, this contractual allocation does not bind regulators and may not withstand scrutiny under expanding "payment chain responsibility" doctrines.

2. **Current practices create genuine regulatory exposure.** Yuno's lack of sanctions screening, beneficial ownership verification, and business model risk assessment represents a compliance gap that regulators in our priority markets could characterize as inadequate, particularly given the 8% of merchants in high-risk categories.

3. **The reputational and commercial risk is immediate; legal risk is crystallizing.** The Philippine PSP partner's review and investor inquiries represent tangible near-term threats. However, the Indonesian enforcement action signals that regulators across APAC are adopting broader interpretations of compliance obligations throughout the payment chain.

### Priority Actions (Next 30 Days)

1. Proactively engage Philippine PSP partner with enhanced compliance roadmap
2. Prepare standardized investor briefing materials on compliance posture
3. Implement immediate sanctions screening for all merchant onboarding
4. Commission independent gap analysis of current onboarding vs. regulatory best practices
5. Establish enhanced due diligence protocols for the 8% high-risk merchant segment

---

## PART I: REGULATORY RISK ASSESSMENT

### Jurisdiction Selection Rationale

We have prioritized three markets based on the following criteria:

- **Indonesia**: Ground zero of the current enforcement action; heightened regulatory attention across the payment ecosystem
- **Philippines**: Active commercial threat from PSP partner review; BSP has clear regulatory authority over payment service providers
- **Singapore**: Most developed regulatory framework in APAC under the Payment Services Act 2019; MAS interpretations often influence regional regulatory approaches

Brazil, Mexico, and Colombia (significant markets by volume) present lower immediate regulatory risk given the current APAC-focused scrutiny and different regulatory maturity levels. However, we recommend monitoring these jurisdictions for spillover effects.

---

### A. Indonesia

#### Regulatory Framework

Indonesia's payment system is primarily regulated by Bank Indonesia (BI) under the Indonesia Payment System Blueprint 2025, with updated regulations under BI Regulation No. 4 of 2025 on Payment System Policy and BI Regulation No. 10 of 2025 concerning Regulation of the Payment System Industry (PBI 10/2025), effective March 31, 2026.

Key regulatory characteristics:
- BI mandates KYC and AML/CFT implementation across the payment ecosystem
- The 2025-2030 Blueprint emphasizes "balance between innovation and consumer protection, integrity and stability"
- All regulated parties—banks, non-banks, infrastructure providers, and affiliates—must comply with BI provisions
- OJK (Financial Services Authority) provides additional oversight for certain fintech activities under OJK Regulation No. 3 of 2024

#### Applicability to Payment Orchestrators

**Current Legal Ambiguity:** Indonesian regulations were drafted primarily with traditional payment facilitators and acquirers in mind. Payment orchestrators like Yuno occupy a regulatory gray zone. However, the recent enforcement action included language emphasizing that **"all entities in the payment chain share responsibility for preventing illicit use."**

**Risk Assessment:** This "payment chain responsibility" statement, while made in the context of a licensed payment facilitator, signals BI's willingness to look beyond direct licensees when assessing compliance failures. Yuno's position as the technical routing layer—making decisions about which PSP processes each transaction—could be characterized by regulators as active participation in the payment chain rather than passive technology provision.

**Specific Vulnerabilities:**
- Yuno routes transactions through Indonesian PSPs without independent KYB verification
- No sanctions screening at the Yuno platform level
- Multi-PSP routing means a single merchant's transactions may flow through multiple partners, creating monitoring gaps
- The 8% high-risk merchant segment (money transfer, crypto-adjacent) presents elevated exposure

#### Risk Level: **HIGH**

The combination of direct regulatory attention from the scandal, ambiguous but expanding regulatory interpretation, and Yuno's lack of independent compliance controls creates material legal exposure. While Yuno may not be the primary enforcement target, regulatory inquiries, requests for information, or being named in enforcement proceedings against PSP partners are realistic near-term risks.

---

### B. Philippines

#### Regulatory Framework

The Bangko Sentral ng Pilipinas (BSP) regulates payment service providers through a comprehensive circular framework:

- **BSP Circular No. 1206 (Series of 2024)**: Consolidated rules for Money Service Businesses under the Manual of Regulations for Non-bank Financial Institutions (MORNBFI)
- **BSP Circular No. 1170**: Permits electronic KYC verification and establishes technology-enabled onboarding standards
- New guidelines for merchant payment applications issued in January 2025 require operators to obtain Merchant Acquirer Licenses (MAL) with specific capital requirements and compliance obligations

Key regulatory characteristics:
- BSP mandates governance standards and risk management measures addressing operational risks, AML, and customer protection
- Three-phase licensing process with eligibility, evaluation, and issuance stages
- Explicit AML/CFT compliance requirements for all BSP-supervised financial institutions
- Compliance officer seminars on AML/CFT are mandatory

#### Applicability to Payment Orchestrators

**Regulatory Clarity:** Unlike Indonesia, the Philippines has more explicit licensing categories for payment service providers. However, payment orchestrators remain an emerging category that BSP regulations do not directly address.

**The PSP Partner Dynamic:** The terse message from Yuno's Philippine PSP partner stating they are "reviewing all payment orchestration relationships for KYB adequacy" is significant. Under BSP regulations, licensed entities bear direct compliance responsibility and face enforcement consequences for failures in their merchant portfolio. PSP partners may:
1. Require Yuno to demonstrate enhanced KYB capabilities
2. Demand access to Yuno's merchant data for their own compliance verification
3. Restrict or terminate relationships with orchestrators lacking robust compliance programs
4. Report concerns to BSP as part of their own compliance obligations

**Risk Assessment:** The immediate risk in the Philippines is commercial (loss of PSP partnership) rather than direct regulatory enforcement against Yuno. However, if Yuno merchants facilitated through Philippine PSPs are implicated in illicit activity, BSP investigations would likely examine the entire transaction chain, including Yuno's role.

#### Risk Level: **HIGH**

The active PSP partner review creates immediate commercial risk. Additionally, BSP's regulatory framework emphasizes that all participants in the payment ecosystem must contribute to AML/CFT objectives. Yuno's current minimal onboarding practices are inconsistent with the compliance posture our PSP partners must maintain.

---

### C. Singapore

#### Regulatory Framework

Singapore's Payment Services Act 2019 (PSA), effective January 28, 2020, represents the most comprehensive payment services regulatory framework in APAC:

- **Licensing Categories:** The PSA covers seven payment service activities, including merchant acquisition services
- **Customer Due Diligence:** Firms must verify customer identities and the nature of their business, with simplified due diligence for lower-risk customers and enhanced due diligence for higher-risk customers
- **Beneficial Ownership:** Explicit requirements for verifying businesses and their beneficial owners, including directors, partners, and persons with executive authority
- **Transaction Monitoring:** Payment services firms must monitor transactions for signs of money laundering and terrorism financing based on thresholds, patterns, and high-risk country connections
- **Sanctions Screening:** Firms must screen customers against UNSC sanctions lists and MAS sanctions lists

#### Applicability to Payment Orchestrators

**Regulatory Clarity:** The PSA explicitly covers "merchant acquisition services" where service providers handle payment processing on merchants' behalf. While Yuno does not directly acquire merchants in the traditional sense, its role in routing transactions and maintaining merchant relationships may fall within MAS's regulatory purview.

**Key Question:** Does Yuno's activity constitute a "payment service" requiring a license, or is Yuno a technology provider outside the PSA's scope?

**Factors Suggesting Regulatory Coverage:**
- Yuno has direct contractual relationships with merchants
- Yuno's platform makes routing decisions affecting transaction processing
- Yuno collects business information during onboarding (even if limited)
- Yuno processes $2.3 billion in annualized transaction volume

**Factors Against Regulatory Coverage:**
- Yuno does not hold funds or settle transactions
- PSP partners maintain acquiring relationships and licensing
- Yuno's contracts characterize its role as technology provision

**Risk Assessment:** MAS has historically taken a substance-over-form approach to regulatory interpretation. The question is whether Yuno's activities, as conducted, constitute a payment service regardless of how they are contractually characterized. Given Singapore's rigorous regulatory environment and MAS's active enforcement posture, operating in Singapore without clarity on licensing status presents meaningful risk.

#### Risk Level: **MEDIUM-HIGH**

Singapore presents clear regulatory requirements but uncertain application to orchestrators. If MAS determines that Yuno requires licensing, operating without a license would constitute a serious regulatory violation. Conversely, if MAS confirms Yuno falls outside PSA scope, Singapore exposure is limited to reputational and commercial concerns. We recommend seeking regulatory clarity proactively.

---

## PART II: LEGAL EXPOSURE ANALYSIS

### A. Key Vulnerabilities

#### 1. Contractual Provisions Are Not a Regulatory Shield

Yuno's PSP contracts state that "Partner is solely responsible for all regulatory compliance, licensing, KYC/KYB, AML, and transaction monitoring obligations in its jurisdiction." While this language may govern the commercial relationship between Yuno and its PSP partners (including indemnification and risk allocation), **contractual provisions do not bind regulators.**

Regulators assess compliance obligations based on statutory and regulatory frameworks, not private contracts. If a regulator determines that Yuno has independent obligations—whether explicit or implied under "payment chain responsibility" doctrines—the PSP contract will not provide a defense.

Furthermore, in enforcement proceedings, regulators may view such contractual language as evidence that Yuno was aware of compliance requirements but deliberately structured its relationships to avoid direct responsibility—a potentially aggravating factor.

#### 2. The "Payment Chain Responsibility" Doctrine

The Indonesian regulator's statement that "all entities in the payment chain share responsibility" reflects a global trend toward expanded compliance expectations:

- **FATF Guidance:** Financial Action Task Force recommendations increasingly emphasize that AML/CFT obligations extend throughout payment ecosystems
- **EU Developments:** Under PSD2 and the forthcoming PSD3, the European approach emphasizes shared responsibility among payment chain participants
- **U.S. Precedent:** U.S. regulators have pursued enforcement actions against technology platforms that facilitated payments, even when those platforms were not traditional financial institutions

This doctrine is particularly relevant for Yuno because:
- Yuno sits at the center of the transaction routing decision
- Yuno has visibility across multiple PSP relationships
- Yuno has a direct relationship with merchants that PSPs may lack
- Yuno's technology choices directly affect which compliance framework applies to each transaction

#### 3. High-Risk Merchant Exposure (8% of Merchant Base)

Approximately 8% of Yuno's merchants operate in categories typically considered higher-risk for AML purposes:
- Money transfer services
- Crypto-adjacent services
- High-value luxury goods

These categories receive heightened regulatory scrutiny globally. Without enhanced due diligence for this segment, Yuno faces disproportionate risk from a relatively small portion of its merchant base.

#### 4. Multi-PSP Routing Creates Monitoring Gaps

A significant structural vulnerability: merchants using Yuno may have transactions routed through multiple PSPs based on geography, payment method, and optimization factors. This creates:

- **Fragmented monitoring:** Each PSP sees only a portion of the merchant's transaction activity
- **Pattern recognition failures:** Suspicious patterns that would be visible in consolidated data may be invisible when distributed across PSPs
- **Responsibility gaps:** No single entity has complete visibility into a merchant's transaction behavior

This is precisely the type of systemic gap that regulators increasingly expect platforms to address.

#### 5. Current Onboarding Deficiencies

Yuno's current onboarding practices fall below regulatory expectations and industry best practices:

| Requirement | Current State | Gap |
|-------------|---------------|-----|
| Business registration verification | Basic collection | Limited verification |
| Beneficial ownership identification | Not performed | Complete gap |
| Sanctions screening | Not performed | Complete gap |
| Business model risk assessment | Not performed | Complete gap |
| Ongoing transaction monitoring | Not performed | Complete gap |

---

### B. Legal vs. Reputational Risk Matrix

| Jurisdiction | Legal Risk | Reputational/Commercial Risk | Primary Concern |
|--------------|------------|------------------------------|-----------------|
| Indonesia | HIGH - Expanding regulatory interpretation | HIGH - Regional attention | Legal |
| Philippines | MEDIUM - Indirect through PSP partners | HIGH - Active partnership at risk | Commercial (immediate), Legal (secondary) |
| Singapore | MEDIUM-HIGH - Licensing uncertainty | MEDIUM - MAS reputation matters | Legal (clarity needed) |
| Brazil/Mexico/Colombia | LOW - Different regulatory focus | MEDIUM - Investor confidence | Reputational |

---

## PART III: PRACTICAL RISK MITIGATION STRATEGY

### Phase 1: Immediate Actions (0-30 Days)

#### 1.1 Philippine PSP Partner Engagement
**Owner:** Head of Partnerships
**Priority:** CRITICAL

- Schedule call within 48 hours to understand specific concerns
- Prepare enhanced compliance roadmap to demonstrate commitment
- Offer to share merchant KYB data under appropriate confidentiality protections
- Propose joint compliance review to identify specific gaps
- Document all communications for regulatory response purposes

#### 1.2 Investor Briefing Materials
**Owner:** General Counsel + CFO
**Priority:** HIGH

Prepare standardized materials addressing:
- Yuno's current compliance posture (accurate, not defensive)
- Distinction between legal exposure and reputational concern
- Concrete remediation timeline
- Resource commitment to compliance enhancement
- Governance oversight of compliance program

#### 1.3 Immediate Sanctions Screening Implementation
**Owner:** Head of Compliance
**Priority:** CRITICAL

- Implement sanctions screening for all new merchant onboarding immediately
- Select vendor with global watchlist coverage (OFAC, UN, EU, MAS, local lists)
- Screen existing merchant base within 30 days
- Establish clear procedures for positive matches and escalation
- Estimated implementation: 5-7 business days with third-party provider

#### 1.4 Independent Gap Analysis
**Owner:** General Counsel
**Priority:** HIGH

Commission external review comparing:
- Current onboarding practices vs. regulatory requirements in priority markets
- Current practices vs. industry best practices for payment platforms
- Specific gaps requiring remediation
- Resource and timeline estimates for gap closure

#### 1.5 Enhanced Due Diligence for High-Risk Segment
**Owner:** Head of Compliance
**Priority:** HIGH

For the 8% of merchants in high-risk categories:
- Implement immediate enhanced review procedures
- Require beneficial ownership disclosure
- Conduct business model verification
- Establish periodic re-verification requirements
- Consider risk-based pricing or transaction limits pending full compliance

---

### Phase 2: Short-Term Actions (30-90 Days)

#### 2.1 Tiered KYB Framework Implementation
**Owner:** Head of Compliance + Product
**Priority:** HIGH

Implement risk-based approach:

**Enhanced Due Diligence (High-Risk: ~8%)**
- Full beneficial ownership verification
- Business model documentation and review
- Source of funds verification
- Ongoing enhanced monitoring
- Annual re-verification

**Standard Due Diligence (Medium-Risk: ~40%)**
- Business registration verification
- Beneficial ownership identification (not full verification)
- Sanctions screening
- Basic business model review
- Bi-annual re-verification

**Simplified Due Diligence (Low-Risk: ~52%)**
- Business registration verification
- Sanctions screening
- Annual re-verification
- Transaction-based monitoring triggers

#### 2.2 PSP Contract Renegotiation
**Owner:** General Counsel + Head of Partnerships
**Priority:** HIGH

Key negotiation points:
- KYB data sharing provisions (access to PSP verification results)
- Information sharing protocols for suspicious activity
- Clear delineation of compliance responsibilities
- Cooperation requirements for regulatory inquiries
- Audit rights and procedures
- Termination provisions tied to compliance failures

#### 2.3 Beneficial Ownership Verification Capability
**Owner:** Head of Compliance
**Priority:** MEDIUM-HIGH

- Select and implement beneficial ownership verification provider
- Integrate with merchant onboarding workflow
- Establish verification standards (25% ownership threshold consistent with FATF)
- Create ongoing monitoring for ownership changes
- Document verification procedures for regulatory review

#### 2.4 Regulatory Engagement - Singapore
**Owner:** General Counsel
**Priority:** MEDIUM-HIGH

Proactively engage with MAS to clarify licensing status:
- Prepare detailed description of Yuno's business model
- Seek guidance on PSA applicability
- If licensing required, initiate application process
- If not required, obtain written confirmation for records

---

### Phase 3: Medium-Term Actions (90+ Days)

#### 3.1 Consolidated Transaction Monitoring
**Owner:** Head of Compliance + Engineering
**Priority:** MEDIUM

Build capability to:
- Aggregate transaction data across PSP relationships
- Identify patterns invisible to individual PSPs
- Detect velocity changes, geographic anomalies, and unusual patterns
- Generate alerts for compliance review
- Produce SAR-quality documentation when required

#### 3.2 Transaction Pattern Analytics
**Owner:** Data Science + Compliance
**Priority:** MEDIUM

Develop monitoring for:
- Structuring patterns (transactions designed to avoid reporting thresholds)
- Rapid merchant behavior changes
- Geographic risk indicators
- Payment method anomalies
- Peer comparison analysis

#### 3.3 Regulatory Engagement Strategy
**Owner:** General Counsel + Government Affairs
**Priority:** MEDIUM

Develop proactive engagement approach for key markets:
- Regular meetings with regulators in Indonesia, Philippines, Singapore
- Participation in industry consultations and working groups
- Position Yuno as thought leader in orchestrator compliance
- Build relationships before enforcement situations arise

#### 3.4 Compliance Program Documentation
**Owner:** Head of Compliance
**Priority:** MEDIUM

Create comprehensive compliance documentation:
- Written policies and procedures
- Training materials and records
- Audit trails and decision documentation
- Board and management reporting frameworks
- Third-party management procedures

---

## PART IV: KEY AMBIGUITIES AND JUDGMENT CALLS

### 1. Where Does Orchestrator Responsibility Begin and End?

**The Core Ambiguity:** No jurisdiction has explicitly defined KYB obligations for payment orchestrators. Yuno's legal obligations must be inferred from:
- General AML/CFT principles
- Payment services regulations designed for different business models
- Regulatory statements about "payment chain responsibility"
- Analogies to similar businesses

**Our Judgment:** We believe regulators will increasingly view orchestrators as having independent compliance obligations, particularly where:
- The orchestrator has a direct merchant relationship
- The orchestrator makes routing decisions affecting regulatory jurisdiction
- The orchestrator has visibility that PSPs lack
- The orchestrator derives commercial benefit from the payment flow

Yuno meets all four criteria. We recommend proceeding as though Yuno has independent KYB obligations rather than waiting for regulatory clarification that may come in the form of enforcement.

### 2. Adequacy of Contractual Risk Transfer

**The Core Ambiguity:** Do Yuno's contracts with PSPs effectively transfer compliance risk?

**Our Judgment:** For regulatory purposes, no. For commercial purposes, partially.

- Regulators will assess Yuno's conduct against their standards, not contract terms
- However, if Yuno faces enforcement, robust contracts may support indemnification claims against PSP partners
- Contract terms may also affect commercial negotiations with PSPs facing their own regulatory pressure

### 3. Regulatory Interpretation of "Payment Chain"

**The Core Ambiguity:** How broadly will regulators interpret "payment chain responsibility"?

**Our Judgment:** We expect expanding interpretation over time. The Indonesian statement is an early signal of a broader trend. FATF guidance, EU regulatory developments, and U.S. enforcement patterns all suggest that:
- Technology platforms will face increasing scrutiny
- "We're just technology" defenses will become less effective
- Substance-over-form analysis will dominate

### 4. Proportionality of Compliance Investment

**The Core Ambiguity:** How much should Yuno invest in compliance infrastructure given uncertain legal requirements?

**Our Judgment:** The proposed program is calibrated to:
- Address the most critical gaps (sanctions screening, beneficial ownership for high-risk)
- Build scalable infrastructure for future requirements
- Demonstrate good faith to regulators and commercial partners
- Avoid operational paralysis from over-engineering

We recommend this level of investment as a reasonable balance between legal risk mitigation and business needs.

---

## PART V: RECOMMENDATIONS SUMMARY

### Prioritized Action List

| Priority | Action | Owner | Timeline | Resources |
|----------|--------|-------|----------|-----------|
| 1 | Philippine PSP engagement | Partnerships | Immediate | Leadership time |
| 2 | Sanctions screening implementation | Compliance | 7 days | $50-100K/year |
| 3 | Investor briefing materials | Legal/Finance | 14 days | Internal |
| 4 | Independent gap analysis | Legal | 30 days | $75-150K |
| 5 | High-risk merchant EDD | Compliance | 30 days | Internal + vendor |
| 6 | Tiered KYB framework | Compliance/Product | 60 days | $200-400K implementation |
| 7 | PSP contract renegotiation | Legal/Partnerships | 90 days | Internal |
| 8 | Singapore MAS engagement | Legal | 60 days | $50-100K (external counsel) |
| 9 | Beneficial ownership verification | Compliance | 90 days | $100-200K/year |
| 10 | Consolidated monitoring | Engineering/Compliance | 180 days | $500K-1M |

### Resource Requirements

**Immediate (0-30 days):** $125-250K + significant leadership time
**Short-term (30-90 days):** $350-700K implementation costs
**Medium-term (90+ days):** $600K-1.2M + ongoing operational costs

**Ongoing Annual Costs:** Approximately $350-500K for sanctions screening, beneficial ownership verification, and monitoring tools

### Success Metrics

1. **Regulatory:** No adverse regulatory findings or enforcement actions in priority markets
2. **Commercial:** Retention of Philippine PSP partnership; satisfactory completion of enterprise client audits
3. **Investor Relations:** Positive response to compliance briefings; no investor exits citing compliance concerns
4. **Operational:** 100% sanctions screening coverage; beneficial ownership verified for all high-risk merchants

---

## CONCLUSION

Yuno faces genuine regulatory exposure following the Indonesian enforcement action. While the company's contractual arrangements with PSPs were designed to allocate compliance responsibility, these arrangements do not bind regulators and may prove insufficient as "payment chain responsibility" doctrines expand.

The good news: Yuno's current gaps are addressable with reasonable investment, and proactive remediation can position the company favorably with regulators, commercial partners, and investors. The proposed program balances risk mitigation against operational practicality.

We recommend proceeding with the immediate actions outlined above and scheduling a follow-up discussion with the executive team within 30 days to assess progress and adjust the roadmap as needed.

---

**APPENDIX A: Regulatory Framework Details**

### Indonesia - Key Regulations

- Bank Indonesia Regulation No. 4 of 2025 on Payment System Policy
- Bank Indonesia Regulation No. 10 of 2025 on Payment System Industry Regulation (effective March 31, 2026)
- Indonesia Payment System Blueprint 2025-2030
- OJK Regulation No. 3 of 2024 on Financial Sector Technology Innovation

### Philippines - Key Regulations

- BSP Circular No. 1206 (Series of 2024) - Money Service Business Rules
- BSP Circular No. 1170 - Electronic KYC Verification
- Manual of Regulations for Non-bank Financial Institutions (MORNBFI)
- Merchant Acquirer License (MAL) Guidelines (January 2025)

### Singapore - Key Regulations

- Payment Services Act 2019 (effective January 28, 2020)
- MAS Notice PS-N01 (AML/CFT requirements)
- MAS Guidelines on Licensing for Payment Service Providers

---

**APPENDIX B: Glossary of Terms**

| Term | Definition |
|------|------------|
| KYB | Know Your Business - due diligence processes for business client onboarding |
| KYC | Know Your Customer - due diligence processes for individual customer verification |
| AML | Anti-Money Laundering |
| CFT | Combating the Financing of Terrorism |
| PSP | Payment Service Provider |
| MAS | Monetary Authority of Singapore |
| BSP | Bangko Sentral ng Pilipinas (Central Bank of the Philippines) |
| BI | Bank Indonesia |
| OJK | Otoritas Jasa Keuangan (Indonesia Financial Services Authority) |
| EDD | Enhanced Due Diligence |
| FATF | Financial Action Task Force |
| SAR | Suspicious Activity Report |
| UBO | Ultimate Beneficial Owner |
| PEP | Politically Exposed Person |
| MAL | Merchant Acquirer License |
| MORNBFI | Manual of Regulations for Non-bank Financial Institutions |

---

*This memorandum constitutes legal advice and is protected by attorney-client privilege. Distribution should be limited to authorized recipients.*
