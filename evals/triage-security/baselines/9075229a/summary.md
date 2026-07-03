## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/11 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 5/5 | 0 | 100% |
| eval-15 | 5/5 | 0 | 100% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 5/5 | 0 | 100% |
| eval-18 | 5/5 | 0 | 100% |
| eval-19 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-20 | 4/4 | 0 | 100% |
| eval-21 | 4/4 | 0 | 100% |
| eval-22 | 4/4 | 0 | 100% |
| eval-23 | 4/4 | 0 | 100% |
| eval-24 | 4/4 | 0 | 100% |
| eval-25 | 4/4 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 4/5 | 1 | 80% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 6/6 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 8/8 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Cross-stream impact notice is NOT generated because the issue is unscoped — it covers all streams by definition (Step 8 Case B applies only to scoped issues)"
  **Evidence:** "No cross-stream impact notice was generated (correct outcome), but the reasoning is wrong. remediation.md states: 'No Case B (cross-stream impact) applies because the other stream is not affected.' The correct reason per the assertion is that Case B does not apply because the issue is unscoped — an unscoped issue covers all streams by definition, so cross-stream notice is inapplicable regardless of whether other streams are affected. The output shows the agent applied Case B reasoning (checking stream affectedness) instead of correctly recognizing Case B is only for scoped issues."

</details>

**Pass rate:** 99% · **Tokens:** 48,425 · **Duration:** 112s

**Baseline** (`fcbfa091`): 100% · 44,507 tokens · 106s

