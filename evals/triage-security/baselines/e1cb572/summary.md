## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/10 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 4/5 | 1 | 80% |
| eval-5 | 5/5 | 0 | 100% |
| eval-6 | 5/5 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 5/5 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Cross-stream impact notice is NOT generated because the issue is unscoped — it covers all streams by definition (Step 7 Case B applies only to scoped issues)"
  **Evidence:** "remediation.md line 14 states 'No cross-stream impact comment (Case B) is needed because the other stream (2.2.x) is not affected.' While the output correctly does NOT generate a cross-stream impact notice, it gives the wrong reason. The assertion requires the justification to be that the issue is unscoped (Case B applies only to scoped issues). The output instead claims Case B is skipped because the other stream is not affected, implying Case B would have been triggered if 2.2.x were affected -- which contradicts the rule that Case B only applies to scoped issues."

</details>

**Pass rate:** 98% · **Tokens:** 46,914 · **Duration:** 102s

**Baseline** (`4f620b9`): 100% · 36,109 tokens · 83s

