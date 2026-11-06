# task_01: SaaS MSA Multi-Tier Liability Cap, Super-Cap & Cross-Bucket Erosion

**Category:** Limitation of Liability & Indemnification | **Difficulty:** Hard

## Why It's Hard
Requires resolving a 4-way clause interaction: (1) including one-time Implementation Fees in the Section 1.4/11.1 12-month lookback cap ($315k vs $270k), (2) applying Section 11.4 cross-bucket erosion where General Cap payouts reduce the 3x Data Super-Cap from $945k to $630k, (3) distinguishing Section 5 non-PII Confidentiality (uncapped + lost profits permitted under 11.5) from Section 6 PII Data Security (capped at remaining Super-Cap + lost profits barred).

## Contract Document
```text
MASTER SAAS AND IMPLEMENTATION SERVICES AGREEMENT
Document ID: MSA-2025-8841
Effective Date: May 1, 2025

BETWEEN:
  Vanguard Cloud Systems, Inc. ("Provider")
AND:
  Meridian Global Logistics Corp. ("Customer")

1. DEFINITIONS
1.1 "Affiliate" means any entity controlling, controlled by, or under common control with a Party.
1.2 "Confidential Information" has the meaning set forth in Section 5.1, and expressly excludes Customer Personal Data governed exclusively by Section 6 (Data Protection).
1.3 "Customer Personal Data" means personally identifiable information (PII) of Customer's employees or end-consumers uploaded to the Hosted Service.
1.4 "Fees" means all monetary amounts actually paid by Customer to Provider under any Order Form, including both Subscription Fees and Implementation Services Fees.

2. ORDER FORM NO. 1 (INCORPORATED BY REFERENCE)
2.1 Term: May 1, 2025 through April 30, 2027 (24 Months).
2.2 Subscription Fee: $22,500.00 per month ($270,000.00 per 12-month contract year), payable monthly in advance.
2.3 One-Time Implementation Services Fee: $45,000.00, invoiced and paid in full on May 15, 2025.
2.4 Payment History Stipulation: Between May 1, 2025 and April 30, 2026 (the first 12 months), Customer timely paid all twelve (12) monthly Subscription Fee installments ($270,000.00) plus the Implementation Services Fee ($45,000.00), for total cumulative Fees paid of $315,000.00.

5. CONFIDENTIALITY
5.1 Each Party shall protect the other Party's non-public business, technical, and financial information ("Confidential Information"), including proprietary pricing algorithms and supply-chain routing models. For clarity, incidents involving Customer Personal Data are governed solely by Section 6 and shall not be deemed breaches of this Section 5.

6. DATA PROTECTION AND SECURITY
6.1 Provider shall maintain SOC 2 Type II administrative, physical, and technical safeguards to protect Customer Personal Data against unauthorized access, exfiltration, or disclosure ("Data Security Breach").

9. INTELLECTUAL PROPERTY INDEMNIFICATION
9.1 Provider shall defend Customer against any third-party claim alleging that the Hosted Service infringes any valid United States patent, copyright, or trade secret, and shall indemnify Customer for all resulting court-awarded damages or Provider-approved settlement amounts ("IP Infringement Claim").

11. LIMITATION OF LIABILITY
11.1 General Liability Cap. EXCEPT AS EXPRESSLY PROVIDED IN SECTIONS 11.2 AND 11.3, IN NO EVENT SHALL EITHER PARTY'S AGGREGATE LIABILITY ARISING OUT OF OR RELATED TO THIS AGREEMENT EXCEED ONE HUNDRED PERCENT (100%) OF THE TOTAL FEES ACTUALLY PAID BY CUSTOMER TO PROVIDER UNDER THIS AGREEMENT IN THE TWELVE (12) MONTH PERIOD IMMEDIATELY PRECEDING THE EVENT GIVING RISE TO THE FIRST CLAIM ("GENERAL CAP").

11.2 Data Protection Super-Cap. NOTWITHSTANDING SECTION 11.1, AND SUBJECT TO SECTION 11.4, PROVIDER'S AGGREGATE LIABILITY FOR ALL CLAIMS ARISING OUT OF OR RELATING TO A BREACH OF SECTION 6 (DATA PROTECTION AND SECURITY) SHALL NOT EXCEED THREE TIMES (3X) THE GENERAL CAP ("DATA SUPER-CAP").

11.3 Uncapped Claims (Carve-Outs). NOTWITHSTANDING SECTIONS 11.1 AND 11.2, NEITHER THE GENERAL CAP NOR THE DATA SUPER-CAP SHALL APPLY TO LIABILITY ARISING FROM:
  (a) Provider's indemnification obligations for Third-Party IP Infringement Claims under Section 9.1;
  (b) Either Party's breach of its Confidentiality obligations under Section 5 (which, per Section 1.2 and Section 5.1, excludes Customer Personal Data claims under Section 6); or
  (c) A Party's gross negligence, willful misconduct, or fraud.

11.4 Cross-Bucket Erosion Rule. THE GENERAL CAP AND THE DATA SUPER-CAP ARE NOT INDEPENDENT CUMULATIVE POOLS. Any amounts paid or payable by Provider for claims subject to the Section 11.1 General Cap shall reduce dollar-for-dollar the remaining available limit under the Section 11.2 Data Super-Cap. Conversely, any amounts paid or payable by Provider for Uncapped Claims under Section 11.3(a)-(c) shall NOT reduce or erode either the General Cap or the Data Super-Cap. Within any single cap tier, earlier-incurred or concurrently resolved General Cap claims are applied first before calculating remaining Data Super-Cap availability.

11.5 Exclusion of Consequential Damages and Exceptions. NEITHER PARTY SHALL BE LIABLE FOR ANY INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS OR LOST REVENUE, EVEN IF ADVISED OF THEIR POSSIBILITY; PROVIDED, HOWEVER, THAT THIS SECTION 11.5 EXCLUSION SHALL NOT APPLY TO:
  (i) Damages arising from a breach of Section 5 (Confidentiality);
  (ii) Third-party settlement amounts or damages expressly indemnified under Section 9.1 (IP Indemnification); or
  (iii) A Party's willful misconduct or fraud.
```

