# task_04: Anti-Assignment, Reverse Triangular Merger & Safe Harbor Net-Worth Proviso

**Category:** Corporate M&A & Change of Control | **Difficulty:** Hard

## Why It's Hard
Requires recognizing that a reverse triangular merger triggers Section 16.2 deemed assignment, verifying parent-guaranty cures for Tangible Net Worth (Total Assets minus Intangibles minus Liabilities), catching Affiliate attribution to a Schedule D Restricted Competitor, and applying the two-tier Section 16.3(d) transfer + scale surcharge ($75k + $125k = $200k vs $0 for internal restructurings).

## Contract Document
```text
EXCLUSIVE PATENT AND TECHNOLOGY LICENSE AGREEMENT
Document ID: EPTLA-2025-772

1. DEFINITIONS
1.1 "Affiliate" means any entity that directly or indirectly controls, is controlled by, or is under common control with a Party (where "control" means ownership of >50% of voting securities).
1.2 "Change of Control" means: (a) the acquisition by any person or group of more than fifty percent (50%) of the voting equity of Licensee; (b) any merger, consolidation, or reorganization of Licensee with or into another entity, EXPRESSLY INCLUDING a reverse triangular merger in which a subsidiary of an acquirer merges into Licensee and Licensee survives as a wholly-owned subsidiary of the acquirer; or (c) the sale of all or substantially all of Licensee's assets.
1.3 "Restricted Competitor" means any entity listed on Schedule D, or any Affiliate of an entity listed on Schedule D.

16. ASSIGNMENT AND CHANGE OF CONTROL
16.1 General Anti-Assignment Rule. Except as expressly permitted under Section 16.3, Licensee shall not assign, delegate, or transfer this Agreement, in whole or in part, by operation of law or otherwise, without Licensor's prior written consent. Any attempted assignment or deemed assignment in violation of this Section 16 shall be null and void ab initio and shall constitute an immediate, non-curable material breach.
16.2 Change of Control Deemed Assignment. Any Change of Control of Licensee (as defined in Section 1.2) shall be deemed an assignment of this Agreement by operation of law subject to Section 16.1.
16.3 Safe Harbor Proviso for Qualified Corporate Transactions. NOTWITHSTANDING SECTIONS 16.1 AND 16.2, Licensor's prior written consent shall NOT be required for an assignment to an Affiliate or a deemed assignment resulting from a Change of Control, PROVIDED THAT ALL FOUR (4) OF THE FOLLOWING CONDITIONS ARE SATISFIED:
  (a) Non-Competitor Condition: The assignee, acquirer, or ultimate parent resulting from the transaction is NOT a Restricted Competitor (as defined in Section 1.3 and Schedule D);
  (b) Tangible Net Worth Threshold: Immediately following the closing of the transaction, the surviving Licensee (or assignee) maintains a verified Tangible Net Worth (Total Assets minus Intangible Assets minus Total Liabilities) of at least FIFTY MILLION DOLLARS ($50,000,000.00), OR the ultimate parent executes an unconditional corporate guaranty prior to closing and itself has a Tangible Net Worth of at least $50,000,000.00;
  (c) Advance Notice & Financial Certification: Licensee delivers written notice of the transaction together with a CFO-certified pro forma balance sheet to Licensor at least FIFTEEN (15) CALENDAR DAYS prior to the closing date; AND
  (d) Volume Expansion Transfer Fee: If the transaction is a Change of Control (including a reverse triangular merger) with an unaffiliated third party (i.e., not a purely internal reorganization among existing Affiliates), Licensee shall pay to Licensor a one-time Transfer Administration Fee of SEVENTY-FIVE THOUSAND DOLLARS ($75,000.00); plus, if the acquirer's consolidated annual revenue exceeds $500,000,000.00, an additional Scale Surcharge of ONE HUNDRED TWENTY-FIVE THOUSAND DOLLARS ($125,000.00) (for a combined fee of $200,000.00). Purely internal reorganizations among existing Affiliates where ultimate parent ownership is unchanged owe $0.00 under this Section 16.3(d).

SCHEDULE D — RESTRICTED COMPETITORS LIST
1. CyberDyne Robotics Inc.
2. OmniCorp Defense Systems PLC
3. BlackMesa Analytics GmbH
```

## Task Prompt
You are corporate M&A counsel evaluating four proposed transactions (`TX-1`, `TX-2`, `TX-3`, `TX-4`) under the attached Exclusive Patent and Technology License Agreement (`EPTLA-2025-772`).

