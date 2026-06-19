## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 9/10 | 1 | 90% |
| eval-6 | 10/10 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "The structural summary or reductive findings note the assertion change in test_recommend_purls_basic — the PURL assertion changed from checking a fully qualified PURL with qualifiers to checking a versioned PURL without qualifiers, which the semantic assessment may identify as a relaxation contributing to the MIXED classification"
  **Evidence:** "The report does not mention the assertion change in test_recommend_purls_basic as a reductive signal or relaxation. The assertion change is only mentioned in criterion-1.md (line 31-33) in the context of evaluating acceptance criteria, not as a structural/semantic finding contributing to the MIXED classification. The Test Change Classification analysis in report.md (lines 14, 29, 62) only identifies the removed function and added functions, not the assertion change within test_recommend_purls_basic."

</details>

**Pass rate:** 98% · **Tokens:** 60,000 · **Duration:** 300s

**Baseline** (`6f405ac`): 98% · 63,377 tokens · 175s

