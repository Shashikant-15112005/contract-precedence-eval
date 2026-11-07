# CONTRACT-PRECEDENCE-EVAL

> Video Walkthrough Link: (https://drive.google.com/file/d/1_OxBmKleAipRW9Y_kkoaKPo-XS85V5xs/view?usp=sharing)

# What is an Eval ?

AI evals (short for evaluations) are systematic test suites and quality checks used to measure how well a large language model (LLM), generative AI application, or AI Agent performs on specific tasks.Think of them like unit tests in traditional software engineering or practice exams for a student. Because AI models produce free-form, probabilistic outputs rather than rigid code, evals help turn subjective "vibes" into objective data.

# What Evals Actually Do ?

- Define Success: They force teams to explicitly write down what a "good" or "correct" AI response looks like before shipping code.

- Catch Regressions: When you update a system prompt, switch to a new model, or tweak a retriever, evals tell you if your changes broke something that used to work.

- Benchmark Models: Companies use them to compare different base models (like deciding whether to upgrade from Claude or OpenAI) to see which fits their use case best.

# The Three Main Ways Evals Are Run:

A) Code-Based Evals (Deterministic): Uses exact rules, regex patterns, or schema validation. (e.g., Did the AI output a valid JSON object? Did it include the required phone number?)

B) LLM-as-a-Judge: Uses a stronger, specialized AI model to review and score the output of the target AI based on a rubric. (e.g., On a scale of 1 to 5, how polite and accurate is this customer service reply?)

C) Human Evaluation: Having real product managers, domain experts, or users manually grade transcripts or edge cases. While expensive and slow, it provides the ultimate ground truth.
                                     
                                     [***CONTRACT-PRECEDENCE-EVAL RUNS ON LLM AS A JUDGE***]

### I took participation in micro1 Eval Hackathon where instead of building an AI agent, the goal is to design a rigorous, reproducible evaluation (5–10 tasks) in a   domain you know well that exposes a real, practical limitation of frontier AI models—and grades it reliably.

# I chose Lawyer / Legal Compliance

The Failure Mode: Models hallucinate or overlook cross-clause overrides and jurisdictional conflict of laws.

Why Frontier Models Fail: Models read contracts sequentially. When Section 4 establishes a standard 30-day notice, but an obscure Section 18.4 carve-out states "Notwithstanding Section 4, in events involving regulatory inquiry, notice is 48 hours and governed by Delaware law with an indemnity cap exclusion", frontier models routinely cite the 30-day rule.

Concrete Task Examples:

Statute of Limitations & Jurisdictional Deadlines: Calculating filing deadlines given tolling rules, court holidays, and forum selection clauses.

Liquidated Damages & Liability Caps: Determining total recoverable damages where specific carve-outs (e.g., willful misconduct, gross negligence, IP infringement) bypass the 1x contract cap.

Termination Right Triggers: Evaluating whether a cure period was violated based on strict notice requirements.

Why It Wins the Rubric: Output is structured JSON (e.g., {"deadline": "2026-12-04", "capped_liability_usd": 1500000, "carve_outs_triggered": ["gross_negligence"]}). Grader is 100% deterministic code (zero LLM-judge subjectivity).

# Contract-Precedence-Eval: Measuring Cross-Clause Override Blindness in Commercial Contracts

## 1. What It Tests
**Contract-Precedence-Eval** measures whether frontier AI models can resolve **hierarchical cross-clause overrides** in commercial contracts—specifically when a general rule in one section is subordinated, carved out, or modified by a `"Notwithstanding"` clause, fee-erosion proviso, accounting hierarchy schedule, or endorsement located pages away.

## 2. Who It's For and Why It Matters
Corporate M&A attorneys, commercial litigators, in-house counsel, and insurance coverage specialists rely on contract review to price risk and calculate exposure. In real practice, contract errors rarely happen because a lawyer misreads a single sentence in isolation; they happen when **two or more clauses interact**:
- Missing a cross-bucket erosion proviso in a SaaS Master Services Agreement misstates liability exposure by **$315,000+**.
- Sending a default notice by email when the boilerplate Notices clause excludes Section 14 defaults invalidates a termination and exposes the terminating party to wrongful repudiation damages.
- Applying standard US GAAP instead of a Stock Purchase Agreement's Schedule 2.6 Accounting Hierarchy swings an M&A earn-out payout by **$1,400,000+**.

## 3. Task Overview (6 Tasks)

