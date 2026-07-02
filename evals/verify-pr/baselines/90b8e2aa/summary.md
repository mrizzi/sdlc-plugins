## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 10/10 | 0 | 100% |
| eval-6 | 9/10 | 1 | 90% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — no reviews match the eval result detection criteria, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "report.md contains no 'Eval Quality' row in the verification table. The table rows are: Review Feedback, Root-Cause Investigation, Scope Containment, Diff Size, Commit Traceability, Sensitive Patterns, CI Status, Acceptance Criteria, Test Quality, Test Change Classification, Verification Commands. There is no mention of 'Eval Quality' anywhere in report.md or any criterion file. Without explicit evidence of an Eval Quality row set to N/A, the assertion cannot be confirmed."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "The human reviewer comment from reviewer-b (comment id 50001) is NOT misidentified as an eval result — it is processed as a normal review comment (classified in review-50001.md) and its classification does not reference eval detection or eval metrics"
  **Evidence:** "review-50001.md correctly classifies the comment as 'code change request' and processes it as a normal review comment. However, the classification's Reasoning section explicitly references eval detection: 'This is a human reviewer comment, not an eval result. The review (id 40002) is from user "reviewer-b" (a human user), not from github-actions[bot], and does not contain the ## Eval Results marker or sdlc-workflow/run-evals footer.' The assertion requires the classification does not reference eval detection, but the classification discusses the 3-criteria eval detection heuristic (even though it concludes the comment is NOT an eval result)."

</details>

**Pass rate:** 97% · **Tokens:** 37,278 · **Duration:** 168s

**Baseline** (`d573976e`): 100% · 71,215 tokens · 253s

