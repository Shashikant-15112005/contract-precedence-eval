# task_06: Claims-Made Insurance: Interrelated Prior Demand Deeming & 70/30 Soft Hammer

**Category:** Insurance Coverage & Claims-Made Endorsements | **Difficulty:** Hard

## Why It's Hard
Requires linking a May 2026 class action back to an unreported Nov 2024 demand letter under the Section 5.1 Interrelated Claims Deeming Rule (barring coverage), drawing covered Defense Costs from Endorsement No. 1's $500k Supplemental Defense Allowance before eroding the $5M primary limit, and computing 70/30 co-insurance splits on both post-refusal defense costs and excess judgment under the Section 6.1 Soft Hammer Clause.

## Contract Document
```text
EXECUTIVE & PROFESSIONAL LIABILITY INSURANCE POLICY (CLAIMS-MADE AND REPORTED)
Policy Number: EPL-2026-9904
Insured: Sterling FinTech Solutions Inc.

DECLARATIONS
- Policy Period: January 1, 2026 (12:01 AM) to December 31, 2026 (11:59 PM)
- Automatic Extended Reporting Window: 45 calendar days after Policy Period expiration (through February 14, 2027) ONLY for Claims first made against the Insured during the Policy Period.
- Retroactive Date: January 1, 2023
- Prior & Pending Demand Date: January 1, 2025
- Policy Aggregate Limit of Liability: $5,000,000.00
- Per-Claim Self-Insured Retention (Deductible): $100,000.00 (Applies to each separate covered Claim; Insured must pay the first $100,000.00 of covered Loss/Defense Costs before Insurer's payment obligation attaches).

SECTION I — INSURING AGREEMENT & TEMPORAL CONDITIONS
1.1 Coverage Grant. Insurer shall pay Covered Loss (including Defense Costs and Settlements/Judgments) in excess of the Per-Claim Retention resulting from any Claim first made against the Insured during the Policy Period (Jan 1, 2026 – Dec 31, 2026) and reported to Insurer in writing during the Policy Period or within the 45-day Automatic Extended Reporting Window, provided the Wrongful Act occurred on or after the Retroactive Date (Jan 1, 2023).

SECTION IV — DEFENSE COSTS & SUPPLEMENTAL DEFENSE ENDORSEMENT
4.1 Defense Inside the Limits. Except as modified by Endorsement No. 1, all Defense Costs paid by Insurer are part of, and erode dollar-for-dollar, the $5,000,000.00 Policy Aggregate Limit.
4.2 Endorsement No. 1 — Dedicated Supplemental Defense Allowance. NOTWITHSTANDING SECTION 4.1, the Policy provides a separate, additional aggregate allowance of FIVE HUNDRED THOUSAND DOLLARS ($500,000.00) ("Supplemental Defense Allowance") exclusively for covered Defense Costs (in excess of the applicable Per-Claim Retention). Covered Defense Costs paid by Insurer shall be drawn FIRST from this $500,000.00 Supplemental Defense Allowance before eroding a single dollar of the $5,000,000.00 Policy Aggregate Limit.

SECTION V — INTERRELATED CLAIMS DEEMING RULE & PRIOR NOTICE EXCLUSION
5.1 Interrelated Claims Single-Claim Deeming Rule. All Claims arising out of, based upon, or attributable to the same Wrongful Act or a series of logically or causally interrelated Wrongful Acts shall be deemed to be a SINGLE CLAIM, and such Single Claim shall be deemed to have been FIRST MADE on the earliest date on which the earliest of such interrelated Claims (including any written pre-suit demand letter for monetary or non-monetary relief) was first received by the Insured.
5.2 Prior Demand / Prior & Pending Exclusion. No coverage shall apply to any Claim (or interrelated series of Claims under Section 5.1) deemed first made prior to the Policy Period (January 1, 2026) or involving any written demand or proceeding pending prior to the Prior & Pending Demand Date (January 1, 2025).

SECTION VI — CONSENT TO SETTLE & 70/30 SOFT HAMMER CLAUSE
6.1 Soft Hammer Co-Insurance Rule. If Insurer recommends a settlement of a covered Claim that is unconditionally acceptable to the claimant ("Recommended Settlement Amount"), and the Insured refuses to consent to such settlement and elects to continue litigating:
  (a) Insurer's liability for Covered Loss shall be capped at:
      (i) 100% of covered Defense Costs incurred up to the date of the Insured's refusal, PLUS the Recommended Settlement Amount (less the $100,000.00 Retention); PLUS
      (ii) SEVENTY PERCENT (70%) of any additional covered Defense Costs incurred AFTER the date of refusal; PLUS
      (iii) SEVENTY PERCENT (70%) of the amount by which any final judgment or subsequent settlement exceeds the Recommended Settlement Amount.
  (b) The remaining THIRTY PERCENT (30%) of post-refusal Defense Costs and THIRTY PERCENT (30%) of the excess judgment/settlement above the Recommended Settlement Amount shall be borne solely by the Insured and shall not be covered under this Policy.
```

