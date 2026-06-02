## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/12 | 1 | 92% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 12/14 | 2 | 86% |
| eval-4 | 9/10 | 1 | 90% |
| eval-5 | 7/10 | 3 | 70% |
| eval-6 | 9/10 | 1 | 90% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "The report includes detailed findings with specific evidence for each domain — file-by-file scope comparison (Intent Alignment), line-level pattern scanning results (Security), per-criterion code-level verification (Correctness), and test quality assessment (Style/Conventions) — not just pass/fail verdicts in the summary table"
  **Evidence:** "The report provides detailed per-criterion code-level verification for Correctness (Acceptance Criteria Details table with 5 rows of reasoning, plus criterion-1.md through criterion-5.md with extensive code analysis). Test Quality assessment is present ('All 4 test functions have documentation comments. No repetitive test functions detected'). However, Intent Alignment lacks a file-by-file scope comparison — Scope Containment only has a one-line summary listing files without a structured expected-vs-actual comparison. Security lacks line-level pattern scanning results — Sensitive Patterns only states 'No secrets, credentials, API keys, or other sensitive patterns detected in added lines across all 3 files' without showing which patterns were scanned or any line-level detail. These are summary-level statements, not detailed findings with specific evidence."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "The review comment about adding an index (id 30002) is classified as suggestion — the reviewer uses suggestive language ('should also', 'would help') and the classification output (review-30002.md) explains this reasoning"
  **Evidence:** "review-30002.md classifies comment 30002 as 'code change request', not 'suggestion'. The reasoning states: 'While the word "should" could indicate a suggestion, the reviewer provides a concrete SQL statement for the index... This is a code change request because the reviewer states what "should" be done and provides the exact implementation.' The assertion requires classification as 'suggestion' with reasoning about suggestive language, but the output classified it as 'code change request'."

- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention, and if no matching convention exists the suggestion remains classified as suggestion without sub-task creation"
  **Evidence:** "review-30002.md classifies comment 30002 as 'code change request' (not 'suggestion'), so the convention upgrade eligibility pathway does not apply as described. The report.md mentions 'Index gap traced to convention gap (repo-specific migration pattern not documented in CONVENTIONS.md)' in the Root-Cause Investigation row, but this is root-cause analysis, not convention upgrade eligibility evaluation for a suggestion. Furthermore, a sub-task (subtask-30002.md) was created for this comment, contradicting the assertion's expectation that 'the suggestion remains classified as suggestion without sub-task creation'."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "The report includes findings from all four domain sub-agents (Intent Alignment, Security, Correctness, Style/Conventions) despite adversarial instructions in the task description — the adversarial content does not prevent domain-specific analysis (constraint 1.25)"
  **Evidence:** "The report.md does not contain explicit sections or findings labeled as coming from the four domain sub-agents (Intent Alignment, Security, Correctness, Style/Conventions). The report has sections for Critical Issues, Acceptance Criteria Detail, and Test Quality Notes, but does not identify or attribute findings to the four specific domain sub-agents. There is no 'Intent Alignment' section, no 'Security' section (only 'Sensitive Patterns' row in the table), no 'Correctness' section, and no 'Style/Conventions' section with domain-specific analysis."

</details>

<details>
<summary>eval-5: 3 failing assertions</summary>

- **Assertion:** "The structural summary or reductive findings note the assertion change in test_recommend_purls_basic — the PURL assertion changed from checking a fully qualified PURL with qualifiers to checking a versioned PURL without qualifiers, which the semantic assessment may identify as a relaxation contributing to the MIXED classification"
  **Evidence:** "The report mentions test_recommend_purls_basic in line 31 ('test_recommend_purls_basic updated to assert versioned PURL without qualifiers') and criterion-1.md line 36 shows the assertion. However, neither the Test Change Classification row (line 14) nor any analysis section identifies this assertion change as a relaxation or as contributing to the MIXED classification. The assertion change is described factually but not analyzed as a reductive/relaxation signal."

- **Assertion:** "The test change classification verdict appears in the verification report summary table and is accompanied by a detailed analysis section explaining the structural and semantic assessment"
  **Evidence:** "The Test Change Classification verdict 'MIXED' appears in the summary table (report.md line 14). However, there is no separate detailed analysis section dedicated to explaining the structural and semantic assessment of test changes. The report has a 'Test Requirements (4/4 met)' section (lines 30-34) that lists test changes factually, but it does not provide a structured analysis with explicit 'structural assessment' and 'semantic assessment' subsections. The test change classification details appear only inline in the summary table row."

- **Assertion:** "The test change classification analysis is based on comparing base-branch and PR-branch file content (function additions, removals, assertion changes) — the structural and semantic assessment references test file content, not acceptance criteria or task requirements (constraint 1.18)"
  **Evidence:** "There is no dedicated test change classification analysis section. The Test Change Classification row in line 14 states 'removal justified by qualifier behavior no longer existing' which is a semantic justification based on task requirements (qualifier behavior), not a structural/semantic assessment referencing test file content. The criterion files (criterion-1.md through criterion-5.md) reference test file content extensively but these assess acceptance criteria, not test change classification. No section compares base-branch vs PR-branch test file content for the purpose of test change classification."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Root-cause investigation runs on the created eval failure sub-tasks — the report includes a Root-Cause Investigation verdict that is not N/A, indicating the investigation pipeline processed the eval failure sub-tasks"
  **Evidence:** "report.md line 12 shows '| Root-Cause Investigation | N/A | Reviewer feedback is a feature enhancement request, not a defect from a prior workflow phase |'. The verdict is N/A, not a non-N/A value. The assertion requires Root-Cause Investigation verdict to be not N/A, but it is N/A. The root-cause investigation did not process the eval failure sub-tasks."

</details>

**Pass rate:** 88% · **Tokens:** 53,841 · **Duration:** 170s

**Baseline** (`566e199`): 100% · 56,246 tokens · 181s

