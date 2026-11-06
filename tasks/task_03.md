# task_03: Most Favored Nation (MFN) Effective Price & Retroactive Ratchet Audit

**Category:** Commercial Pricing & MFN Audits | **Difficulty:** Hard

## Why It's Hard
Requires filtering 5 comparator contracts against four distinct Section 4.3 exemptions (government entity, >120% volume tier, 3-year 100% upfront prepayment), computing Effective Annual Per-Seat Price under Section 4.2 by amortizing Year-1 signing rebates, free support credits, and waived onboarding fees, and applying quarterly retroactive ratchet-down adjustments across Q1–Q4.

## Contract Document
```text
ENTERPRISE SOFTWARE LICENSING AND MOST FAVORED NATION (MFN) AGREEMENT
Document ID: MFN-2026-4402
Contract Year 1: January 1, 2026 – December 31, 2026

1. BASELINE COMMERCIAL TERMS (CUSTOMER: APEX CAPITAL HOLDINGS)
1.1 Licensed Volume: 2,500 Enterprise Seats.
1.2 Baseline Unit Price: $120.00 per seat per year ($300,000.00 total annual fee).
1.3 Billing & Payment Schedule: Billed and paid in four (4) equal quarterly installments of $75,000.00 on the first day of each calendar quarter (Q1: Jan 1, Q2: Apr 1, Q3: Jul 1, Q4: Oct 1).

4. MOST FAVORED NATION (MFN) PRICE PROTECTION
4.1 MFN Rate Guarantee. If, at any time during Contract Year 1, Licensor enters into a new or amended license agreement with any Third-Party Customer ("Comparator Deal") that provides a lower Effective Annual Per-Seat Price (as calculated under Section 4.2) than the price then in effect for Apex Capital Holdings, and such Comparator Deal is NOT an Exempt Transaction under Section 4.3, Licensor shall automatically reduce Apex's unit price to match that lower Effective Annual Per-Seat Price.

4.2 Calculation of Effective Annual Per-Seat Price. To prevent circumvention of Section 4.1 through disguised discounts, the "Effective Annual Per-Seat Price" of any Comparator Deal shall be computed using the following formula:
  Effective Annual Per-Seat Price = (Annualized Headline Seat Fee - Year 1 Signing Rebates - Year 1 Free Support/Service Credits - Waived Standard Onboarding Fees) / Comparator Seat Count.
  For clarity, only rebates, credits, and fee waivers applicable to Year 1 of the Comparator Deal are deducted in this formula.

4.3 Exempt Transactions (MFN Carve-Outs). NOTWITHSTANDING SECTION 4.1, a Comparator Deal shall NOT trigger an MFN adjustment if ANY ONE OR MORE of the following exemptions apply:
  (a) Public Sector / Non-Profit Exemption: The Comparator Customer is a federal, state, or municipal government agency, public university, or registered 501(c)(3) non-profit organization;
  (b) Volume Tier Exemption: The Comparator Deal commits to a contracted seat count strictly exceeding one hundred twenty percent (120%) of Apex's contracted seat count (i.e., strictly greater than 3,000 seats);
  (c) Multi-Year Full Prepayment Exemption: The Comparator Deal has a binding non-cancellable term of at least three (3) years AND requires one hundred percent (100%) of the entire multi-year contract value to be paid upfront within thirty (30) days of signing; or
  (d) Distressed / Insolvency Restructuring: The pricing is granted pursuant to a court-supervised bankruptcy reorganization under Chapter 11.

4.4 Retroactive Quarterly Application & Ratchet-Down Rule.
  (a) Any qualifying MFN price reduction takes effect retroactively as of the first day of the calendar quarter in which the qualifying Comparator Deal was executed (e.g., a deal signed on May 18 in Q2 applies to the entirety of Q2, Q3, and Q4, unless superseded by an even lower qualifying price in a later quarter).
  (b) MFN adjustments are strictly downward ("ratchet-down only"): once Apex's unit price is reduced in a quarter, it remains at that reduced rate for subsequent quarters of Contract Year 1 unless a subsequent qualifying Comparator Deal establishes an even lower Effective Annual Per-Seat Price.
  (c) Year-End Audit Refund: At the conclusion of Contract Year 1, Licensor shall refund to Apex the difference between the $300,000.00 actually paid by Apex ($75,000.00 per quarter) and the sum of the adjusted quarterly fees across Q1, Q2, Q3, and Q4. (Note: For any quarter, Adjusted Quarterly Fee = (Applicable Annual Per-Seat Price * 2,500 seats) / 4).
```