## Task Prompt
You are coverage counsel calculating exact insurer payouts, insured out-of-pocket costs, and remaining policy limits across three claims (`CLAIM-A`, `CLAIM-B`, `CLAIM-C`) under the attached Claims-Made Professional Liability Policy (`EPL-2026-9904`).

### Chronological Claims Submitted by Insured
1. **`CLAIM-A` (Ledger Sync Software Defect — Settled Without Hammer Dispute):**
   - **Wrongful Act Date:** March 15, 2024 (after the Jan 1, 2023 Retroactive Date).
   - **First Written Demand / Lawsuit Received by Insured:** February 10, 2026.
   - **Reported to Insurer:** February 18, 2026.
   - **Financials:** Insured incurred **$450,000.00** in Defense Costs and settled the claim with Insurer's consent for **$1,200,000.00** (Total gross Loss + Defense Costs = **$1,650,000.00**).
   - *Retention application rule:* Apply the $100,000.00 Per-Claim Retention to Defense Costs first (so Insured pays the first $100,000.00 of Defense Costs; Insurer pays the remaining $350,000.00 of Defense Costs + $1,200,000.00 settlement).

2. **`CLAIM-B` (2026 Class Action Linked to a November 2024 Pre-Suit Demand Letter):**
   - **Wrongful Act Date:** August 2024 (an algorithmic fee overcharge on enterprise accounts).
   - **Prior Demand History:** On **November 12, 2024**, counsel for one enterprise customer sent Insured a written demand letter demanding a $45,000 refund and system remediation for the exact same August 2024 algorithmic fee overcharge. Insured did not report the Nov 2024 letter to any insurer.
   - **Lawsuit Served:** On **May 4, 2026**, a class of enterprise customers (including the Nov 2024 claimant) served a formal lawsuit seeking damages for the same August 2024 algorithmic fee overcharge. Insured reported the lawsuit to Insurer on May 6, 2026.
   - **Financials:** Insured incurred **$300,000.00** in Defense Costs and paid **$900,000.00** in settlement (Total = **$1,200,000.00**).

3. **`CLAIM-C` (API Outage Lawsuit Invoking the Section 6.1 Soft Hammer Clause):**
   - **Wrongful Act Date:** June 1, 2025 (unrelated to Claims A and B).
   - **First Written Demand / Lawsuit Received:** November 10, 2026 (during Policy Period).
   - **Reported to Insurer:** January 15, 2027 (within the 45-day Automatic Extended Reporting Window under Section 1.1).
   - **Settlement Refusal & Final Judgment:**
     - Up to the date of the settlement recommendation, Insured had incurred **$300,000.00** in Defense Costs.
     - Claimant agreed in writing to settle for **$800,000.00** ("Recommended Settlement Amount"), and Insurer recommended accepting it.
     - Insured **refused** to consent and continued litigating.
     - After the refusal, Insured incurred an additional **$200,000.00** in post-refusal Defense Costs, and the court entered a final judgment of **$1,400,000.00** (which is **$600,000.00** in excess of the $800,000.00 Recommended Settlement Amount).
     - *Retention & Allowance Ordering:* Apply the $100,000.00 Per-Claim Retention to the pre-refusal Defense Costs first. Draw covered Defense Costs paid by Insurer from whatever remains of the $500,000.00 Endorsement No. 1 Supplemental Defense Allowance before eroding the $5,000,000.00 Policy Aggregate Limit.

### Instructions
Calculate the exact coverage status, Insurer payout, Insured out-of-pocket exposure (including Retention, uncovered claims, and 30% Hammer co-insurance), and remaining Policy Aggregate Limit after all three claims are resolved.

Return ONLY a valid JSON object matching this exact schema:
```json
{
  "claims": {
    "CLAIM-A": {
      "is_covered": <boolean>,
      "insurer_defense_payout_usd": <float>,
      "insurer_indemnity_payout_usd": <float>,
      "insurer_total_payout_usd": <float>,
      "insured_out_of_pocket_usd": <float>
    },
    "CLAIM-B": {
      "is_covered": <boolean>,
      "insurer_defense_payout_usd": <float>,
      "insurer_indemnity_payout_usd": <float>,
      "insurer_total_payout_usd": <float>,
      "insured_out_of_pocket_usd": <float>
    },
    "CLAIM-C": {
      "is_covered": <boolean>,
      "insurer_defense_payout_usd": <float>,
      "insurer_indemnity_payout_usd": <float>,
      "insurer_total_payout_usd": <float>,
      "insured_out_of_pocket_usd": <float>
    }
  },
  "total_insurer_payout_all_claims_usd": <float>,
  "total_insured_out_of_pocket_all_claims_usd": <float>,
  "supplemental_defense_allowance_remaining_usd": <float>,
  "primary_policy_aggregate_limit_remaining_usd": <float>
}
```