## Task Prompt
You are a senior commercial contracts counsel reviewing a dispute under the attached Master SaaS and Implementation Services Agreement (`MSA-2025-8841`).

### Factual Scenario
On May 10, 2026 (immediately following the completion of the first 12-month period from May 1, 2025 to April 30, 2026, during which Customer paid all scheduled Subscription and Implementation Fees), four distinct claims arise concurrently against Provider:

1. **`claim_sla_outage` (Service Outage & SLA Failure):** A configuration defect caused a 72-hour platform outage. Customer incurred **$410,000.00** in direct replacement hosting and recovery costs, plus **$180,000.00** in documented lost enterprise customer sales profits. There was no gross negligence or willful misconduct.
2. **`claim_data_breach` (PII Data Security Breach):** An unpatched third-party library resulted in unauthorized exfiltration of Customer Personal Data (governed by Section 6). Customer incurred **$780,000.00** in direct forensic investigation and mandatory statutory breach notification costs, plus **$120,000.00** in indirect reputational/lost revenue damages. The parties stipulate this arose from ordinary negligence (not gross negligence or willful misconduct).
3. **`claim_ip_indemnity` (Third-Party Patent Infringement):** A third-party patent holder sued Customer over the Hosted Service. Provider approved and executed a binding third-party settlement of **$1,250,000.00** under Section 9.1.
4. **`claim_trade_secret_leak` (Section 5 Confidentiality Breach):** A Provider account manager improperly disclosed Customer's proprietary supply-chain pricing algorithm (non-PII Confidential Information governed by Section 5) to an unauthorized party. Customer suffered **$220,000.00** in direct remediation/re-engineering costs and **$95,000.00** in documented lost profits directly attributable to the disclosure.

### Instructions
Calculate the exact legally recoverable dollar amount from Provider for each of the four claims and in aggregate under the Agreement. Pay strict attention to:
- The definition of "Fees" in Section 1.4 and Order Form No. 1 when calculating the 12-month lookback General Cap and the 3x Data Super-Cap.
- Which claims allow vs. bar consequential/lost profit damages under Section 11.5.
- Which claims are subject to the General Cap (Section 11.1), the Data Super-Cap (Section 11.2), or Uncapped Carve-Outs (Section 11.3).
- The Cross-Bucket Erosion Rule in Section 11.4 between General Cap claims and Data Super-Cap claims.

Return ONLY a valid JSON object matching this exact schema (all dollar figures rounded to 2 decimal places):
```json
{
  "general_cap_usd": <float>,
  "initial_data_super_cap_usd": <float>,
  "remaining_data_super_cap_after_erosion_usd": <float>,
  "claims": {
    "claim_sla_outage": {
      "cap_category": "<general_cap | data_super_cap | uncapped>",
      "consequential_damages_recoverable": <boolean>,
      "recoverable_amount_usd": <float>
    },
    "claim_data_breach": {
      "cap_category": "<general_cap | data_super_cap | uncapped>",
      "consequential_damages_recoverable": <boolean>,
      "recoverable_amount_usd": <float>
    },
    "claim_ip_indemnity": {
      "cap_category": "<general_cap | data_super_cap | uncapped>",
      "consequential_damages_recoverable": <boolean>,
      "recoverable_amount_usd": <float>
    },
    "claim_trade_secret_leak": {
      "cap_category": "<general_cap | data_super_cap | uncapped>",
      "consequential_damages_recoverable": <boolean>,
      "recoverable_amount_usd": <float>
    }
  },
  "total_recoverable_usd": <float>
}
```