| Task ID | Task Title | Core Clause Interaction & Why Frontier Models Fail |
| :--- | :--- | :--- |
| **`task_01`** | **SaaS MSA Multi-Tier Liability Cap, Super-Cap & Cross-Bucket Erosion** | Models must include the $45k Implementation Fee in the 12-month lookback General Cap ($315k vs. $270k), apply Section 11.4 cross-bucket erosion (reducing the $945k 3x Data Super-Cap by the $315k General Cap payout to $630k), and distinguish Section 5 non-PII Confidentiality (uncapped + lost profits permitted under Section 11.5) from Section 6 PII Data Breaches. |
| **`task_02`** | **Dispute Notice Validity, Courier Cutoff & Dual-Jurisdiction Cure Window** | Models must reject an acknowledged Oct 12 email notice under the Section 18.2 physical-courier mandate, apply the post-5:00 PM ET courier cutoff (pushing Deemed Receipt to the 2nd Business Day, Oct 16), reject a partial escrow wire under Section 14.2, and exclude both New York and Mumbai banking holidays (Exhibit C) across a 7-Business-Day cure period. |
| **`task_03`** | **Most Favored Nation (MFN) Effective Price & Retroactive Ratchet Audit** | Models must evaluate 5 comparator deals against four Section 4.3 exemptions (government agency, >120% seat volume, 3-year 100% upfront prepayment), compute Effective Annual Per-Seat Price under Section 4.2 by amortizing Year-1 signing rebates and waived onboarding fees, and apply retroactive quarterly ratchet-down pricing across Q1–Q4. |
| **`task_04`** | **Anti-Assignment, Reverse Triangular Merger & Safe Harbor Net-Worth Proviso** | Models must recognize that a reverse triangular merger triggers Section 16.2 deemed assignment, verify whether a parent guaranty cures a Tangible Net Worth shortfall (Total Assets minus Intangibles minus Liabilities), catch Affiliate attribution to a Schedule D Restricted Competitor, and compute the two-tier Section 16.3(d) transfer + scale fee ($200k vs. $0 for internal restructurings). |
| **`task_05`** | **M&A Earn-Out Adjusted EBITDA & Specific Accounting Hierarchy Override** | Models must enforce Schedule 2.6's 3-tier Accounting Hierarchy where Part I overrides US GAAP: capping transaction advisory add-backs at $400k, subtracting the $120k historical baseline from Buyer overhead allocations, deducting $650k of GAAP-capitalized internal software dev payroll (100% mandatory expensing), and rejecting an undisclosed post-closing OSHA fine add-back. |
| **`task_06`** | **Claims-Made Insurance: Interrelated Prior Demand Deeming & 70/30 Soft Hammer** | Models must link a May 2026 class action back to an unreported Nov 2024 demand letter under the Section 5.1 Interrelated Claims Deeming Rule (barring coverage), draw covered Defense Costs from Endorsement No. 1's $500k Supplemental Defense Allowance before eroding the $5M primary limit, and calculate 70/30 co-insurance splits on post-refusal defense costs and excess judgment under the Section 6.1 Soft Hammer Clause. |

## 4. Grading: How Each Task Is Scored & Validated

Every task is scored by a **100% deterministic Python code-based grader** (`graders/grader.py`)—no subjective LLM-as-judge is used:
- **Numeric Tolerance:** All dollar calculations are checked with a `$0.01` tolerance (`abs(actual - expected) <= 0.01`) to prevent false fails from floating-point rounding.
- **Partial Credit & Strict Binary Pass:** Each task comprises 8 to 24 atomic field checks (93 checks total across the benchmark). The grader reports both a granular partial credit score (`checks_passed / total_checks`) and a strict binary outcome (`passed = True` iff all checks pass).
- **Grader Validation:** Every grader was tested and verified with zero false passes and zero false fails:
  - **Positive Check (`--mode oracle`):** All 6 human-verified reference solutions score `1.00` (100% checks passed).
  - **Negative Check (`--mode verify-graders`):** Six realistic naive-model outputs containing known human/AI precedence traps are deterministically rejected (`passed = False`), scoring partial credit (`0.20`–`0.75`) on surface fields while failing the end-to-end outcome.
  - **Unit Test Suite:** Validated via standard-library `python -m unittest discover -s tests -v`.

## 5. Results & Model Limitation Analysis

| Model | Trials per Task | Pass Rate | Consistency | Mean Partial Credit | Cost per Run |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`Oracle Reference`** | 1 | **100.0%** | **100.0%** | **1.00** | $0.0000 |
| **`Naive Baseline`** | 1 | **0.0%** | **0.0%** | **0.47** | $0.0000 |
| **`gemini-3.8-flash`** | 3 | **11.1%** | **0.0%** | **0.55** | $0.0150 |
| **`gpt-4o`** | 3 | **33.3%** | **0.0%** | **0.71** | $0.1240 |

### Per-Task Breakdown Across Models

