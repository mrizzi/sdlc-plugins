## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/12 | 1 | 92% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 12/14 | 2 | 86% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 10/10 | 0 | 100% |
| eval-6 | 7/10 | 3 | 70% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "The report includes detailed findings with specific evidence for each domain — file-by-file scope comparison (Intent Alignment), line-level pattern scanning results (Security), per-criterion code-level verification (Correctness), and test quality assessment (Style/Conventions) — not just pass/fail verdicts in the summary table"
  **Evidence:** "Correctness has extensive detailed findings: report.md lines 19-31 provide per-criterion code-level verification, and criterion-1.md through criterion-5.md contain multi-section analyses with code excerpts, data flow tracing, and test coverage analysis. However, Intent Alignment lacks file-by-file scope comparison — report.md line 7 says 'PR files match task specification exactly: 2 modified files and 1 new file, all as specified' without listing the actual file names (list.rs, service/mod.rs, tests/api/package.rs) compared against the task specification. Security lacks line-level pattern scanning results — report.md line 10 says only 'No secrets, credentials, or sensitive patterns detected in any added lines' with no enumeration of patterns scanned or lines examined. Style/Conventions has brief detail ('all 4 tests exercise distinct behaviors', 'all test functions have /// doc comments') but no separate detailed section. The report has detailed findings only for Correctness, not for all four domains as required."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "Each sub-task description includes a Target PR section with the PR URL https://github.com/trustify/trustify-backend/pull/744 (constraint 1.12)"
  **Evidence:** "subtask-1.md contains '## Target PR' with URL 'https://github.com/trustify/trustify-backend/pull/744'. However, subtask-2.md (root-cause task targeting sdlc-plugins) does NOT contain a Target PR section at all. grep for 'Target PR' only matches in subtask-1.md. The assertion requires 'Each sub-task description' to include this section."

- **Assertion:** "Each sub-task description includes a Review Context section with the original review comment text (constraint 1.12)"
  **Evidence:** "subtask-1.md contains '## Review Context' with comment ID 30001 and the full original review comment text. However, subtask-2.md (root-cause task) does NOT contain a Review Context section. grep for 'Review Context' only matches in subtask-1.md. The assertion requires 'Each sub-task description' to include this section."

</details>

<details>
<summary>eval-6: 3 failing assertions</summary>

- **Assertion:** "An eval failure sub-task is created for failing eval-3 — a sub-task description file targets eval-3 assertion failures and includes the failing assertion text and evidence"
  **Evidence:** "Only two sub-task files exist: subtask-1.md (about adding Markdown-specific documentation rule to Check 6, from reviewer-b's comment) and subtask-2.md (root-cause plan-feature skill gap). Neither targets eval-3 assertion failures. The report explicitly states on line 23: 'The 2 eval-3 failures are pre-existing (related to convention upgrade behavior in Check 1, which this PR does not modify) and do not require new sub-tasks.' No eval failure sub-task was created."

- **Assertion:** "Sub-task descriptions include Review Context with the failing assertion text and evidence from the eval review — the Review Context section quotes the two failing assertions about convention upgrade eligibility and sub-task creation, including the evidence text explaining what was missing"
  **Evidence:** "subtask-1.md has a Review Context section (lines 33-35), but it quotes reviewer-b's comment about Markdown documentation rules, not eval assertion failures. subtask-2.md has no Review Context section at all. No sub-task description quotes the eval-3 failing assertions about convention upgrade eligibility or sub-task creation."

- **Assertion:** "Root-cause investigation runs on the created eval failure sub-tasks — the report includes a Root-Cause Investigation verdict that is not N/A, indicating the investigation pipeline processed the eval failure sub-tasks"
  **Evidence:** "The report does include a Root-Cause Investigation verdict of 'DONE' (not N/A) in the table on line 10, and a full investigation in lines 78-89. However, the investigation ran on the reviewer-b feedback sub-task (Markdown exclusion gap), NOT on eval failure sub-tasks. The root cause identified is 'plan-feature skill gap: task excluded Markdown files without considering the repository's primary file format' -- this is about the reviewer's comment, not eval-3's failing assertions about convention upgrade eligibility. No eval failure sub-tasks were created (assertion 5), so the investigation could not have processed them."

</details>

**Pass rate:** 91% · **Tokens:** 79,591 · **Duration:** 392s

**Baseline** (`9a6ca95e`): 100% · 35,176 tokens · 162s