### Proposed Transactions to Evaluate
1. **`TX-1` (Reverse Triangular Merger with Private Equity Buyer):**
   - Structure: Titan Growth Partners (not on Schedule D and not affiliated with any Schedule D entity; consolidated annual revenue of **$680,000,000.00**) forms MergerSub Inc., which merges into Licensee. Licensee survives as a wholly-owned subsidiary of Titan.
   - Financials: Surviving Licensee's post-closing Tangible Net Worth is **$38,000,000.00** (Total Assets $95M, Goodwill/Intangibles $32M, Total Liabilities $25M). Titan Growth Partners has Tangible Net Worth of $420,000,000.00, and Titan executes an unconditional corporate guaranty prior to closing.
   - Notice: Licensee delivers written notice and CFO-certified pro forma financials **20 calendar days** prior to closing.
2. **`TX-2` (Internal Affiliate Spin-Off / Reorganization):**
   - Structure: Licensee assigns the Agreement to its sister company, Licensee Cloud Ops LLC (both 100% owned by the same existing ultimate parent, Apex Holdings Inc., which is not on Schedule D).
   - Financials: Licensee Cloud Ops LLC has Total Assets of **$85,000,000.00**, Intangible Assets (patents/goodwill) of **$20,000,000.00**, and Total Liabilities of **$12,000,000.00** (Tangible Net Worth = $53,000,000.00).
   - Notice: Licensee delivers written notice and CFO-certified pro forma financials **18 calendar days** prior to closing.
3. **`TX-3` (Acquisition by Subsidiary of Restricted Competitor):**
   - Structure: Vanguard AI Ltd., a wholly-owned subsidiary of **OmniCorp Defense Systems PLC** (listed on Schedule D), acquires 60% of Licensee's voting stock.
   - Financials: Post-closing Tangible Net Worth of Licensee is **$110,000,000.00**.
   - Notice: Delivered **30 calendar days** prior to closing.
4. **`TX-4` (Asset Sale with Late Notice & Intangible Asset Trap):**
   - Structure: Licensee sells substantially all of its assets and assigns the Agreement to Horizon Industrial Corp (an unaffiliated third party not affiliated with any Schedule D entity; consolidated annual revenue of **$310,000,000.00**).
   - Financials: Horizon's post-closing balance sheet shows Total Assets of **$90,000,000.00**, Goodwill and Intangible Assets of **$35,000,000.00**, and Total Liabilities of **$15,000,000.00** (Tangible Net Worth = $40,000,000.00). No parent guaranty exists.
   - Notice: Delivered **10 calendar days** prior to closing.

### Instructions
For each transaction (`TX-1` through `TX-4`), determine:
- Whether it triggers Section 16 (either as a direct assignment or a Change of Control).
- Whether it satisfies the Section 16.3 Safe Harbor (so that Licensor's prior written consent is NOT required).
- Which specific Section 16.3 conditions (`non_competitor`, `tangible_net_worth`, `advance_notice`) failed, if any (empty list `[]` if all passed).
- The exact mandatory transfer/scale fee payable under Section 16.3(d) if the transaction proceeds under the Safe Harbor (or `$0.00` if consent is required / Safe Harbor is unavailable or if exempt as an internal affiliate reorganization).

Return ONLY a valid JSON object matching this exact schema:
```json
{
  "transactions": {
    "TX-1": {
      "triggers_section_16": <boolean>,
      "qualifies_for_safe_harbor_no_consent": <boolean>,
      "failed_safe_harbor_conditions": ["<non_competitor | tangible_net_worth | advance_notice>", ...],
      "section_16_3_d_fee_usd": <float>
    },
    "TX-2": {
      "triggers_section_16": <boolean>,
      "qualifies_for_safe_harbor_no_consent": <boolean>,
      "failed_safe_harbor_conditions": ["<non_competitor | tangible_net_worth | advance_notice>", ...],
      "section_16_3_d_fee_usd": <float>
    },
    "TX-3": {
      "triggers_section_16": <boolean>,
      "qualifies_for_safe_harbor_no_consent": <boolean>,
      "failed_safe_harbor_conditions": ["<non_competitor | tangible_net_worth | advance_notice>", ...],
      "section_16_3_d_fee_usd": <float>
    },
    "TX-4": {
      "triggers_section_16": <boolean>,
      "qualifies_for_safe_harbor_no_consent": <boolean>,
      "failed_safe_harbor_conditions": ["<non_competitor | tangible_net_worth | advance_notice>", ...],
      "section_16_3_d_fee_usd": <float>
    }
  }
}
```
