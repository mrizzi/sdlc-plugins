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
| eval-6 | 5/6 | 1 | 83% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 8/8 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "The outputs only demonstrate the above-threshold case (CVSS 7.5). embargo-check.md line 15 defines the trigger threshold as 'CVSS &gt;= 7.0 (Critical or Important)' and line 16 shows 'Threshold met? YES -- 7.5 &gt;= 7.0'. While the threshold definition logically implies below-threshold CVEs would not trigger the gate, there is no explicit evidence that below-threshold CVEs are 'skipped silently' — the outputs do not describe or demonstrate below-threshold behavior, nor do they state that no message or log is produced when CVSS &lt; 7.0. Burden of proof is on PASS; the specific 'skipped silently' behavior is not evidenced."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Each listed issue shows: issue key, status, CVE ID (from labels), summary, and created date"
  **Evidence:** "Most issues show all five fields (e.g., 'TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created: 2026-06-08'). However, the two excluded issues in the Ready for QA section (TC-9023 and TC-9026) are listed in a table that shows Issue, Status, CVE, Summary, and Reason — but omits the Created date field. For example, TC-9023 row shows 'TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | Remediation in progress: TC-9025 is still In Progress' with no created date."

</details>

**Pass rate:** 99% · **Tokens:** 48,781 · **Duration:** 108s

**Baseline** (`4d9733a7`): 100% · 0 tokens · 0s

