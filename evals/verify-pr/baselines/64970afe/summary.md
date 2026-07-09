## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 10/10 | 0 | 100% |
| eval-6 | 10/10 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — no reviews match the eval result detection criteria, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "No mention of 'Eval Quality' exists anywhere in the output files. The report.md table contains rows for Review Feedback, Root-Cause Investigation, Scope Containment, Diff Size, Commit Traceability, Sensitive Patterns, CI Status, Acceptance Criteria, Test Quality, Test Change Classification, and Verification Commands — but no 'Eval Quality' row. A grep for 'eval' and 'quality' across all output files returns no matches. The assertion requires a specific N/A designation for Eval Quality, which is absent from the outputs."

</details>

**Pass rate:** 98% · **Tokens:** 39,589 · **Duration:** 197s

**Baseline** (`4d9733a7`): 98% · 65,110 tokens · 231s

