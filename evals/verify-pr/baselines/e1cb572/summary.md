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

- **Assertion:** "The report includes detailed findings for each failing check with specific evidence from the diff — Scope Containment identifies the missing test file by comparing PR files against the task specification, Acceptance Criteria provides per-criterion analysis explaining each gap"
  **Evidence:** "The Acceptance Criteria check provides detailed per-criterion analysis with code-level evidence (both in report.md and criterion-*.md files). However, Scope Containment is marked PASS with details: 'Changes are limited to the two files specified in the task: modules/fundamental/src/advisory/endpoints/get.rs and modules/fundamental/src/advisory/service/advisory.rs'. It does NOT identify the missing test file tests/api/advisory_summary.rs as a scope gap. The missing test file is mentioned only in the 'Additional Issues' section, not in the Scope Containment check. The assertion requires Scope Containment specifically to identify the missing test file by comparing PR files against the task specification, which it does not do."

</details>

**Pass rate:** 98% · **Tokens:** 62,023 · **Duration:** 207s

**Baseline** (`4f620b9`): 98% · 74,715 tokens · 312s