## Task Prompt
You are conducting the Year-End MFN Compliance Audit for Apex Capital Holdings under the attached Enterprise Software Licensing Agreement (`MFN-2026-4402`) for Contract Year 1 (2026).

### Comparator Deals Executed by Licensor in 2026
During 2026, Apex paid its four scheduled quarterly installments of **$75,000.00** each (**$300,000.00** total). An independent auditor extracted all five (5) comparator enterprise contracts executed by Licensor in 2026:

1. **`DEAL-101` (Executed February 14, 2026 — Q1):**
   - Customer: **Ohio Department of Transportation** (State Government Agency)
   - Seat Count: **2,000 seats** | Term: 1 Year | Payment: Annual
   - Headline Price: **$88.00/seat/year** | Rebates/Credits/Waivers: **$0**
2. **`DEAL-102` (Executed April 22, 2026 — Q2):**
   - Customer: **Vortex Financial Corp.** (Private Commercial Enterprise)
   - Seat Count: **3,200 seats** | Term: 1 Year | Payment: Quarterly
   - Headline Price: **$92.00/seat/year** | Year 1 Signing Rebate: **$16,000.00**
3. **`DEAL-103` (Executed May 19, 2026 — Q2):**
   - Customer: **Kestrel Retail Group Inc.** (Private Commercial Enterprise)
   - Seat Count: **2,200 seats** | Term: 2 Years | Payment: Billed semi-annually (not paid 100% upfront)
   - Headline Price: **$115.00/seat/year** | Year 1 Signing Rebate: **$22,000.00** | Waived Standard Onboarding Fee in Year 1: **$11,000.00** | Free Support Credits: **$0**
4. **`DEAL-104` (Executed August 11, 2026 — Q3):**
   - Customer: **Pinnacle Freight Systems LLC** (Private Commercial Enterprise)
   - Seat Count: **1,800 seats** | Term: 3 Years | Payment: **100% of entire 3-year contract value paid upfront at signing**
   - Headline Price: **$85.00/seat/year** | Rebates/Credits/Waivers: **$0**
5. **`DEAL-105` (Executed September 3, 2026 — Q3):**
   - Customer: **Solaris Biotech Inc.** (Private Commercial Enterprise)
   - Seat Count: **2,500 seats** | Term: 2 Years | Payment: Billed annually
   - Headline Price: **$100.00/seat/year** | Year 1 Signing Rebate: **$5,000.00** | Year 1 Free Support Credits: **$10,000.00** | Waived Onboarding Fees: **$0**

### Instructions
Evaluate each comparator deal under Sections 4.1–4.4 and compute Apex's exact quarterly rates, adjusted fees, and Year-1 MFN refund.

Return ONLY a valid JSON object matching this exact schema (all dollar amounts rounded to 2 decimal places):
```json
{
  "comparator_analysis": {
    "DEAL-101": {"effective_annual_seat_price_usd": <float>, "qualifies_for_mfn": <boolean>, "exemption_reason": "<gov_or_nonprofit | volume_over_120_pct | three_year_upfront | bankruptcy | none>"},
    "DEAL-102": {"effective_annual_seat_price_usd": <float>, "qualifies_for_mfn": <boolean>, "exemption_reason": "<gov_or_nonprofit | volume_over_120_pct | three_year_upfront | bankruptcy | none>"},
    "DEAL-103": {"effective_annual_seat_price_usd": <float>, "qualifies_for_mfn": <boolean>, "exemption_reason": "<gov_or_nonprofit | volume_over_120_pct | three_year_upfront | bankruptcy | none>"},
    "DEAL-104": {"effective_annual_seat_price_usd": <float>, "qualifies_for_mfn": <boolean>, "exemption_reason": "<gov_or_nonprofit | volume_over_120_pct | three_year_upfront | bankruptcy | none>"},
    "DEAL-105": {"effective_annual_seat_price_usd": <float>, "qualifies_for_mfn": <boolean>, "exemption_reason": "<gov_or_nonprofit | volume_over_120_pct | three_year_upfront | bankruptcy | none>"}
  },
  "quarterly_applicable_seat_price_usd": {
    "Q1": <float>,
    "Q2": <float>,
    "Q3": <float>,
    "Q4": <float>
  },
  "quarterly_refund_due_usd": {
    "Q1": <float>,
    "Q2": <float>,
    "Q3": <float>,
    "Q4": <float>
  },
  "total_year_1_refund_usd": <float>
}
```
