## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/11 | 1 | 91% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 9/10 | 1 | 90% |
| eval-5 | 9/10 | 1 | 90% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — the 3-criteria detection (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) found no matches, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "The report does not contain an explicit 'Eval Quality' subsection or row, nor does it mention the 3-criteria detection mechanism (author github-actions[bot], marker '## Eval Results', footer sdlc-workflow/run-evals). While Eval Quality is implicitly absent (no eval results are discussed), the assertion requires explicit mention of Eval Quality as N/A with the specific 3-criteria detection rationale. The summary table (line 13) shows 'Test Quality | PASS | All test functions have doc comments, no repetitive patterns' without breaking out Eval Quality as a component. There is no mention of github-actions[bot], '## Eval Results', or sdlc-workflow/run-evals anywhere in the outputs."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — the 3-criteria detection (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) found no matches, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "The report.md check table (lines 3-15) contains no 'Eval Quality' row. The table lists: Review Feedback, Root-Cause Investigation, Scope Containment, Diff Size, Commit Traceability, Sensitive Patterns, CI Status, Acceptance Criteria, Test Quality, Test Change Classification, Verification Commands. There is no mention of 'Eval Quality', the 3-criteria detection mechanism (github-actions[bot], ## Eval Results, sdlc-workflow/run-evals), or any eval quality assessment anywhere in the report or criterion files."

</details>

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — the 3-criteria detection (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) found no matches, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "The report.md does not contain any 'Eval Quality' row or section. There is no mention of 'Eval Quality', 'eval result reviews', 'github-actions[bot]', '## Eval Results', or 'sdlc-workflow/run-evals' anywhere in the report or criterion files. Without explicit N/A reporting for Eval Quality, the assertion that it is reported as N/A cannot be confirmed. The burden of proof is on PASS, and there is no concrete evidence of this specific determination being made."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — the 3-criteria detection (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) found no matches, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "The report does not contain an Eval Quality row in the summary table (lines 4-16). The table has rows for Review Feedback, Root-Cause Investigation, Scope Containment, Diff Size, Commit Traceability, Sensitive Patterns, CI Status, Acceptance Criteria, Test Quality, Test Change Classification, and Verification Commands — but no Eval Quality row. There is no mention of the 3-criteria detection logic (author github-actions[bot], marker '## Eval Results', footer sdlc-workflow/run-evals) anywhere in the report or criterion files. While the absence of an Eval Quality row could imply N/A, the assertion requires that the 3-criteria detection mechanism be explicitly referenced, which it is not."

</details>

**Pass rate:** 92% · **Tokens:** 35,122 · **Duration:** 176s

**Baseline** (`6b49958`): 100% · 59,008 tokens · 180s

