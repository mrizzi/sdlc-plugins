## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 10/10 | 0 | 100% |
| eval-6 | 9/10 | 1 | 90% |

### Failed Assertions

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "The human reviewer comment from reviewer-b (comment id 50001) is NOT misidentified as an eval result — it is processed as a normal review comment (classified in review-50001.md) and its classification does not reference eval detection or eval metrics"
  **Evidence:** "review-50001.md classifies comment 50001 as 'suggestion' from 'reviewer-b (human reviewer)' and is processed as a normal review comment (not misidentified as an eval result). However, the classification file explicitly references eval detection criteria: 'This comment is NOT an eval result. It comes from a human reviewer... It does not match any of the eval result detection criteria: Author is NOT github-actions[bot], Body does not contain ## Eval Results, Body does not contain sdlc-workflow/run-evals.' The assertion requires that the classification does not reference eval detection, but it does."

</details>

**Pass rate:** 98% · **Tokens:** 71,339 · **Duration:** 241s

**Baseline** (`796c88c`): 100% · 59,919 tokens · 163s

