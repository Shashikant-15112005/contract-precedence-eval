CONTRACT-PRECEDENCE-EVAL
> **Video Walkthrough Link:** [Watch the 5-Minute Walkthrough on Google Drive](https://drive.google.com/file/d/1_OxBmKleAipRW9Y_kkoaKPo-XS85V5xs/view?usp=sharing)
---
What is an Eval?
AI evals (short for evaluations) are systematic test suites and quality checks used to measure how well a large language model (LLM), generative AI application, or AI Agent performs on specific tasks. Think of them like unit tests in traditional software engineering or practice exams for a student. Because AI models produce free-form, probabilistic outputs rather than rigid code, evals help turn subjective "vibes" into objective data.
What Evals Actually Do?
Define Success: They force teams to explicitly write down what a "good" or "correct" AI response looks like before shipping code.
Catch Regressions: When you update a system prompt, switch to a new model, or tweak a retriever, evals tell you if your changes broke something that used to work.
Benchmark Models: Companies use them to compare different base models (like deciding whether to upgrade from Claude or OpenAI) to see which fits their use case best.
The Three Main Ways Evals Are Run:
A) Code-Based Evals (Deterministic): Uses exact rules, numeric tolerances, regex patterns, or schema validation. (e.g., Did the AI output a valid JSON object? Did the calculated liability match within $0.01?)
B) LLM-as-a-Judge: Uses a stronger, specialized AI model to review and score the output of the target AI based on a rubric. (e.g., On a scale of 1 to 5, how polite and accurate is this customer service reply?)
C) Human Evaluation: Having real product managers, domain experts, or users manually grade transcripts or edge cases. While expensive and slow, it provides the ultimate ground truth.
> **Note on Evaluation Method:** `CONTRACT-PRECEDENCE-EVAL` runs on **100% Deterministic Code-Based Grading** (Method A) to guarantee zero false passes, zero false fails, and zero judge bias.
---
I took participation in the micro1 Eval Hackathon, where instead of building an AI agent, the goal is to design a rigorous, reproducible evaluation (5–10 tasks) in a domain you know well that exposes a real, practical limitation of frontier AI models—and grades it reliably.
I Chose Lawyer / Legal Compliance
The Failure Mode: Models hallucinate or overlook cross-clause overrides and jurisdictional conflict of laws.
Why Frontier Models Fail: Models read contracts sequentially. When Section 4 establishes a standard 30-day notice, but an obscure Section 18.4 carve-out states "Notwithstanding Section 4, in events involving regulatory inquiry, notice is 48 hours and governed by Delaware law with an indemnity cap exclusion", frontier models routinely cite the 30-day rule.
Concrete Task Examples:
Statute of Limitations & Jurisdictional Deadlines: Calculating filing deadlines given tolling rules, court holidays, and forum selection clauses.
Liquidated Damages & Liability Caps: Determining total recoverable damages where specific carve-outs (e.g., willful misconduct, gross negligence, IP infringement) bypass the 1x contract cap.
Termination Right Triggers: Evaluating whether a cure period was violated based on strict notice requirements.
Why It Wins the Rubric: Output is structured JSON (e.g., `{"deadline": "2026-12-04", "capped_liability_usd": 1500000, "carve_outs_triggered": ["gross_negligence"]}`). Grader is 100% deterministic code (zero LLM-judge subjectivity).
---
Contract-Precedence-Eval: Measuring Cross-Clause Override Blindness in Commercial Contracts
1. What It Tests
Contract-Precedence-Eval measures whether frontier AI models can resolve hierarchical cross-clause overrides in commercial contracts—specifically when a general rule in one section is subordinated, carved out, or modified by a `"Notwithstanding"` clause, fee-erosion proviso, accounting hierarchy schedule, or endorsement located pages away.
2. Who It's For and Why It Matters
Corporate M&A attorneys, commercial litigators, in-house counsel, and insurance coverage specialists rely on contract review to price risk and calculate exposure. In real practice, contract errors rarely happen because a lawyer misreads a single sentence in isolation; they happen when two or more clauses interact:
Missing a cross-bucket erosion proviso in a SaaS Master Services Agreement misstates liability exposure by $315,000+.
Sending a default notice by email when the boilerplate Notices clause excludes Section 14 defaults invalidates a termination and exposes the terminating party to wrongful repudiation damages.
Applying standard US GAAP instead of a Stock Purchase Agreement's Schedule 2.6 Accounting Hierarchy swings an M&A earn-out payout by $1,400,000+.
3. Task Overview (6 Tasks)
Task ID	Task Title	Core Clause Interaction & Why Frontier Models Fail
`task_01`	SaaS MSA Multi-Tier Liability Cap, Super-Cap & Cross-Bucket Erosion	Models must include the $45k Implementation Fee in the 12-month lookback General Cap ($315k vs. $270k), apply Section 11.4 cross-bucket erosion (reducing the $945k 3x Data Super-Cap by the $315k General Cap payout to $630k), and distinguish Section 5 non-PII Confidentiality (uncapped + lost profits permitted under Section 11.5) from Section 6 PII Data Breaches.
`task_02`	Dispute Notice Validity, Courier Cutoff & Dual-Jurisdiction Cure Window	Models must reject an acknowledged Oct 12 email notice under the Section 18.2 physical-courier mandate, apply the post-5:00 PM ET courier cutoff (pushing Deemed Receipt to the 2nd Business Day, Oct 16), reject a partial escrow wire under Section 14.2, and exclude both New York and Mumbai banking holidays (Exhibit C) across a 7-Business-Day cure period.
`task_03`	Most Favored Nation (MFN) Effective Price & Retroactive Ratchet Audit	Models must evaluate 5 comparator deals against four Section 4.3 exemptions (government agency, >120% seat volume, 3-year 100% upfront prepayment), compute Effective Annual Per-Seat Price under Section 4.2 by amortizing Year-1 signing rebates and waived onboarding fees, and apply retroactive quarterly ratchet-down pricing across Q1–Q4.
`task_04`	Anti-Assignment, Reverse Triangular Merger & Safe Harbor Net-Worth Proviso	Models must recognize that a reverse triangular merger triggers Section 16.2 deemed assignment, verify whether a parent guaranty cures a Tangible Net Worth shortfall (Total Assets minus Intangibles minus Liabilities), catch Affiliate attribution to a Schedule D Restricted Competitor, and compute the two-tier Section 16.3(d) transfer + scale fee ($200k vs. $0 for internal restructurings).
`task_05`	M&A Earn-Out Adjusted EBITDA & Specific Accounting Hierarchy Override	Models must enforce Schedule 2.6's 3-tier Accounting Hierarchy where Part I overrides US GAAP: capping transaction advisory add-backs at $400k, subtracting the $120k historical baseline from Buyer overhead allocations, deducting $650k of GAAP-capitalized internal software dev payroll (100% mandatory expensing), and rejecting an undisclosed post-closing OSHA fine add-back.
`task_06`	Claims-Made Insurance: Interrelated Prior Demand Deeming & 70/30 Soft Hammer	Models must link a May 2026 class action back to an unreported Nov 2024 demand letter under the Section 5.1 Interrelated Claims Deeming Rule (barring coverage), draw covered Defense Costs from Endorsement No. 1's $500k Supplemental Defense Allowance before eroding the $5M primary limit, and calculate 70/30 co-insurance splits on post-refusal defense costs and excess judgment under the Section 6.1 Soft Hammer Clause.
4. Grading: How Each Task Is Scored & Validated
Every task is scored by a 100% deterministic Python code-based grader (`graders/grader.py`)—no subjective LLM-as-judge is used:
Numeric Tolerance: All dollar calculations are checked with a `$0.01` tolerance (`abs(actual - expected) <= 0.01`) to prevent false fails from floating-point rounding.
Partial Credit & Strict Binary Pass: Each task comprises 8 to 24 atomic field checks (93 checks total across the benchmark). The grader reports both a granular partial credit score (`checks_passed / total_checks`) and a strict binary outcome (`passed = True` iff all checks pass).
Grader Validation: Every grader was tested and verified with zero false passes and zero false fails:
Positive Check (`--mode oracle`): All 6 human-verified reference solutions score `1.00` (100% checks passed).
Negative Check (`--mode verify-graders`): Six realistic naive-model outputs containing known human/AI precedence traps are deterministically rejected (`passed = False`), scoring partial credit (`0.20`–`0.75`) on surface fields while failing the end-to-end outcome.
Unit Test Suite: Validated via standard-library `python -m unittest discover -s tests -v`.
5. How to Run & Reproduce
Environment Setup
The harness uses Python 3 standard library modules only (`json`, `urllib`, `re`, `unittest`, `argparse`). Zero third-party dependencies are required to run oracle verification or unit tests.
```bash
# Clone the repository
git clone https://github.com/<your-username>/contract-precedence-eval.git
cd contract-precedence-eval
```
Execution Steps & Commands
Step	Objective	Command to Run	Expected Output / Result
Step 1	Oracle Verification	`python run_eval.py --mode oracle`	`SUCCESS: All 6 reference solutions passed 100% of grader checks.`
Step 2	Grader Unit Tests	`python -m unittest discover -s tests -v`	`Ran 4 tests in 0.111s — OK`
Step 3	Negative Trap Verification	`python run_eval.py --mode verify-graders`	`SUCCESS: Zero false fails on reference solutions; zero false passes on naive outputs.`
Step 4	Run Live Gemini Model	`python run_eval.py --mode llm --provider gemini --model gemini-3.8-flash --trials 3`	Evaluates 6 tasks across 3 trials and saves to `results/`
Step 5	Run Live OpenAI Model	`python run_eval.py --mode llm --provider openai --model gpt-4o --trials 3`	Evaluates 6 tasks across 3 trials and saves to `results/`
Step 6	Generate Results Table	`python summarize_results.py`	Prints aggregated benchmark summary table
6. Results & Model Limitation Analysis
Benchmark Summary Table
Model (version, settings)	Trials per task	Pass rate (pass@1)	pass^k (Consistency)	Mean Partial Credit	Cost per full run
Oracle Reference (`solve`)	1	100.0%	100.0%	1.00	$0.0000
Naive Single-Pass Baseline	1	0.0%	0.0%	0.47	$0.0000
gemini-3.8-flash (temp=0.2)	3	11.1%	0.0%	0.55	$0.0150
gpt-4o (temp=0.2)	3	33.3%	0.0%	0.71	$0.1240
Per-Task Breakdown Across Models
Task ID	Tested Model	Pass Rate	pass^k	Mean Partial Credit	Primary Failure Mode & Tripping Point
`task_01`	`gemini-3.8-flash`<br>`gpt-4o`	0.0%<br>33.3%	0.0%<br>0.0%	0.50<br>0.69	Missed Super-Cap Erosion: Models correctly identify the $315k General Cap, but award the full $780k PII data breach claim without subtracting the $315k General Cap payout from the $945k Data Super-Cap under Section 11.4.
`task_02`	`gemini-3.8-flash`<br>`gpt-4o`	33.3%<br>66.7%	0.0%<br>0.0%	0.63<br>0.88	Procedural Courier Cutoff: Models identify the Section 18.2 physical courier mandate, but miss the 5:00 PM ET cutoff in Section 18.3(b) or omit the Mumbai banking holidays in Exhibit C.
`task_03`	`gemini-3.8-flash`<br>`gpt-4o`	0.0%<br>0.0%	0.0%<br>0.0%	0.58<br>0.71	Headline Price Anchoring: Models identify volume and government exemptions, but fail to amortize Year-1 signing rebates and fee waivers into the net effective seat price under Section 4.2.
`task_04`	`gemini-3.8-flash`<br>`gpt-4o`	33.3%<br>66.7%	0.0%<br>0.0%	0.81<br>0.94	Merger Deemed Assignment & Scale Fee: Models identify the parent guaranty cure for Tangible Net Worth, but fail to apply the $125k scale surcharge on transactions exceeding $500M revenue (Section 16.3(d)).
`task_05`	`gemini-3.8-flash`<br>`gpt-4o`	0.0%<br>0.0%	0.0%<br>0.0%	0.30<br>0.40	Accounting Hierarchy Inversion: Models fail to reverse $650k of GAAP-capitalized internal software development payroll under Schedule 2.6 Part I, overpaying the earn-out by $1.4M+.
`task_06`	`gemini-3.8-flash`<br>`gpt-4o`	0.0%<br>33.3%	0.0%<br>0.0%	0.47<br>0.63	Interrelated Claims Deeming Bar: Models overlook the Nov 2024 demand letter connection under Section 5.1 (wrongfully finding coverage for Claim B), and miscalculate 70/30 Soft Hammer co-insurance on Claim C.
7. Cost and Runtime
Operation	Scope	Average Runtime	Estimated Cost
Oracle Verification	All 6 tasks (Human Reference)	0.12 seconds	$0.0000
Grader Unit Test Suite	4 test cases (`unittest`)	0.11 seconds	$0.0000
Naive Baseline Checks	All 6 tasks (Adversarial Traps)	0.12 seconds	$0.0000
Gemini 3.8 Flash Full Run	6 tasks × 3 trials (18 calls)	~68 seconds	$0.0150
GPT-4o Full Run	6 tasks × 3 trials (18 calls)	~74 seconds	$0.1240
8. Main Failure Mode & Hot Take
> **Sequential Clause Anchoring vs. Hierarchical Norm Resolution**
Frontier language models process commercial agreements as linear narratives rather than directed dependency graphs of legal obligations. When an early clause establishes a clean quantitative baseline (such as a 1x 12-month liability cap or US GAAP EBITDA), the model anchors on that number. Subsequent clauses that introduce state-mutating carve-outs, cross-bucket cap erosion, or schedule hierarchy overrides fail to trigger backward re-computation.
Because models score respectable partial credit (55%–71%) by correctly answering surface provisions, their outputs appear convincing at first glance. However, their strict end-to-end reliability (`pass^k`) drops to 0.0%, demonstrating that current frontier models cannot be trusted with autonomous contract risk assessment without human-supervised precedence validation.
9. Provenance & AI Use Disclosure
Provenance: All six contracts, dispute scenarios, financial schedules, reference solutions, and test suites were authored specifically for the micro1 Eval Hackathon. All company names, contract numbers, and dispute figures are 100% synthetic. No confidential, proprietary, or un-licensed real-world data was used. Licensed under the MIT License.
AI Use & Human Review Disclosure: AI tools (Gemini) were used to assist with initial repository scaffolding, formatting markdown tables, and drafting baseline regex/schema boilerplate. Every contract clause interaction, mathematical derivation, calendar holiday calculation, reference JSON solution, and grader assertion was authored, reviewed, and mathematically verified against commercial law standards, and confirmed through automated unit tests.
10. Representative Transcripts
Transcript File	Task ID	Key Failure Demonstrated
`transcripts/sample_naive_failure_task_01.json`	`task_01`	Missed Section 11.4 cross-bucket erosion and trade-secret exception.
`transcripts/sample_naive_failure_task_02.json`	`task_02`	Missed Section 18.3(b) courier 5:00 PM cutoff and Exhibit C banking holidays.
`transcripts/sample_naive_failure_task_03.json`	`task_03`	Headline seat pricing vs. Section 4.2 net amortized effective seat price.
`transcripts/sample_naive_failure_task_04.json`	`task_04`	Reverse triangular merger trigger and Section 16.3(d) scale fee omission.
`transcripts/sample_naive_failure_task_05.json`	`task_05`	US GAAP software development capitalization override under Schedule 2.6.
`transcripts/sample_naive_failure_task_06.json`	`task_06`	Section 5.1 interrelated prior demand coverage bar and 70/30 Soft Hammer split.
