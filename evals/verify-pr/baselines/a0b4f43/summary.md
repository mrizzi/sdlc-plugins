## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/10 | 0 | 100% |
| eval-2 | 10/10 | 0 | 100% |
| eval-3 | 12/13 | 1 | 92% |
| eval-4 | 9/9 | 0 | 100% |
| eval-5 | 9/9 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "Convention upgrade eligibility is evaluated for review comment 30002 (index suggestion) — the review classification output (review-30002.md) or the report's Style/Conventions analysis explains whether the suggestion matches a documented or demonstrated project convention"
  **Evidence:** "review-30002.md classifies the comment directly as 'code change request' based on the reviewer's directive language ('The migration should also add an index'). It does not mention convention upgrade eligibility, convention analysis, or whether the index suggestion matches a documented or demonstrated project convention. The report (line 6) mentions 'index addition classified as convention gap (repo-specific, undocumented pattern)' in the Root-Cause Investigation row, but this is a root-cause classification, not a convention upgrade eligibility analysis for the review comment classification. There is no explicit evaluation of whether the suggestion qualifies for convention upgrade from suggestion to code change request."

</details>

**Pass rate:** 98% · **Tokens:** 53,912 · **Duration:** 165s

**Baseline** (`b89536d`): 98% · 58,919 tokens · 172s