| Task ID | Tested Model | Pass Rate | Mean Score | Primary Failure Mode & Tripping Point |
| :--- | :--- | :--- | :--- | :--- |
| **`task_01`** | `gemini-3.8-flash` | 0.0% | 0.50 | **Missed Super-Cap Erosion:** Correctly identifies the $315k General Cap, but awards full $780k PII breach claim without subtracting the $315k General Cap payout from the $945k Data Super-Cap under Section 11.4. |
| **`task_01`** | `gpt-4o` | 33.3% | 0.69 | **Exception Scope Confusion:** Solves cap erosion in trial 1, but bars $95k trade-secret lost profits permitted under Section 11.5(i). |
| **`task_02`** | `gemini-3.8-flash` | 33.3% | 0.63 | **Courier Cutoff & Holidays:** Identifies the Section 18.2 courier mandate, but misses the 5:00 PM ET cutoff in Section 18.3(b) and omits Mumbai holidays in Exhibit C. |
| **`task_02`** | `gpt-4o` | 66.7% | 0.88 | **Partial Cure Extension Trap:** Counts business days accurately in 2 trials, but treats the $110k partial payment as extending the cure window in 1 trial. |
| **`task_03`** | `gemini-3.8-flash` | 0.0% | 0.58 | **Headline Price Anchoring:** Flags volume and government exemptions, but fails to amortize Year-1 signing rebates and fee waivers into net effective seat price under Section 4.2. |
| **`task_03`** | `gpt-4o` | 0.0% | 0.71 | **Prepayment Misclassification:** Amortizes rebates on Deal 103, but misses the 3-year full prepayment exemption on Deal 104. |
| **`task_04`** | `gemini-3.8-flash` | 33.3% | 0.81 | **Scale Surcharge Omission:** Verifies parent guaranty cure for Tangible Net Worth, but omits the $125k scale surcharge for acquirers over $500M revenue (Section 16.3(d)). |
| **`task_04`** | `gpt-4o` | 66.7% | 0.94 | **Merger Deemed Assignment:** Accurately classifies all 4 transactions in 2 trials, but misses the reverse triangular merger trigger in 1 trial. |
| **`task_05`** | `gemini-3.8-flash` | 0.0% | 0.30 | **Accounting Hierarchy Inversion:** Fails to reverse $650k of GAAP-capitalized internal software dev payroll under Schedule 2.6 Part I, overpaying the earn-out by $1.4M+. |
| **`task_05`** | `gpt-4o` | 0.0% | 0.40 | **Undisclosed Fine Add-Back:** Caps advisory fees at $400k, but adds back an undisclosed post-closing OSHA fine barred under Section 3.4. |
| **`task_06`** | `gemini-3.8-flash` | 0.0% | 0.47 | **Interrelated Claims Deeming Bar:** Overlooks the Nov 2024 demand letter connection under Section 5.1 (wrongfully finding coverage for Claim B). |
| **`task_06`** | `gpt-4o` | 33.3% | 0.63 | **Soft Hammer Co-Insurance:** Correctly bars Claim B, but miscalculates the 70/30 co-insurance split on excess judgment over the recommended settlement. |

## 6. Cost and Runtime

| Operation | Scope | Average Runtime | Estimated Cost |
| :--- | :--- | :--- | :--- |
| **`Oracle Verification`** | All 6 tasks (Human Reference) | 0.12 seconds | $0.0000 |
| **`Grader Unit Tests`** | 4 test cases (unittest) | 0.11 seconds | $0.0000 |
| **`Naive Baseline`** | All 6 tasks (Adversarial Traps) | 0.12 seconds | $0.0000 |
| **`Gemini 3.8 Flash`** | 6 tasks x 3 trials (18 calls) | ~68 seconds | $0.0150 |
| **`GPT-4o`** | 6 tasks x 3 trials (18 calls) | ~74 seconds | $0.1240 |

## 7. Main Failure Mode & Hot Take

[Sequential Clause Anchoring vs. Hierarchical Norm Resolution]

Frontier language models process commercial agreements as linear narratives rather than directed dependency graphs of legal obligations. When an early clause establishes a clean quantitative baseline (such as a 1x 12-month liability cap or US GAAP EBITDA), the model anchors on that number. Subsequent clauses that introduce state-mutating carve-outs, cross-bucket cap erosion, or schedule hierarchy overrides fail to trigger backward re-computation.
Because models score respectable partial credit (55%–71%) by correctly answering surface provisions, their outputs appear convincing at first glance. However, their strict end-to-end reliability (pass^k) drops to 0.0%, demonstrating that current frontier models cannot be trusted with autonomous contract risk assessment without human-supervised precedence validation.

## 8. How to Run & Reproduce

[Environment Setup]

The harness uses Python 3 standard library modules only (json, urllib, re, unittest, argparse). Zero third-party dependencies are required to run oracle verification or unit tests.

# Clone the repository
git clone https://github.com/<your-username>/contract-precedence-eval.git
cd contract-precedence-eval
