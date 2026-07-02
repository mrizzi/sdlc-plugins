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
| eval-19 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-20 | 4/4 | 0 | 100% |
| eval-21 | 4/4 | 0 | 100% |
| eval-22 | 4/4 | 0 | 100% |
| eval-23 | 4/4 | 0 | 100% |
| eval-24 | 4/4 | 0 | 100% |
| eval-25 | 4/4 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 5/6 | 1 | 83% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 5/5 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "No output file contains explicit evidence about the behavior for CVSS &lt; 7.0. The embargo-check.md shows a threshold check ('Threshold: CVSS &gt;= 7.0', 'Meets threshold?: YES (7.5 &gt;= 7.0)') which implies the gate is conditional, but there is no explicit statement that the gate is skipped silently for Low or Moderate severity CVEs. The eval run only exercises the above-threshold case (CVSS 7.5). No negative-case behavior is documented in any output file."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Each listed issue shows: issue key, status, CVE ID (from labels), summary, and created date"
  **Evidence:** "Issues in Query 1 (TC-9001, TC-9002, TC-9003, TC-9004) and Query 2 (TC-9010) each show all five fields, e.g. line 30: 'TC-9001 — Status: New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created: 2026-06-08'. The Ready for QA table (TC-9020, line 79) also shows all five fields. However, the 'Excluded from Ready for QA' table (lines 85-88) lists TC-9023 and TC-9026 with columns 'Issue | Status | CVE | Summary | Reason' — these issues are missing the created date field, showing a 'Reason' column instead."

</details>

**Pass rate:** 98% · **Tokens:** 54,333 · **Duration:** 148s

**Baseline** (`d573976e`): 99% · 0 tokens · 0s

