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
| eval-17 | 4/5 | 1 | 80% |
| eval-18 | 5/5 | 0 | 100% |
| eval-19 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-20 | 4/4 | 0 | 100% |
| eval-21 | 4/4 | 0 | 100% |
| eval-22 | 4/4 | 0 | 100% |
| eval-23 | 4/4 | 0 | 100% |
| eval-24 | 4/4 | 0 | 100% |
| eval-25 | 4/4 | 0 | 100% |
| eval-26 | 5/5 | 0 | 100% |
| eval-27 | 5/5 | 0 | 100% |
| eval-28 | 5/5 | 0 | 100% |
| eval-29 | 5/5 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-30 | 4/4 | 0 | 100% |
| eval-31 | 4/4 | 0 | 100% |
| eval-32 | 4/4 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 6/6 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 8/8 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "The eval scenario only tests a single CVE with CVSS 7.5 (High). While embargo-check.md defines the trigger threshold as 'CVSS &gt;= 7.0' (line 17), there is no output file demonstrating the behavior for a below-threshold CVE. No output shows a Low or Moderate severity CVE being processed with the gate skipped silently. The threshold logic implies below-threshold CVEs would not trigger the gate, but there is no concrete evidence in the outputs showing silent skipping behavior for CVSS &lt; 7.0 CVEs."

</details>

**Pass rate:** 99% · **Tokens:** 58,180 · **Duration:** 124s

**Baseline** (`64970afe`): 99% · 48,781 tokens · 108s

