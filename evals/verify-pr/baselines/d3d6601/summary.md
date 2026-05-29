## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/11 | 0 | 100% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 9/10 | 1 | 90% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — the 3-criteria detection (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) found no matches, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "The report.md does not contain an 'Eval Quality' row in the verification table. The table has 'Test Quality | N/A | No test files in diff' and 'Test Change Classification | N/A | No test files in diff' but no separate Eval Quality line. The 3-criteria detection mechanism (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) is not mentioned anywhere in the outputs. There is no evidence that Eval Quality was assessed or reported as N/A."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — the 3-criteria detection (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) found no matches, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "report.md line 13: 'Test Quality | PASS | All test functions have doc comments; no repetitive test patterns detected; Eval Quality N/A (no eval result reviews)' — Eval Quality is N/A and does not affect Test Quality. report.md line 100: 'Eval Quality — N/A: No eval result reviews found on the PR.' However, the report does NOT mention the specific 3-criteria detection mechanism (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals). The assertion requires that the 3-criteria detection is referenced. The report only states 'No eval result reviews found on the PR' without specifying the detection criteria used."

</details>

**Pass rate:** 96% · **Tokens:** 57,413 · **Duration:** 185s

**Baseline** (`fc7c4cb`): 92% · 35,122 tokens · 176s

